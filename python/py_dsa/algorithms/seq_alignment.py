from typing import Callable, Tuple, List


def sequence_align_slow(
    x: str, y: str, c: Callable[[str, str], float], delta: float
) -> Tuple[List[Tuple[str, str]], float]:
    """Needleman-Wunsch algorithm for global sequence alignment.

    The Needleman-Wunsch algorithm is a dynamic programming algorithm used for global sequence alignment.
    It is particularly useful for aligning two sequences of similar length, and is often used in bioinformatics
    to align protein or nucleotide sequences. The algorithm works by building a 2D matrix of scores, where
    each cell in the matrix represents the optimal alignment score for the subsequences ending at the corresponding
    positions in the input sequences.

    Args:
        x (str): The first sequence to align.
        y (str): The second sequence to align.
        c (Callable[[str, str], float]): A function that takes two characters and returns a score for matching them.
        delta (float): The penalty for inserting or deleting a character in the alignment.

    Returns:
        Tuple[List[Tuple[str, str]], float]: A tuple containing the optimal alignment as a list of pairs of characters,
            and the score of the optimal alignment.

    """
    m, n = len(x), len(y)
    # rows are including element j, cols are including element i
    A = [[0] * (n + 1) for _ in range(m + 1)]
    # Store the alignment path for each cell
    paths = [[[] for _ in range(n + 1)] for _ in range(m + 1)]

    # initialize dp array for base case
    # of not adding up to the i'th or j'th value
    for i in range(1, m + 1):
        A[i][0] = i * delta

    for j in range(1, n + 1):
        A[0][j] = j * delta

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            match = c(x[i - 1], y[j - 1]) + A[i - 1][j - 1]
            skipX = delta + A[i - 1][j]
            skipY = delta + A[i][j - 1]

            A[i][j] = min(match, skipX, skipY)

            # add to inclusion pairs if match
            # otherwise we have to add a "space" in x or y
            if A[i][j] == match:
                paths[i][j] = paths[i - 1][j - 1] + [(i, j)]
            elif A[i][j] == skipX:
                paths[i][j] = paths[i - 1][j]
            else:  # insert,
                paths[i][j] = paths[i][j - 1]

    return (paths[m][n], A[m][n])


def space_efficient_alignment(
    x: str, y: str, c: Callable[[str, str], float], delta: float
) -> List[float]:
    """Helper function for Hirschberg's algorithm. It is used to efficiently align two sequences
    of similar length. The algorithm works by building a 2D matrix of scores, where each cell in the matrix represents
    the optimal alignment score for the subsequences ending at the corresponding positions in the input sequences.

    Args:
        x (str): The first sequence to align.
        y (str): The second sequence to align.
        c (Callable[[str, str], float]): A function that takes two characters and returns a score for matching them.
        delta (float): The penalty for inserting or deleting a character in the alignment.

    Returns:
        List[float]: A list of scores for the optimal alignment.

    """
    n = len(y)
    m = len(x)
    B = [[0] * 2 for _ in range(m + 1)]
    for i in range(m + 1):
        B[i][0] = i * delta

    for j in range(1, n + 1):
        B[0][1] = j * delta
        for i in range(1, m + 1):
            match = c(x[i - 1], y[j - 1]) + B[i - 1][0]
            skipX = delta + B[i - 1][1]
            skipY = delta + B[i][0]

            B[i][1] = min(match, skipX, skipY)

        for i in range(m + 1):
            B[i][0] = B[i][1]

    return [B[i][1] for i in range(m + 1)]


def sequence_align_fast(
    x: str, y: str, c: Callable[[str, str], float], delta: float
) -> Tuple[List[Tuple[str, str]], float]:
    """Main part of Hirschberg's algorithm, a divide and conquer dynamic programming algorithm.
    It is used to efficiently align two sequences of similar length.
    The algorithm works by building a 2D matrix of scores, where each cell in the matrix represents
    the optimal alignment score for the subsequences ending at the corresponding positions in the input sequences.

    Args:
        x (str): The first sequence to align.
        y (str): The second sequence to align.
        c (Callable[[str, str], float]): A function that takes two characters and returns a score for matching them.
        delta (float): The penalty for inserting or deleting a character in the alignment.

    Returns:
        Tuple[List[Tuple[str, str]], float]: A tuple containing the optimal alignment paths and the alignment score.

    """
    m = len(x)
    n = len(y)

    if m == 0:
        return n * delta
    if n == 0:
        return m * delta

    if m <= 2 or n <= 2:
        return sequence_align_slow(x, y, c, delta)

    mid = n // 2
    f = space_efficient_alignment(x, y[:mid], c, delta)
    g = space_efficient_alignment(x[::-1], y[mid:][::-1], c, delta)

    # q = index minimizing f(q,n/2)+g(q,n/2)
    q = min(range(m + 1), key=lambda i: f[i] + g[m - i])
    left_path, left_score = sequence_align_fast(x[:q], y[:mid], c, delta)
    right_path, right_score = sequence_align_fast(x[q:], y[mid:], c, delta)

    # Adjust indices in right_path
    right_path = [(i + q, j + mid) for i, j in right_path]

    return left_path + right_path, left_score + right_score
