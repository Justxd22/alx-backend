#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination."""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Server class to paginate a database of popular baby names."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cache dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Return data about page."""
        d = self.indexed_dataset()
        assert index is not None and index >= 0 and index <= max(d.keys())
        paged = []
        data_count = 0
        nindex = None
        for i, item in d.items():
            if i >= index and data_count < page_size:
                paged.append(item)
                data_count += 1
                continue
            if data_count == page_size:
                nindex = i
                break
        return {
            "index": index,
            "next_index": nindex,
            "page_size": len(paged),
            "data": paged,
        }
