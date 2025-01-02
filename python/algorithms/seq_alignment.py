def sequence_align_slow(x, y, c, delta) -> tuple:
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
            match = c(x[i-1], y[j-1]) + A[i-1][j-1]
            skipX = delta + A[i-1][j]
            skipY = delta + A[i][j-1]
            
            A[i][j] = min(match, skipX, skipY)
            
            # add to inclusion pairs if match
            # otherwise we have to add a "space" in x or y
            if A[i][j] == match:
                paths[i][j] = paths[i-1][j-1] + [(i, j)]
            elif A[i][j] == skipX:
                paths[i][j] = paths[i-1][j]
            else: # insert, 
                paths[i][j] = paths[i][j-1]
    
    return (paths[m][n], A[m][n])


def alignment(x, y, c, delta) -> tuple:
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
            match = c(x[i-1], y[j-1]) + A[i-1][j-1]
            skipX = delta + A[i-1][j]
            skipY = delta + A[i][j-1]
            
            A[i][j] = min(match, skipX, skipY)
            
            # add to inclusion pairs if match
            # otherwise we have to add a "space" in x or y
            if A[i][j] == match:
                paths[i][j] = paths[i-1][j-1] + [(i, j)]
            elif A[i][j] == skipX:
                paths[i][j] = paths[i-1][j]
            else: # insert, 
                paths[i][j] = paths[i][j-1]
    
    return (paths[m][n], A[m][n])

# Hirschberg’s algorithm, 6.7
def space_efficient_alignment(x, y, c, delta) -> list:
    n = len(y)
    m = len(x)
    B = [[0]*2 for _ in range(m + 1)]
    for i in range(m + 1):
        B[i][0] = i * delta

    for j in range(1, n+1):
        B[0][1] = j*delta
        for i in range(1, m+1):
            match = c(x[i-1], y[j-1]) + B[i-1][0]
            skipX = delta + B[i-1][1]
            skipY = delta + B[i][0]

            B[i][1] = min(match, skipX, skipY)

        for i in range(m + 1):
            B[i][0] = B[i][1]

    return [B[i][1] for i in range(m + 1)]

# divide_and_conquer_alignment
def sequence_align_fast(x, y, c, delta) -> tuple:
    m = len(x)
    n = len(y)

    if m == 0:
        return n * delta
    if n == 0:
        return m * delta
    
    if m <= 2 or n <= 2:
        return alignment(x, y, c, delta)
    
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