#!/usr/bin/env python3
"""Tuple of size two containing a start index and an end index."""


import csv
import math
from typing import List


def index_range(page, page_size):
    """Tuple of size two containing a start index and an end index."""
    return (((page - 1) * page_size), (page * page_size))


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Server class to paginate a database of popular baby names."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cache dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get page from size/page."""
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0
        index = index_range(page=page, page_size=page_size)
        if index[0] > len(self.dataset()):
            return []
        return self.dataset()[index[0]:index[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return data about page."""
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0
        index = index_range(page=page, page_size=page_size)
        return {"page_size": page_size,
                "page": page,
                "data": self.get_page(page, page_size),
                "next_page": page + 1 if index[1] < len(self.__dataset)
                else None,
                "prev_page": page - 1 if index[0] > 0 else None,
                "total_pages": math.ceil(len(self.dataset()) / page_size),
                }
