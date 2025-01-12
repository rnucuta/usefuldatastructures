import math
import time
import random
from typing import List


def bin_list_to_int(x: List[int]) -> int:
    """Helper function to convert list of bits to an integer"""
    x_int = 0
    for bit in x:
        x_int = (x_int << 1) | bit
    return x_int


def int_to_bin_list(x: int) -> List[int]:
    """Helper function to convert integer to a list of bits"""
    y = [int(x) for x in bin(x)[2:]]
    return y


def bin_list_addition(x: List[int], y: List[int]) -> List[int]:
    """Helper function/carry adder implementation to assist in addition
    make it O(n) instead of inverting array to int back to array
    (which is still O(n))
    """
    longer = x
    shorter = y
    if len(y) > len(x):
        longer = y
        shorter = x

    carry = 0

    result: List[int] = []

    i = len(longer) - 1
    j = len(shorter) - 1

    while i >= 0 or j >= 0 or carry:
        b_l = longer[i] if i >= 0 else 0
        b_s = shorter[j] if j >= 0 else 0

        total = b_l + b_s + carry
        carry = total // 2
        result.append(total % 2)
        i -= 1
        j -= 1

    return result[::-1]


def reference_multiply(x: List[int], y: List[int]) -> int:
    """Grade school multiplication. Of course, multiplication is
    not implemented like this, and is much faster in hardware.
    """
    result = 0

    for i in range(len(x)):
        for j in range(len(y)):
            result += (x[i] * y[j]) << (len(x) - i - 1 + len(y) - j - 1)

    return result


# TODO: write detailed explanatino of algorithm
def karatsuba(x: List[int], y: List[int]) -> int:
    """Fast multiplication implementation which gives O(n^1.585)"""
    # assumption: comes as list of binary numbers
    if len(x) == 1 or len(y) == 1:
        return bin_list_to_int(x) * bin_list_to_int(y)
    n = max(len(x), len(y))

    # make same len
    x = [0] * (n - len(x)) + x
    y = [0] * (n - len(y)) + y

    # divide and conquer
    m = n // 2
    m_p = (n + 1) // 2
    x1 = x[:m]
    x0 = x[m:]
    y1 = y[:m]
    y0 = y[m:]
    # p = karatsuba(int_to_bin_list(bin_list_to_int(x1)+bin_list_to_int(x0)), int_to_bin_list(bin_list_to_int(y1)+bin_list_to_int(y0)))
    p = karatsuba(bin_list_addition(x1, x0), bin_list_addition(y1, y0))
    x1y1 = karatsuba(x1, y1)
    x0y0 = karatsuba(x0, y0)
    return (x1y1 << (2 * m_p)) + ((p - x1y1 - x0y0) << m_p) + x0y0


def forward_fft(P: List[int]) -> List[float]:
    """Forward fft helper function: reference: https://www.youtube.com/watch?v=h7apO7q16V0"""
    n = len(P)
    if n == 1:
        return P
    # omega = math.exp((2j*math.pi)/n)
    # eix=cos(x)+isin(x)
    angle = 2 * math.pi / n
    factor = [complex(math.cos(angle * k), math.sin(angle * k)) for k in range(n // 2)]

    P_e = P[::2]
    P_0 = P[1::2]

    y_e = forward_fft(P_e)
    y_0 = forward_fft(P_0)

    y = [0] * n
    for i in range(n // 2):
        y[i] = y_e[i] + factor[i] * y_0[i]
        y[i + n // 2] = y_e[i] - factor[i] * y_0[i]

    return y


def inverse_fft(P: List[int]) -> List[float]:
    """Inverse fft helper function: reference: https://www.youtube.com/watch?v=h7apO7q16V0"""
    n = len(P)
    if n == 1:
        return P
    # omega = (1/n)*math.exp(-(2j*math.pi)/n)
    angle = -2 * math.pi / n
    factor = [complex(math.cos(angle * k), math.sin(angle * k)) for k in range(n // 2)]

    P_e = P[::2]
    P_0 = P[1::2]

    y_e = inverse_fft(P_e)
    y_0 = inverse_fft(P_0)

    y = [0] * n
    for i in range(n // 2):
        y[i] = y_e[i] + factor[i] * y_0[i]
        y[i + n // 2] = y_e[i] - factor[i] * y_0[i]

    return y


def fft(x: List[int], y: List[int]) -> List[int]:
    """Fast fourier transform for fast integer multiplication. O(n log n)"""
    x_coef = x[::-1]
    y_coef = y[::-1]

    # n must be greater than (len(x)-1)+(len(y)-1)+1
    n = 1
    while n < len(x) + len(y):
        n *= 2

    # make same len
    x_coef += [0] * (n - len(x))
    y_coef += [0] * (n - len(y))

    # convert coefficeints to fft values
    fft_a = forward_fft(x_coef)
    fft_b = forward_fft(y_coef)

    # multiply fft values
    product = [fft_a[i] * fft_b[i] for i in range(n)]

    # convert values back to coefficients, removing
    # imaginary values and scale coefficents
    coefficients = [round(c.real / n) for c in inverse_fft(product)]

    # perform carry operations
    # result is in little endian order
    result = 0
    carry = 0
    for i in range(len(coefficients)):
        total = coefficients[i] + carry
        bit = total % 2
        carry = total // 2
        result += bit * (1 << i)

    # include any remaining carry
    i = len(coefficients)
    while carry > 0:
        bit = carry % 2
        carry = carry // 2
        result += bit * (1 << i)
        i += 1

    return result


if __name__ == "__main__":
    # Demo script to show how much faster fft is versus "grade school" multiplication
    for i in [5, 10, 50, 100, 200, 500, 1000, 2000, 3000, 4000]:
        for j in range(5):
            test = [random.randrange(0, 2, 1) for k in range(i)]
            s = time.time()
            reference_multiply(test, test)
            end = time.time() - s
            print("reference n: {} t: {}".format(i, end))
            s = time.time()
            karatsuba(test, test)
            end = time.time() - s
            print("karatsuba n: {} t: {}".format(i, end))
            s = time.time()
            fft(test, test)
            end = time.time() - s
            print("fft n: {} t: {}".format(i, end))
