"""Interface for agents."""

from abc import ABCMeta

import torch

from rllib.util.logger import Logger
from rllib.util.utilities import tensor_to_distribution


class AbstractAgent(object, metaclass=ABCMeta):
    """Interface for agents that interact with an environment.

    Parameters
    ----------
    gamma: float, optional (default=1.0)
        MDP discount factor.
    exploration_steps: int, optional (default=0)
        initial exploratory steps.
    exploration_episodes: int, optional (default=0)
        initial exploratory episodes

    Methods
    -------
    act(state): int or ndarray
        Given a state, it returns an action to input to the environment.
    observe(observation):
        Record an observation from the environment.
    start_episode:
        Start a new episode.
    end_episode:
        End an episode.
    end_interaction:
        End an interaction with an environment.
    """

    def __init__(self, environment, gamma=1.0, exploration_steps=0,
                 exploration_episodes=0, comment=''):
        self.environment = environment
        self.logger = Logger(f"{environment.title()}/{self.name}", comment=comment)
        self.counters = {'total_episodes': 0, 'total_steps': 0}
        self.episode_steps = []

        self.gamma = gamma
        self.exploration_episodes = exploration_episodes
        self.exploration_steps = exploration_steps

        self._training = True

        self.comment = comment

    def __str__(self):
        """Generate string to parse the agent."""
        comment = self.comment if len(self.comment) else self.policy.__class__.__name__
        opening = "=" * 88
        str_ = f"\n{opening}\n{self.name} in {self.environment} with {comment}\n"
        str_ += f"Total episodes {self.counters['total_episodes']}\n"
        str_ += f"Total steps {self.counters['total_steps']}\n"
        str_ += f"{self.logger}{opening}\n"
        return str_

    def act(self, state):
        """Ask the agent for an action to interact with the environment."""
        if self.total_steps < self.exploration_steps or (
                self.total_episodes < self.exploration_episodes):
            policy = self.policy.random()
        else:
            if not isinstance(state, torch.Tensor):
                state = torch.tensor(state, dtype=torch.get_default_dtype())
            policy = self.policy(state)

        self.pi = tensor_to_distribution(policy)
        if self._training:
            action = self.pi.sample()
        elif self.pi.has_enumerate_support:
            action = torch.argmax(self.pi.probs)
        else:
            action = self.pi.mean

        return action.detach().numpy()

    def observe(self, observation):
        """Observe transition from the environment.

        Parameters
        ----------
        observation: Observation

        """
        self.policy.update()  # update policy parameters (eps-greedy.)

        self.counters['total_steps'] += 1
        self.episode_steps[-1] += 1
        self.logger.update(rewards=observation.reward.item())
        self.logger.update(entropy=observation.entropy.item())

    def start_episode(self):
        """Start a new episode."""
        self.episode_steps.append(0)

    def end_episode(self):
        """End an episode."""
        self.counters['total_episodes'] += 1
        rewards = self.logger.current['rewards']
        self.logger.end_episode(environment_return=rewards[0] * rewards[1])

    def end_interaction(self):
        """End the interaction with the environment."""
        pass

    def _train(self):
        """Train the agent."""
        pass

    def train(self, val=True):
        """Set the agent in training mode."""
        self._training = val

    def eval(self, val=True):
        """Set the agent in evaluation mode."""
        self.train(not val)

    @property
    def total_episodes(self):
        """Return number of steps in current episode."""
        return self.counters['total_episodes']

    @property
    def total_steps(self):
        """Return number of steps of interaction with environment."""
        return self.counters['total_steps']

    @property
    def name(self):
        """Return class name."""
        return self.__class__.__name__
