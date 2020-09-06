"""V-MPO Agent Implementation."""
import torch.nn.modules.loss as loss

from rllib.algorithms.vmpo import VMPO
from rllib.value_function import NNValueFunction

from .mpo_agent import MPOAgent


class VMPOAgent(MPOAgent):
    """Implementation of an agent that runs V-MPO."""

    def __init__(
        self,
        policy,
        critic,
        criterion=loss.MSELoss,
        epsilon=0.1,
        epsilon_mean=0.1,
        epsilon_var=0.001,
        regularization=False,
        top_k_fraction=0.5,
        train_frequency=0,
        num_rollouts=2,
        *args,
        **kwargs,
    ):
        super().__init__(
            policy=policy,
            critic=critic,
            train_frequency=train_frequency,
            num_rollouts=num_rollouts,
            *args,
            **kwargs,
        )

        self.algorithm = VMPO(
            policy=policy,
            critic=critic,
            criterion=criterion(reduction="none"),
            epsilon=epsilon,
            epsilon_mean=epsilon_mean,
            epsilon_var=epsilon_var,
            regularization=regularization,
            top_k_fraction=top_k_fraction,
            gamma=self.gamma,
        )

        self.policy = self.algorithm.policy
        self.optimizer = type(self.optimizer)(
            [p for n, p in self.algorithm.named_parameters() if "target" not in n],
            **self.optimizer.defaults,
        )

    @classmethod
    def default(cls, environment, *args, **kwargs):
        """See `AbstractAgent.default'."""
        critic = NNValueFunction.default(environment)
        return super().default(environment, critic=critic, *args, **kwargs)

    def learn(self) -> None:
        """Learn with V-MPO (On-Policy?)."""
        super().learn()
        if self.train_frequency == 0:
            # If train_frequency == 0, then it is on-policy.
            # Thus, erase memory after training.
            self.memory.reset()