from typing import Optional, List, Tuple, Union

import numpy as np
import torch.nn as nn
from torch import Tensor


def deep_copy_module(module: nn.Module) -> nn.Module: ...


class Swish(nn.Module):
    def forward(self, *args: Tensor, **kwargs) -> Tensor: ...


def parse_nonlinearity(non_linearity: str) -> nn.Module: ...


def parse_layers(layers: Optional[List[int]], in_dim: int, non_linearity: str
                 ) -> Tuple[nn.Sequential, int]: ...


def update_parameters(target_module: nn.Module, new_module: nn.Module, tau: float = 0.
                      ) -> None: ...


def count_vars(module: nn.Module) -> int: ...


def zero_bias(module: nn.Module) -> None: ...


def inverse_softplus(x: Tensor) -> Tensor: ...


class TileCode(nn.Module):
    tiles: Tensor
    bins: Tensor
    num_outputs: int
    extra_dims: int
    one_hot: bool

    def __init__(self, low: List[float], high: List[float], bins: int, one_hot: bool = True) -> None: ...

    def _tuple_to_int(self, tuple_: Union[Tensor, Tuple[Tensor]]) -> Tensor: ...

    def forward(self, *args: Tensor, **kwargs) -> Tensor: ...


def digitize(tensor: Tensor, bin_boundaries: Tensor) -> Tensor: ...


class OneHotEncode(nn.Module):
    num_classes: int
    extra_dim: int

    def __init__(self, num_classes: int) -> None: ...

    def forward(self, *args: Tensor, **kwargs) -> Tensor: ...


def one_hot_encode(tensor: Tensor, num_classes: int) -> Tensor: ...


def get_batch_size(tensor: Tensor) -> Tuple[int]: ...


def random_tensor(discrete: bool, dim: int, batch_size: int = None) -> Tensor: ...


def repeat_along_dimension(array: Tensor, number: int, dim: int = 0) -> Tensor: ...


def torch_quadratic(array: Tensor, matrix: Tensor) -> Tensor: ...


def freeze_parameters(module: nn.Module) -> None: ...


def unfreeze_parameters(module: nn.Module) -> None: ...


class disable_gradient(object):
    def __init__(self, *modules) -> None: ...

    def __enter__(self) -> None: ...

    def __exit__(self, *args) -> None: ...
