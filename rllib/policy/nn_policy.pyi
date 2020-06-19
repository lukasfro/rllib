from typing import List, Optional, Type, TypeVar

import torch
from torch import Tensor

from rllib.dataset.datatypes import Action, TupleDistribution

from .abstract_policy import AbstractPolicy

T = TypeVar("T", bound="NNPolicy")

class NNPolicy(AbstractPolicy):
    input_transform: torch.nn.Module
    nn: torch.nn.Module
    def __init__(
        self,
        dim_state: int,
        dim_action: int,
        num_states: int = ...,
        num_actions: int = ...,
        layers: Optional[List[int]] = ...,
        biased_head: bool = ...,
        non_linearity: str = ...,
        squashed_output: bool = ...,
        tau: float = ...,
        deterministic: bool = ...,
        action_scale: Action = ...,
        input_transform: Optional[torch.nn.Module] = ...,
    ) -> None: ...
    @classmethod
    def from_other(cls: Type[T], other: T) -> T: ...
    @classmethod
    def from_nn(
        cls: Type[T],
        module: torch.nn.Module,
        dim_state: int,
        dim_action: int,
        num_states: int = ...,
        num_actions: int = ...,
        tau: float = ...,
        deterministic: bool = ...,
        action_scale: Action = ...,
        input_transform: Optional[torch.nn.Module] = ...,
    ): ...
    def forward(self, *args: Tensor, **kwargs) -> TupleDistribution: ...
    def embeddings(self, state: Tensor, action: Optional[Tensor] = ...) -> Tensor: ...

class FelixPolicy(AbstractPolicy):
    def __init__(
        self,
        dim_state: int,
        dim_action: int,
        num_states: int = ...,
        num_actions: int = ...,
        tau: float = ...,
        deterministic: bool = ...,
        action_scale: Action = ...,
        input_transform: Optional[torch.nn.Module] = ...,
    ) -> None: ...
