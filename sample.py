"""
Example usage of timeitPro `timeit` decorator.
"""

from timeitPro.core import timeit
from timeitPro.dashboard import run_dashboard


# -----------------------------
# Example 1: Simple function
# -----------------------------
@timeit(runs=5, show_console=True, show_average=True)
def compute_squares(n: int) -> int:
    """
    Compute the sum of squares from 1 to n.
    Simulates CPU work.
    """
    result = sum(i * i for i in range(1, n + 1))
    return result


# -----------------------------
# Example 2: Function with memory usage
# -----------------------------
@timeit(runs=3, show_console=True, show_average=True)
def create_list(size: int) -> list[int]:
    """
    Create a large list of integers to simulate memory usage.
    """
    lst = [i for i in range(size)]
    return lst


if __name__ == "__main__":
    # Run the functions
    print("Running compute_squares(1000)...")
    compute_squares(1_000_000)

    print("\nRunning create_list(100000)...")
    create_list(1_000_000)

    run_dashboard()
