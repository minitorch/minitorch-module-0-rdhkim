"""
Collection of the core mathematical operators used throughout the code base.
"""

import math
from typing import Callable, Iterable

# ## Task 0.1
#
# Implementation of a prelude of elementary functions.


def mul(x: float, y: float) -> float:
    "$f(x, y) = x * y$"
    return x * y


def id(x: float) -> float:
    "$f(x) = x$"
    return x


def add(x: float, y: float) -> float:
    "$f(x, y) = x + y$"
    return x + y


def neg(x: float) -> float:
    "$f(x) = -x$"
    return -x


def lt(x: float, y: float) -> float:
    "$f(x) =$ 1.0 if x is less than y else 0.0"
    if x < y:
        return 1.0
    else:
        return 0.0

def eq(x: float, y: float) -> float:
    "$f(x) =$ 1.0 if x is equal to y else 0.0"
    if x == y:
        return 1.0
    else:
        return 0.0


def max(x: float, y: float) -> float:
    "$f(x) =$ x if x is greater than y else y"
    if x > y:
        return x
    else:
        return y


def is_close(x: float, y: float) -> float:
    "$f(x) = |x - y| < 1e-2$"
    return abs(x-y) < 1e-2


def sigmoid(x: float) -> float:
    r"""
    $f(x) =  \frac{1.0}{(1.0 + e^{-x})}$

    (See https://en.wikipedia.org/wiki/Sigmoid_function )

    Calculate as

    $f(x) =  \frac{1.0}{(1.0 + e^{-x})}$ if x >=0 else $\frac{e^x}{(1.0 + e^{x})}$

    for stability.
    """
    if x >=0 :
        return 1.0 / (1.0 + exp(-x))
    else:
        return exp(x) / (1.0 + exp(x))


def relu(x: float) -> float:
    """
    $f(x) =$ x if x is greater than 0, else 0

    (See https://en.wikipedia.org/wiki/Rectifier_(neural_networks) .)
    """
    if x > 0:
        return x
    else:
        return 0


EPS = 1e-6


def log(x: float) -> float:
    "$f(x) = log(x)$"
    return math.log(x + EPS)


def exp(x: float) -> float:
    "$f(x) = e^{x}$"
    return math.exp(x)


def log_back(x: float, d: float) -> float:
    r"If $f = log$ as above, compute $d \times f'(x)$"
    return d * (1/(x + EPS))


def inv(x: float) -> float:
    "$f(x) = 1/x$"
    return 1/x


def inv_back(x: float, d: float) -> float:
    r"If $f(x) = 1/x$ compute $d \times f'(x)$"
    return -1/(x**2)


def relu_back(x: float, d: float) -> float:
    r"If $f = relu$ compute $d \times f'(x)$"
    if relu(x) > 0:
        return d * (relu(x)/x)
    else:
        return 0


# ## Task 0.3

# Small practice library of elementary higher-order functions.


def map(fn: Callable[[float], float]) -> Callable[[Iterable[float]], Iterable[float]]:
    """
    Higher-order map.

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: Function from one value to one value.

    Returns:
        A function that takes a list, applies `fn` to each element, and returns a
         new list
    """
    def map_fn(arr: list):
        return [fn(item) for item in arr]
    return map_fn


def negList(ls: Iterable[float]) -> Iterable[float]:
    "Use `map` and `neg` to negate each element in `ls`"
    return map(neg)(ls)


def zipWith(
    fn: Callable[[float, float], float]
) -> Callable[[Iterable[float], Iterable[float]], Iterable[float]]:
    """
    Higher-order zipwith (or map2).

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: combine two values

    Returns:
        Function that takes two equally sized lists `ls1` and `ls2`, produce a new list by
         applying fn(x, y) on each pair of elements.

    """
    def zipWithFn(ls1: list, ls2: list):
        return [fn(x, y) for x, y in zip(ls1, ls2)]
    return zipWithFn


def addLists(ls1: Iterable[float], ls2: Iterable[float]) -> Iterable[float]:
    "Add the elements of `ls1` and `ls2` using `zipWith` and `add`"
    return zipWith(add)(ls1, ls2)


def reduce(
    fn: Callable[[float, float], float], start: float
) -> Callable[[Iterable[float]], float]:
    r"""
    Higher-order reduce.

    Args:
        fn: combine two values
        start: start value $x_0$

    Returns:
        Function that takes a list `ls` of elements
         $x_1 \ldots x_n$ and computes the reduction :math:`fn(x_3, fn(x_2,
         fn(x_1, x_0)))`
    """
    def reduceFn(ls):
        if len(ls) == 1:
            return ls[0]
        else:
            return fn(reduceFn(ls[1:]), ls[0])
    return reduceFn


def sum(ls: Iterable[float]) -> float:
    "Sum up a list using `reduce` and `add`."
    if not ls:
        return 0
    else:
        return reduce(add, ls[0])(ls)


def prod(ls: Iterable[float]) -> float:
    "Product of a list using `reduce` and `mul`."
    return reduce(mul, ls[0])(ls)
