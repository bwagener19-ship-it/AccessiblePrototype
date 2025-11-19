from collections import deque, defaultdict
import heapq

class Stack:
    def __init__(self):
        self._data = []
    def push(self, item): self._data.append(item)
    def pop(self):
        if not self.is_empty(): return self._data.pop()
        raise IndexError("pop from empty stack")
    def peek(self):
        if not self.is_empty(): return self._data[-1]
        raise IndexError("peek from empty stack")
    def is_empty(self): return len(self._data) == 0

class Queue:
    def __init__(self):
        self._data = deque()
    def enqueue(self, item): self._data.append(item)
    def dequeue(self):
        if not self.is_empty(): return self._data.popleft()
        raise IndexError("dequeue from empty queue")
    def is_empty(self): return len(self._data) == 0

class HashTable:
    def __init__(self):
        self._table = defaultdict(list)
    def _hash(self, key): return hash(key) % 100
    def set(self, key, value): self.insert(key, value)
    def insert(self, key, value):
        h = self._hash(key)
        for i, (k, v) in enumerate(self._table[h]):
            if k == key:
                self._table[h][i] = (key, value); return
        self._table[h].append((key, value))
    def get(self, key):
        h = self._hash(key)
        for k, v in self._table[h]:
            if k == key: return v
        return None

class PriorityQueue:
    def __init__(self): self.queue = []
    def push(self, priority, item): heapq.heappush(self.queue, (priority, item))
    def pop(self):
        if self.queue: return heapq.heappop(self.queue)[1]
        return None

class Node:
    def __init__(self, key, value=None):
        self.key = key; self.value = value; self.left = None; self.right = None

class BinarySearchTree:
    def __init__(self): self.root = None
    def insert(self, key, value=None): self.root = self._insert(self.root, key, value)
    def _insert(self, node, key, value):
        if node is None: return Node(key, value)
        if key < node.key: node.left = self._insert(node.left, key, value)
        elif key > node.key: node.right = self._insert(node.right, key, value)
        else: node.value = value
        return node
    def find(self, key): return self._find(self.root, key)
    def _find(self, node, key):
        if node is None: return None
        if key == node.key: return node.value
        elif key < node.key: return self._find(node.left, key)
        else: return self._find(node.right, key)
    def search(self, key): return self.find(key)
    def inorder(self):
        result = []
        def _inorder(node):
            if not node: return
            _inorder(node.left); result.append((node.key, node.value)); _inorder(node.right)
        _inorder(self.root); return result

class Graph:
    def __init__(self): self.edges = defaultdict(list)
    def add_edge(self, u, v, w): self.edges[u].append((v, w))
    def shortest_path(self, start, target):
        pq = [(0, start, [])]; visited = set()
        while pq:
            dist, node, path = heapq.heappop(pq)
            if node in visited: continue
            visited.add(node)
            new_path = path + [node]
            if node == target: return new_path, dist
            for neighbor, weight in self.edges.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (dist + weight, neighbor, new_path))
        return None, float("inf")

# KMP
def kmp_search(text, pattern):
    if not pattern: return 0
    lps = [0] * len(pattern); length = 0; i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1; lps[i] = length; i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0; i += 1
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1; j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def dijkstra_shortest_path(edges, start, target):
    pq = [(0, start, [])]
    visited = set()
    while pq:
        dist, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        new_path = path + [node]
        if node == target:
            return new_path, dist
        for nbr, w in edges.get(node, []):
            if nbr not in visited:
                heapq.heappush(pq, (dist + w, nbr, new_path))
    return None, float('inf')


def max_overlap_kmp(a: str, b: str) -> int:
    minlen = min(len(a), len(b))
    combined = b + '$' + a[-minlen:]
    lps = [0] * len(combined)

    for i in range(1, len(combined)):
        j = lps[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = lps[j - 1]
        if combined[i] == combined[j]:
            j += 1
        lps[i] = j
    return min(lps[-1], minlen)


def greedy_assemble_fragments(fragments):
    frags = fragments[:]
    while len(frags) > 1:
        max_ol = -1
        pair = (0, 1)
        merged = None
        for i in range(len(frags)):
            for j in range(len(frags)):
                if i == j:
                    continue
                a, b = frags[i], frags[j]
                ol = max_overlap_kmp(a, b)
                if ol > max_ol:
                    max_ol = ol
                    pair = (i, j)
                    merged = a + b[ol:]
        if max_ol <= 0:
            frags[0] = frags[0] + frags.pop()
        else:
            i, j = pair
            if i < j:
                frags.pop(j)
                frags.pop(i)
            else:
                frags.pop(i)
                frags.pop(j)
            frags.append(merged)
    return frags[0] if frags else ''


product_name_list = ["Apples", "Bananas", "Carrots"]
