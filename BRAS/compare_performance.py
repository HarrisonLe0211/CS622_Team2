import random
import timeit
import sortedcontainers
import matplotlib.pyplot as plt

# Skip List Implementation (Same as before)
class Node:
    def __init__(self, value=None, level=0):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.header = Node(None, self.MAX_LEVEL)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL - 1:
            lvl += 1
        return lvl

    def insert(self, value):
        update = [None] * (self.MAX_LEVEL)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl

        new_node = Node(value, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, value):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.value == value:
            return True
        return False

    def delete(self, value):
        update = [None] * (self.MAX_LEVEL)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]
        if current and current.value == value:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1

# Treap Implementation (Same as before)
class TreapNode:
    def __init__(self, key, priority):
        self.key = key
        self.priority = priority
        self.left = None
        self.right = None

class Treap:
    def rotate_right(self, root):
        L = root.left
        root.left = L.right
        L.right = root
        return L

    def rotate_left(self, root):
        R = root.right
        root.right = R.left
        R.left = root
        return R

    def insert(self, root, key, priority):
        if root is None:
            return TreapNode(key, priority)

        if key < root.key:
            root.left = self.insert(root.left, key, priority)
            if root.left and root.left.priority > root.priority:
                root = self.rotate_right(root)
        else:
            root.right = self.insert(root.right, key, priority)
            if root.right and root.right.priority > root.priority:
                root = self.rotate_left(root)
        return root

    def search(self, root, key):
        if root is None:
            return False
        if root.key == key:
            return True
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def delete(self, root, key):
        if root is None:
            return None
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            if root.left.priority > root.right.priority:
                root = self.rotate_right(root)
                root.right = self.delete(root.right, key)
            else:
                root = self.rotate_left(root)
                root.left = self.delete(root.left, key)
        return root

# Benchmark function extended for search and delete
def benchmark_operations(structure, operation, num_elements, elements):
    times = []

    for _ in range(10):  # Run 10 trials
        start = timeit.default_timer()

        for element in elements:
            if operation == "insert":
                if isinstance(structure, SkipList):
                    structure.insert(element)
                elif isinstance(structure, Treap):
                    root = None
                    structure.insert(root, element, random.randint(1, num_elements))
                else:  # Red-Black Tree (SortedDict)
                    structure[element] = None
            elif operation == "search":
                if isinstance(structure, SkipList):
                    structure.search(element)
                elif isinstance(structure, Treap):
                    root = None
                    structure.search(root, element)
                else:  # Red-Black Tree (SortedDict)
                    _ = element in structure
            elif operation == "delete":
                if isinstance(structure, SkipList):
                    structure.delete(element)
                elif isinstance(structure, Treap):
                    root = None
                    structure.delete(root, element)
                else:  # Red-Black Tree (SortedDict)
                    try:
                        del structure[element]
                    except KeyError:
                        pass  # Ignore if element is not present

        end = timeit.default_timer()
        times.append(end - start)

    return sum(times) / len(times)  # Average time over 10 trials

# Performance analysis for insert, search, and delete
def performance_analysis():
    num_elements = 1000
    skiplist = SkipList()
    treap = Treap()
    rbtree = sortedcontainers.SortedDict()

    elements = random.sample(range(1, num_elements * 10), num_elements)

    # Measure insert time
    skiplist_insert_time = benchmark_operations(skiplist, "insert", num_elements, elements)
    treap_insert_time = benchmark_operations(treap, "insert", num_elements, elements)
    rbtree_insert_time = benchmark_operations(rbtree, "insert", num_elements, elements)

    # Measure search time
    skiplist_search_time = benchmark_operations(skiplist, "search", num_elements, elements)
    treap_search_time = benchmark_operations(treap, "search", num_elements, elements)
    rbtree_search_time = benchmark_operations(rbtree, "search", num_elements, elements)

    # Measure delete time
    skiplist_delete_time = benchmark_operations(skiplist, "delete", num_elements, elements)
    treap_delete_time = benchmark_operations(treap, "delete", num_elements, elements)
    rbtree_delete_time = benchmark_operations(rbtree, "delete", num_elements, elements)

    # Print results
    print(f"Skip List Insert Time: {skiplist_insert_time:.6f} seconds")
    print(f"Treap Insert Time: {treap_insert_time:.6f} seconds")
    print(f"Red-Black Tree (SortedDict) Insert Time: {rbtree_insert_time:.6f} seconds")

    print(f"Skip List Search Time: {skiplist_search_time:.6f} seconds")
    print(f"Treap Search Time: {treap_search_time:.6f} seconds")
    print(f"Red-Black Tree (SortedDict) Search Time: {rbtree_search_time:.6f} seconds")

    print(f"Skip List Delete Time: {skiplist_delete_time:.6f} seconds")
    print(f"Treap Delete Time: {treap_delete_time:.6f} seconds")
    print(f"Red-Black Tree (SortedDict) Delete Time: {rbtree_delete_time:.6f} seconds")

    # Plot the results
    operations = ["Insert", "Search", "Delete"]
    skiplist_times = [skiplist_insert_time, skiplist_search_time, skiplist_delete_time]
    treap_times = [treap_insert_time, treap_search_time, treap_delete_time]
    rbtree_times = [rbtree_insert_time, rbtree_search_time, rbtree_delete_time]

    fig, ax = plt.subplots()
    index = range(len(operations))
    bar_width = 0.2

    ax.bar([i - bar_width for i in index], skiplist_times, bar_width, label="Skip List")
    ax.bar(index, treap_times, bar_width, label="Treap")
    ax.bar([i + bar_width for i in index], rbtree_times, bar_width, label="Red-Black Tree")

    ax.set_xlabel("Operation")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Performance Comparison")
    ax.set_xticks(index)
    ax.set_xticklabels(operations)
    ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_analysis()