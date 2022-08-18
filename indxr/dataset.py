from typing import Callable, Dict

import torch

from .indxr import Indxr


class Dataset(torch.utils.data.Dataset):
    def __init__(
        self,
        indxr_args: Dict,
        callback: Callable = None,
    ):
        self.indxr_args = indxr_args
        self.callback = callback

        self.main_index = Indxr(**indxr_args)

    # Support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index: int) -> str:

        if self.callback:
            return self.callback(self.main_index[index])

        return self.main_index[index]

    # This allows to call len(dataset) to get the dataset size
    def __len__(self) -> int:
        return len(self.main_index)
