from typing import List, Tuple
from collections import defaultdict

import numpy as np
from torch.utils.data import Dataset


def stratified_split(classes_list: List[int], fraction=0.2) -> Tuple[
    List[int], List[int]]:
    """
    Return training and eval indices where each class is represented of
    the same fraction. Left element of tuple has _fraction_ amout of each class and
    """
    indices = defaultdict(list)
    for i, k in enumerate(classes_list):
        indices[k].append(i)

    left_indices = []
    right_indices = []
    for k, sub_indices in indices.items():
        size = int(fraction * len(sub_indices) + .5)
        sub = np.random.choice(sub_indices, size, replace=False)
        left_indices.extend(sub)
        right_indices.extend([i for i in sub_indices if i not in sub])

    assert len(left_indices) + len(right_indices) == len(classes_list)
    assert not any(i in right_indices for i in left_indices)
    return left_indices, right_indices


class DataSubSet(Dataset):

    def __init__(self, ds: Dataset, indices: List[int], transform=None):
        self.ds = ds
        self.indices = indices
        self.transform = transform

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item: int):
        i = self.ds[self.indices[item]]
        if self.transform is not None:
            img, *other = i
            return (self.transform(img), *other)
        return i

    @property
    def class_to_idx(self):
        return self.ds.class_to_idx

