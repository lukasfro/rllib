import rllib.util
from rllib.util.rollout import rollout_model, rollout_policy
import rllib.util.neural_networks
from rllib.util.plotting import plot_on_grid, plot_learning_losses, \
    plot_values_and_policy
from rllib.value_function import NNValueFunction
from rllib.policy import NNPolicy
from rllib.model.pendulum_model import PendulumModel
from rllib.environment.system_environment import SystemEnvironment
from rllib.environment.systems import InvertedPendulum
from rllib.algorithms.control.mmpo import ModelBasedMPO
from gpytorch.distributions import Delta
import torch
import torch.distributions
import torch.optim as optim
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


torch.manual_seed(0)


# %% Define Reward Function
def reward_function(state, action):
    cos_angle = torch.cos(state[..., 0])
    velocity = state[..., 1]

    angle_tolerance = rllib.util.tolerance(cos_angle, lower=0.95, upper=1., margin=0.1)
    velocity_tolerance = rllib.util.tolerance(velocity, lower=-.5, upper=0.5,
                                              margin=0.5)
    return angle_tolerance * velocity_tolerance


def state_transform(states):
    angle, angular_velocity = torch.split(states, 1, dim=-1)
    states = torch.cat((torch.cos(angle), torch.sin(angle), angular_velocity),
                       dim=-1)
    return states


bounds = [(-np.pi, np.pi), (-2, 2)]
plot_on_grid(lambda x: reward_function(x, action=None), bounds, num_entries=[100, 100])
plt.title('Reward function')
plt.xlabel('Angle')
plt.ylabel('Angular velocity')
plt.show()

# %% Define Policy and Value functions.

value_function = NNValueFunction(dim_state=3, layers=[64, 64], biased_head=False,
                                 input_transform=state_transform)
policy = NNPolicy(dim_state=3, dim_action=1, layers=[64, 64], biased_head=False,
                  squashed_output=True, input_transform=state_transform)
model = PendulumModel(mass=0.3, length=0.5, friction=0.005)
environment = SystemEnvironment(InvertedPendulum(mass=0.3, length=0.5, friction=0.005,
                                                 step_size=1 / 80))

mpo = ModelBasedMPO(model, reward_function, policy, value_function, epsilon=0.1,
                    epsilon_mean=0.01, epsilon_var=0.001, gamma=0.99)

optimizer = optim.Adam(mpo.parameters(), lr=5e-4)
value_losses = []
eta_parameters = []
policy_losses = []
policy_returns = []

init_distribution = torch.distributions.Uniform(torch.tensor([-np.pi, -0.05]),
                                                torch.tensor([np.pi, 0.05]))
# test_state = torch.tensor([[-np.pi, 0.]])

# %%
num_trajectories = 20
num_simulation_steps = 400
num_subsample = 2
batch_size = 100
refresh_interval = num_subsample

for i in tqdm(range(100)):
    # Compute the state distribution
    if i % refresh_interval == 0:
        with torch.no_grad():
            states = init_distribution.sample((num_trajectories,))
            states, actions = rollout_model(model, policy, initial_states=states,
                                            max_steps=num_simulation_steps)

            # Sum along trajectory, average across samples
            reward = reward_function(states, actions).sum(dim=0).mean()
            policy_returns.append(reward.numpy())

    if np.mean(policy_returns[-3:]) >= 200:
        break

    # Shuffle to get a state distribution
    trajectory = states.reshape(-1, states.shape[-1])
    np.random.shuffle(trajectory.numpy())

    policy_episode_loss = 0.
    value_episode_loss = 0.

    # Copy over old policy for KL divergence
    mpo.reset()

    # Iterate over state batches in the state distribution
    state_batches = torch.split(trajectory, batch_size)[::num_subsample]
    for states in state_batches:
        optimizer.zero_grad()
        losses = mpo(states, num_action_samples=15)
        losses.loss.backward()
        optimizer.step()

        # losses = mbrl.util.map_and_cast(lambda x: x.detach().numpy(), losses)
        # Track statistics
        value_episode_loss += losses.value_loss.detach().numpy()
        policy_episode_loss += losses.policy_loss.detach().numpy()

    value_losses.append(value_episode_loss / len(state_batches))
    policy_losses.append(policy_episode_loss / len(state_batches))

    eta_parameters.append([eta.detach().numpy() for eta in mpo.mpo_loss.parameters()])

# %%

plt.plot(refresh_interval * np.arange(len(policy_returns)), policy_returns)
plt.xlabel('Iteration')
plt.ylabel('Cumulative reward')
plt.show()

plot_learning_losses(policy_losses, value_losses, horizon=20)
plt.show()

# %% Test controller
# theta0 = -torch.tensor(np.pi)
test_state = torch.tensor([np.pi, 0.])
environment.state = test_state.numpy()
environment.initial_state = lambda: test_state
rollout_policy(environment, lambda x: Delta(policy(x).mean), max_steps=400, render=True)

with torch.no_grad():
    states, actions = rollout_model(model, lambda x: Delta(policy(x).mean),
                                    initial_states=test_state, max_steps=400)
    rewards = reward_function(states, actions).numpy()
    states = states.numpy()

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 5))

plt.sca(ax1)
plt.plot(states[:, 0], states[:, 1], 'x')
plt.plot(states[-1, 0], states[-1, 1], 'x')
plt.xlabel('Angle [rad]')
plt.ylabel('Angular velocity [rad/s]')

plt.sca(ax2)
plt.plot(rewards)
plt.xlabel('Time step')
plt.ylabel('Instantaneous reward')
plt.show()
print(f'Cumulative reward: {np.sum(rewards)}')

bounds = [(-2 * np.pi, 2 * np.pi), (-12, 12)]
ax_value, ax_policy = plot_values_and_policy(value_function, policy, bounds, [200, 200])
ax_value.plot(states[:, 0], states[:, 1], color='C1')
ax_value.plot(states[-1, 0], states[-1, 1], 'x', color='C1')
plt.show()
