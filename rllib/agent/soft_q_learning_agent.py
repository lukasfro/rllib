"""Implementation of DQNAgent Algorithms."""
from rllib.agent import QLearningAgent
from rllib.algorithms.q_learning import SoftQLearning


class SoftQLearningAgent(QLearningAgent):
    """Implementation of a DQN-Learning agent.

    Parameters
    ----------
    q_function: AbstractQFunction
        q_function that is learned.
    criterion: nn.Module
        Criterion to minimize the TD-error.
    optimizer: nn.optim
        Optimization algorithm for q_function.
    memory: ExperienceReplay
        Memory where to store the observations.
    temperature: ParameterDecay.
        Temperature of Soft Q function.
    target_update_frequency: int
        How often to update the q_function target.
    gamma: float, optional
        Discount factor.
    exploration_steps: int, optional
        Number of random exploration steps.
    exploration_episodes: int, optional
        Number of random exploration steps.

    References
    ----------
    Mnih, Volodymyr, et al. (2015)
    Human-level control through deep reinforcement learning. Nature.
    """

    def __init__(self, env_name, q_function, criterion, optimizer,
                 memory, temperature, num_iter=1, batch_size=64,
                 target_update_frequency=4, train_frequency=0, num_rollouts=1,
                 gamma=1.0, exploration_steps=0, exploration_episodes=0, comment=''):
        super().__init__(env_name, q_function=q_function, policy=None,
                         criterion=criterion, optimizer=optimizer, memory=memory,
                         num_iter=num_iter, batch_size=batch_size,
                         target_update_frequency=target_update_frequency,
                         train_frequency=train_frequency, num_rollouts=num_rollouts,
                         gamma=gamma, exploration_steps=exploration_steps,
                         exploration_episodes=exploration_episodes, comment=comment)

        self.algorithm = SoftQLearning(q_function, criterion(reduction='none'),
                                       temperature, self.gamma)
        self.policy = self.algorithm.policy
