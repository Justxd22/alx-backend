#!/usr/bin/env python3
"""Tuple of size two containing a start index and an end index."""


def index_range(page, page_size):
    """Tuple of size two containing a start index and an end index."""
    return (((page - 1) * page_size), (page * page_size))
