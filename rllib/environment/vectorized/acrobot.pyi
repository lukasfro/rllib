from typing import Any, Tuple

from gym.envs.classic_control.acrobot import AcrobotEnv

from rllib.dataset.datatypes import Action, Array, Done, Reward, State
from rllib.environment.vectorized.util import VectorizedEnv

class VectorizedAcrobotEnv(AcrobotEnv, VectorizedEnv):
    """Vectorized implementation of Acrobot with continuous actions."""

    max_torque: float
    def __init__(self, discrete: bool = ...) -> None: ...
    def step(self, action: Action) -> Tuple[State, Reward, Done, dict]: ...
    def _dsdt(self, s_augmented: Array, t: Any) -> Array: ...
    def _get_ob(self) -> State: ...
    def _terminal(self) -> Done: ...

class DiscreteVectorizedAcrobotEnv(VectorizedAcrobotEnv):
    """Vectorized Implementation of Acrobot with discrete actions."""

    def __init__(self) -> None: ...
    def step(self, action: Action) -> Tuple[State, Reward, Done, dict]: ...