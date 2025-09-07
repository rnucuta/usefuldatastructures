from functools import cache
from typing import List


def find_max_form(strs: List[str], m: int, n: int) -> int:
    """0/1 knapsack problem with 3 dimensions. https://leetcode.com/problems/ones-and-zeroes/description/"""

    @cache
    def dp(i: int, m: int, n: int) -> int:
        if i == 0 or (m == 0 and n == 0):
            return 0

        if strs[i - 1].count("0") > m or strs[i - 1].count("1") > n:
            return dp(i - 1, m, n)
        else:
            return max(
                dp(i - 1, m, n),
                dp(i - 1, m - strs[i - 1].count("0"), n - strs[i - 1].count("1")) + 1,
            )

    return dp(len(strs), m, n)
