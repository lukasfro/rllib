"""Implementation of Deterministic Policy Gradient Algorithms."""
from itertools import chain

import torch.nn.modules.loss as loss
from torch.optim import Adam

from rllib.algorithms.dpg import DPG
from rllib.policy import NNPolicy
from rllib.util.parameter_decay import Constant, OUNoise, ParameterDecay
from rllib.value_function import NNQFunction

from .off_policy_agent import OffPolicyAgent


class DPGAgent(OffPolicyAgent):
    """Implementation of the Deterministic Policy Gradient Agent.

    The AbstractDDPGAgent algorithm implements the DPG-Learning algorithm except for
    the computation of the TD-Error, which leads to different algorithms.

    TODO: build compatible q-function approximation.

    Parameters
    ----------
    critic: AbstractQFunction
        critic that is learned.
    policy: AbstractPolicy
        policy that is learned.
    criterion: nn.Module

    References
    ----------
    Silver, David, et al. (2014) "Deterministic policy gradient algorithms." JMLR.
    Lillicrap et. al. (2016). CONTINUOUS CONTROL WITH DEEP REINFORCEMENT LEARNING. ICLR.

    """

    def __init__(
        self,
        critic,
        policy,
        exploration_noise,
        criterion=loss.MSELoss,
        policy_noise=0.2,
        noise_clip=0.5,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        assert policy.deterministic, "Policy must be deterministic."
        self.algorithm = DPG(
            critic=critic,
            policy=policy,
            criterion=criterion(reduction="none"),
            gamma=self.gamma,
            policy_noise=policy_noise,
            noise_clip=noise_clip,
        )
        self.policy = self.algorithm.policy

        if not isinstance(exploration_noise, ParameterDecay):
            exploration_noise = Constant(exploration_noise)

        self.params["exploration_noise"] = exploration_noise
        self.dist_params.update(
            add_noise=True, policy_noise=self.params["exploration_noise"]
        )

    def train(self, val=True):
        """Set the agent in training mode."""
        super().train(val)
        self.dist_params.update(add_noise=True)

    def eval(self, val=True):
        """Set the agent in evaluation mode."""
        super().eval(val)
        self.dist_params.update(add_noise=False)

    @classmethod
    def default(cls, environment, *args, **kwargs):
        """See `AbstractAgent.default'."""
        critic = NNQFunction.default(environment)
        policy = NNPolicy.default(environment, deterministic=True)
        optimizer = Adam(chain(policy.parameters(), critic.parameters()), lr=3e-4)

        return super().default(
            environment=environment,
            critic=critic,
            policy=policy,
            optimizer=optimizer,
            exploration_noise=kwargs.pop(
                "exploration_noise", OUNoise(dim=environment.dim_action)
            ),
            policy_update_frequency=2,
            clip_gradient_val=10,
            *args,
            **kwargs,
        )
