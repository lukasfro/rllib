"""Implementation of a Transformation that clamps the next step attributes."""

import torch.jit
from .abstract_transform import AbstractTransform
from rllib.dataset.datatypes import Observation


class NextStateClamper(AbstractTransform):
    """Implementation of a Next Scale Clamper.

    Given a next state, it will saturate it in the inverse transformation.

    This helps to limit the forward propagation of models.

    Parameters
    ----------
    low: torch.tensor
    high: torch.tensor
    """

    def __init__(self, low, high, constant_idx=None):
        super().__init__()
        self.low = low
        self.high = high
        self.constant_idx = [] if constant_idx is None else constant_idx

    def forward(self, observation: Observation):
        """See `AbstractTransform.__call__'."""
        return observation

    @torch.jit.export
    def inverse(self, observation: Observation):
        """See `AbstractTransform.inverse'."""
        next_state = torch.max(torch.min(observation.next_state, self.high), self.low)
        next_state[..., self.constant_idx] = 0.
        idx = torch.diag_embed(observation.next_state != next_state)
        next_scale_tril = observation.next_state_scale_tril
        try:
            next_scale_tril[idx].clamp_max_(1e-6)
            next_scale_tril[..., self.constant_idx, self.constant_idx].clamp_max_(1e-6)
        except IndexError:
            pass

        return Observation(
            state=observation.state,
            action=observation.action,
            reward=observation.reward,
            next_state=next_state,
            done=observation.done,
            next_action=observation.next_action,
            log_prob_action=observation.log_prob_action,
            entropy=observation.entropy,
            state_scale_tril=observation.state_scale_tril,
            next_state_scale_tril=next_scale_tril
        )
