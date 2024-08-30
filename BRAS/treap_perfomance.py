import random
import time
import pandas as pd
import tracemalloc

# Step 1: Implementing the Treap
class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None
    
    def rotate_right(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        return new_root
    
    def rotate_left(self, root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root
        return new_root
    
    def insert(self, root, key):
        if not root:
            return TreapNode(key)
        
        if key < root.key:
            root.left = self.insert(root.left, key)
            if root.left.priority > root.priority:
                root = self.rotate_right(root)
        else:
            root.right = self.insert(root.right, key)
            if root.right.priority > root.priority:
                root = self.rotate_left(root)
        
        return root
    
    def delete(self, root, key):
        if not root:
            return root
        
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            if root.left.priority > root.right.priority:
                root = self.rotate_right(root)
                root.right = self.delete(root.right, key)
            else:
                root = self.rotate_left(root)
                root.left = self.delete(root.left, key)
        
        return root
    
    def search(self, root, key):
        if not root or root.key == key:
            return root
        
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)
    
    def insert_key(self, key):
        self.root = self.insert(self.root, key)
    
    def delete_key(self, key):
        self.root = self.delete(self.root, key)
    
    def search_key(self, key):
        return self.search(self.root, key)

    def size(self, root):
        if root is None:
            return 0
        return 1 + self.size(root.left) + self.size(root.right)

# Step 2: Measuring Time and Memory Usage
def measure_time_and_memory(treap, operation, key=None):
    start_time = time.time()
    tracemalloc.start()

    if operation == 'insert':
        treap.insert_key(key)
    elif operation == 'delete':
        treap.delete_key(key)
    elif operation == 'search':
        treap.search_key(key)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed_time = time.time() - start_time

    return elapsed_time, peak

def conduct_analysis(num_operations):
    treap = Treap()
    keys = random.sample(range(1, num_operations * 10), num_operations)
    insertion_times = []
    search_times = []
    deletion_times = []
    memory_usages = []

    for key in keys:
        # Measure insertion time and memory usage
        insertion_time, memory_usage = measure_time_and_memory(treap, 'insert', key)
        insertion_times.append(insertion_time)
        memory_usages.append(memory_usage)
        
        # Measure search time and memory usage
        search_time, _ = measure_time_and_memory(treap, 'search', key)
        search_times.append(search_time)
        
    for key in keys:
        # Measure deletion time and memory usage
        deletion_time, _ = measure_time_and_memory(treap, 'delete', key)
        deletion_times.append(deletion_time)

    average_insertion_time = sum(insertion_times) / num_operations
    average_search_time = sum(search_times) / num_operations
    average_deletion_time = sum(deletion_times) / num_operations
    average_memory_usage = sum(memory_usages) / num_operations

    return average_insertion_time, average_search_time, average_deletion_time, average_memory_usage

# Step 3: Running the Analysis

# Let's assume you have already run the conduct_analysis function
# and obtained the following results:
num_operations = 1000
average_insertion_time, average_search_time, average_deletion_time, average_memory_usage = conduct_analysis(num_operations)

# Store the results in a dictionary
results = {
    "Operation": ["Insertion", "Search", "Deletion", "Memory Usage"],
    "Average Time (seconds)": [average_insertion_time, average_search_time, average_deletion_time, None],
    "Memory Usage (KB)": [None, None, None, average_memory_usage / 1024]
}

# Convert the results into a Pandas DataFrame
df_results = pd.DataFrame(results)

# Displaying the results in a table
print("Experimental Results:")
print(df_results.to_string(index=False))