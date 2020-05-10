"""Python Script Template."""
import torch
import torch.nn as nn
import torch.optim as optim

from rllib.algorithms.mpc import RandomShooting, CEMShooting, MPPIShooting
from rllib.environment import GymEnvironment
from rllib.policy.mpc_policy import MPCPolicy
from rllib.model.environment_model import EnvironmentModel
from rllib.reward.environment_reward import EnvironmentReward
from rllib.dataset.experience_replay import ExperienceReplay
from rllib.util.training import evaluate_agent

from rllib.agent import MPCAgent

from rllib.algorithms.td import ModelBasedTDLearning
import copy


class EnvironmentTermination(nn.Module):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment

    def forward(self, state, action, next_state=None):
        self.environment.state = state
        next_state, reward, done, _ = self.environment.step(action)
        return done

SEED = 0
MAX_STEPS = 200
# ENVIRONMENT = 'VPendulum-v0'
ENVIRONMENT = 'VContinuous-CartPole-v0'

env = GymEnvironment(ENVIRONMENT, SEED)
env_model = copy.deepcopy(env)
env_model.reset()
dynamical_model = EnvironmentModel(env_model)
reward_model = EnvironmentReward(env_model)
termination = EnvironmentTermination(env_model)
GAMMA = 0.99
horizon = 50
num_iter = 5
num_samples = 100
num_elites = 5
num_steps = horizon
solver = 'cem_shooting'
kappa = 1.
betas = [0.2, 0.8, 0]
warm_start = True
num_cpu = 2

memory = ExperienceReplay(max_len=2000, num_steps=1)

value_function = None  # NNValueFunction(env.dim_state, layers=[64, 64])
# optimizer = optim.Adam(value_function.parameters(), lr=1e-4)

if solver == 'random_shooting':
    mpc_solver = RandomShooting(
        dynamical_model, reward_model, horizon, gamma=GAMMA,
        num_samples=num_samples, num_elites=num_elites,
        termination=termination, terminal_reward=value_function,
        warm_start=warm_start, default_action='mean', num_cpu=num_cpu)
elif solver == 'cem_shooting':
    mpc_solver = CEMShooting(
        dynamical_model, reward_model, horizon, gamma=GAMMA,
        num_iter=num_iter, num_samples=num_samples, num_elites=num_elites,
        termination=termination, terminal_reward=value_function,
        warm_start=warm_start, default_action='mean', num_cpu=num_cpu)
elif solver == 'mppi_shooting':
    mpc_solver = MPPIShooting(
        dynamical_model, reward_model, horizon, gamma=GAMMA, num_iter=num_iter,
        kappa=kappa, filter_coefficients=betas, num_samples=num_samples,
        termination=termination, terminal_reward=value_function,
        warm_start=warm_start, default_action='mean', num_cpu=num_cpu)
else:
    raise NotImplementedError

policy = MPCPolicy(mpc_solver)
value_learning = ModelBasedTDLearning(
    value_function, criterion=nn.MSELoss(reduction='none'), policy=policy,
    dynamical_model=dynamical_model, reward_model=reward_model,
    termination=termination, num_steps=num_steps, gamma=GAMMA)

agent = MPCAgent(env.name, mpc_policy=policy)
evaluate_agent(agent, environment=env, num_episodes=1, max_steps=MAX_STEPS, render=True)