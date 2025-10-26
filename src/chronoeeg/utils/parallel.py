"""Parallel processing utilities."""

from typing import Callable, List, Any
from joblib import Parallel, delayed


def parallel_process(
    func: Callable,
    items: List[Any],
    n_jobs: int = -1,
    desc: str = "Processing"
) -> List[Any]:
    """
    Process items in parallel using joblib.
    
    Parameters
    ----------
    func : Callable
        Function to apply to each item
    items : List
        Items to process
    n_jobs : int
        Number of parallel jobs (-1 = all cores)
    desc : str
        Description for progress bar
    
    Returns
    -------
    List
        Results from processing each item
    """
    return Parallel(n_jobs=n_jobs)(
        delayed(func)(item) for item in items
    )
