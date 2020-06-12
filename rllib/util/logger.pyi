"""Implementation of a Logger class."""

from typing import Dict, Iterator, List, Tuple, Union

import numpy as np
import tensorboardX
import torch


class Logger(object):
    statistics: List[Dict[str, float]]
    current: Dict[str, Tuple[int, float]]
    writer: tensorboardX.SummaryWriter
    episode: int
    keys: set
    _tensorboard: bool

    def __init__(self, name: str, comment: str = '', tensorboard: bool=False) -> None: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Dict[str, float]]: ...

    def __getitem__(self, item: int) -> Dict[str, float]: ...

    def __str__(self) -> str: ...

    def get(self, key: str) -> List[float]: ...

    def update(self, **kwargs) -> None: ...

    def end_episode(self, **kwargs) -> None: ...

    def save_hparams(self, hparams: dict) -> None: ...

    def export_to_json(self) -> None: ...

    def log_hparams(self, hparams: dict, metrics: dict = None) -> None: ...
