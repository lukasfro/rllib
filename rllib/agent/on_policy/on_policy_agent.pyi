"""On Policy Agent."""
from typing import List

from torch.optim.optimizer import Optimizer

from .abstract_agent import AbstractAgent
from rllib.algorithms.abstract_algorithm import AbstractAlgorithm
from rllib.dataset.datatypes import Observation


class OnPolicyAgent(AbstractAgent):
    """Template for an on-policy algorithm."""

    algorithm: AbstractAlgorithm
    batch_size: int
    trajectories: List[List[Observation]]
    optimizer: Optimizer
    target_update_frequency: int
    num_iter: int


    def __init__(self, env_name: str, optimizer: Optimizer,
                 batch_size: int = 1, target_update_frequency: int = 1, num_iter: int = 1,
                 train_frequency: int = 0, num_rollouts: int = 1, gamma: float = 1.0,
                 exploration_steps: int = 0, exploration_episodes: int = 0,
                 comment: str = '') -> None: ...