# Useful Data Structures

A comprehensive collection of essential computer science data structures and algorithms implemented in Python and C++. This repository serves as both a learning resource and a reference implementation for developers looking to understand or implement these fundamental building blocks of software engineering.

## Overview

This repository contains carefully crafted implementations of classic data structures with a focus on:

- Clean, well-documented code
- Type safety (using Python's typing system)
- Efficient implementations
- Practical usage examples

You can install the package locally by running
```bash
cd python
python3 -m pip install -Ue .
```

## Current Implementations

### Data Structures

#### Python
- Binary Search Tree (BST)
- Count-Min Sketch
- Disjoint Set (Union-Find)
- Fenwick Tree (Binary Indexed Tree)
- Fibonacci Heap
- Huffman Encoding
- LFU Cache (Least Frequently Used)
- LRU Cache (Least Recently Used)
- Max Stack
- Multi-Level Cache
- Open Addressing Hash Map
- Rolling Analytics
- Rope
- Skip List
- Treap
- Trie

#### C++
- Binary Search Tree (BST)
- Red-Black Tree
- Hash Map

### Algorithms
- Breadth-First Search
- Kruskal's Algorithm
- Knapsack
- Selection Algorithm
- Topological Sort

## Coming in Next Release

### New Data Structures
- Segment Tree
- Vector Implementation (C++)
- Double-Ended Heap

### New Algorithms
- 0-1 BFS
- Dynamic Programming Collection
- Selection Algorithm Improvements

### Infrastructure
- Comprehensive Test Suite
- Package Release
- Performance Benchmarking
- Extended Documentation

## Usage

Each data structure and algorithm is self-contained and can be used independently. The implementations focus on being both educational and production-ready, with clear documentation explaining the underlying concepts and usage patterns.

## Contributing

Contributions are welcome! Whether it's:
- Adding new data structures
- Improving existing implementations
- Adding test cases
- Enhancing documentation
- Fixing bugs

Please feel free to submit pull requests or open issues for discussion. Before committing, ensure that the python project passes linting checks by running `pre-commit run --all`. Unittests can be ran through `python3 -m unittest discover -s tests -p "*.py"`. These will be automatically checked as well through Github Actions.

<!-- ## License

[] -->