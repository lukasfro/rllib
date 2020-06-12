"""Implementation of Advantage-Actor Critic Agent."""

from rllib.algorithms.gaac import GAAC

from .actor_critic_agent import ActorCriticAgent


class GAACAgent(ActorCriticAgent):
    """Implementation of the Advantage-Actor Critic.

    TODO: build compatible function approximation.

    References
    ----------
    Mnih, V., et al. (2016).
    Asynchronous methods for deep reinforcement learning. ICML.
    """

    def __init__(self, policy, critic, optimizer,
                 criterion, num_iter=1, target_update_frequency=1,
                 lambda_=0.97,
                 train_frequency=0, num_rollouts=1,
                 gamma=1.0, exploration_steps=0, exploration_episodes=0,
                 tensorboard=False, comment=''):
        super().__init__(policy=policy, critic=critic, optimizer=optimizer,
                         criterion=criterion, num_iter=num_iter,
                         target_update_frequency=target_update_frequency,
                         train_frequency=train_frequency, num_rollouts=num_rollouts,
                         gamma=gamma, exploration_steps=exploration_steps,
                         exploration_episodes=exploration_episodes,
                         tensorboard=tensorboard, comment=comment)
        self.algorithm = GAAC(policy, critic, criterion(reduction='none'), lambda_,
                              gamma)
        self.policy = self.algorithm.policy
