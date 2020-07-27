from typing import Callable, Optional, Tuple, Union

import numpy as np
import torch.__spec__ as torch_mod
from torch import Tensor

from rllib.dataset.datatypes import (
    Array,
    Distribution,
    Gaussian,
    Reward,
    TupleDistribution,
)

def get_backend(array: Array) -> Union[np, torch_mod]: ...
def mellow_max(values: Array, omega: float = ...) -> Array: ...
def integrate(
    function: Callable,
    distribution: Distribution,
    out_dim: Optional[int] = ...,
    num_samples: int = ...,
) -> Tensor: ...
def tensor_to_distribution(args: TupleDistribution, **kwargs) -> Distribution: ...
def separated_kl(p: Gaussian, q: Gaussian) -> Tuple[Tensor, Tensor]: ...
def sample_mean_and_cov(sample: Tensor, diag: bool = ...) -> Tuple[Tensor, Tensor]: ...
def safe_cholesky(covariance_matrix: Tensor, jitter: float = ...) -> Tensor: ...
def moving_average_filter(x: Array, y: Array, horizon: int) -> Array: ...

class RewardTransformer(object):
    offset: float
    low: float
    high: float
    scale: float
    def __init__(
        self,
        offset: float = ...,
        low: float = ...,
        high: float = ...,
        scale: float = ...,
    ) -> None: ...
    def __call__(self, reward: Reward) -> Reward: ...
