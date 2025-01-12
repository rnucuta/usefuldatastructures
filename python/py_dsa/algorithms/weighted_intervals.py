from typing import List


def jobScheduling(
    startTime: List[float], endTime: List[float], profit: List[float]
) -> float:
    """Schedules jobs to achieve maximum profit such that there are no overlapping jobs.
    This is an iteration of the weighted interval scheduling problem

    Args:
        startTime (List[int]): A list of start times for each job.
        endTime (List[int]): A list of end times for each job.
        profit (List[int]): A list of profits for each job.

    Returns:
        int: The maximum profit that can be achieved by scheduling jobs without overlapping.

    """
    # goal: find a way to schedule jobs
    # to achieve maximum profit such
    # that there are no overlapping jobs
    # 1. sort by end times
    n = len(startTime)
    jobs = [(0, 0, 0)] + [(endTime[i], startTime[i], profit[i]) for i in range(n)]
    jobs.sort()

    # 2. create function p(j) = i
    # where j is job index, and i is latest job whose end time is less
    # the start time. O(n log(n))
    p = [0] * (n + 1)
    for i, job in enumerate(jobs[1:]):
        startTime = job[1]
        l, r = 1, i
        while l <= r:
            mid = (l + r) // 2
            if jobs[mid][0] > startTime:
                r = mid - 1
            elif jobs[mid][0] <= startTime:
                l = mid + 1
        p[i + 1] = l - 1

    # base case:
    # if there are no jobs that are not overlapping with current
    # job, including it will add 0 benefit
    # recursive problem:
    dp = [0] * (n + 1)

    # o(n)
    for i in range(1, n + 1):
        # include job, which means have to go
        # to last previously acceptable job or skip job
        dp[i] = max(jobs[i][2] + dp[p[i]], dp[i - 1])

    return dp[-1]
