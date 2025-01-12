"""Implementation of MapReduce for counting the number of
words in a string. Try running in python3.13 No GIL mode!
"""

import threading
import time
import json
import re
from collections import defaultdict, Counter
from pathlib import Path


def read_file(file_path: str) -> str:
    """Reads a file and returns its content as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file, or None if the file is not found.

    """
    try:
        with open(file_path, "r") as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None


def name_node(text: str, n_threads: int) -> list[str]:
    """Splits the input text into subsets for the specified number of threads.

    Args:
        text (str): The input text to be split.
        n_threads (int): The number of threads to split the text into.

    Returns:
        list[str]: A list of text subsets for each thread.

    """
    words = text.split()
    # finds average length
    avg_len = len(words) / float(n_threads)
    subsets = []
    last = 0.0

    # creates list of len n_threads with split text
    while last < len(words):
        subsets.append(" ".join(words[int(last) : int(last + avg_len)]))
        last += avg_len

    # if there is an uneven split, add the final missed text to the final thread
    if len(words) % n_threads:
        subsets[-1] += " " + " ".join(words[int(last) :])

    return subsets


def map_func(subset: str) -> list[tuple[str, int]]:
    """Maps words in a text subset to key-value pairs.

    Args:
        subset (str): The text subset to be processed.

    Returns:
        list[tuple[str, int]]: A list of tuples containing words and their counts.

    """
    # Find all words in the subset and convert them to lowercase
    words = re.findall(r"\w+", subset.lower())
    # Generate key-value pairs as tuples
    return [(word, 1) for word in words]


def reduce_func(
    lock: threading.Lock,
    reduced_count: list[dict[str, int]],
    kv_pairs: list[tuple[str, int]],
) -> None:
    """Reduces the key-value pairs into a combined count.
    Combine the counts for each word in the subset of text from the kv pairs from map

    Args:
        lock (threading.Lock): A lock to synchronize access to shared data.
        reduced_count (list[dict[str, int]]): The list to store reduced counts.
        kv_pairs (list[tuple[str, int]]): The key-value pairs to be reduced.

    """
    thread_count = defaultdict(int)
    for key, value in kv_pairs:
        thread_count[key] += value
    with lock:
        reduced_count.append(thread_count)


def task_tracker(
    subset: str, reduced_count: list[dict[str, int]], lock: threading.Lock
) -> None:
    """Tracks the task of mapping and reducing for a text subset.
    Combines map and reduce phases into one thread

    Args:
        subset (str): The text subset to be processed.
        reduced_count (list[dict[str, int]]): The list to store reduced counts.
        lock (threading.Lock): A lock to synchronize access to shared data.

    """
    # Map phase
    kv_pairs = map_func(subset)
    # Reduce phase
    reduce_func(lock, reduced_count, kv_pairs)


def combiner_func(reduced_count: list[dict[str, int]]) -> Counter:
    """Combines the reduced counts from all threads into a final count. One thread no matter n threads

    Args:
        reduced_count (list[dict[str, int]]): The list of reduced counts from threads.

    Returns:
        Counter: A Counter object containing the final word counts.

    """
    # iterate through all counters to get one overall coutner
    final_count = Counter()
    for data in reduced_count:
        final_count.update(data)
    return final_count


def thread_splitter(subsets: list[str]) -> list[dict[str, int]]:
    """Splits the work into threads and collects the reduced counts.

    Args:
        subsets (list[str]): The list of text subsets to be processed.

    Returns:
        list[dict[str, int]]: The list of reduced counts from all threads.

    """
    lock = threading.Lock()
    threads = []

    # global var
    reduced_count = []

    # starts all task tracker threads
    for subset in subsets:
        thread = threading.Thread(
            target=task_tracker, args=(subset, reduced_count, lock)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    return reduced_count


if __name__ == "__main__":
    while True:
        # console input
        file_path = input("Enter the path to the data file or press q to quit: ")
        if file_path.lower() == "q":
            break

        if not Path(file_path).is_file():
            print("Invalid file path.")
            continue

        data = read_file(file_path)
        if data is None:
            continue

        try:
            n_threads = int(input("Enter the number of threads to use (N>=1): "))
            if n_threads < 1:
                raise ValueError
        except ValueError:
            print("Invalid number of threads. Please enter a positive integer.")
            continue

        # single thread run
        start_time = time.time()
        subsets = name_node(data, 1)
        reduced_count = thread_splitter(subsets)
        single_results = combiner_func(reduced_count)
        single_threaded_time = time.time() - start_time

        # multi thread run
        start_time = time.time()
        subsets = name_node(data, n_threads)
        reduced_count = thread_splitter(subsets)
        multi_results = combiner_func(reduced_count)
        multi_threaded_time = time.time() - start_time

        # Report times
        print("Single-threaded execution time: {}s".format(single_threaded_time))
        print(
            "Multi-threaded execution time:  {}s with {} threads".format(
                multi_threaded_time, n_threads
            )
        )

        while True:
            # console input to view results
            view_result = input(
                "View results? (s: singlethread, m: multithread, c: continue) "
            )
            if view_result.lower() == "s" or view_result.lower() == "singlethread":
                print(json.dumps(single_results, indent=2))
                print()
            elif view_result.lower() == "m" or view_result.lower() == "multithread":
                print(json.dumps(multi_results, indent=2))
                print()
            elif view_result.lower() == "c" or view_result.lower() == "continue":
                print()
                break
            else:
                print("Invalid input. Please try again.")
