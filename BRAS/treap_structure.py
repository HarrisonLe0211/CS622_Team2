import random

class TreapNode:
    def __init__(self, key, room_type, hotel_id, status='Free'):
        self.key = key  # room number
        self.room_type = room_type
        self.hotel_id = hotel_id
        self.status = status
        self.priority = random.randint(1, 100)  # heap priority
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        return left_child

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        return right_child

    def insert(self, node, key, room_type, hotel_id):
        if node is None:
            return TreapNode(key, room_type, hotel_id)

        if key < node.key:
            node.left = self.insert(node.left, key, room_type, hotel_id)
            if node.left.priority > node.priority:
                node = self.rotate_right(node)
        else:
            node.right = self.insert(node.right, key, room_type, hotel_id)
            if node.right.priority > node.priority:
                node = self.rotate_left(node)
        return node

    def search_by_name(self, node, name_key, search_type):
        """
        Search by room_type or status and return a list of matching rooms.

        :param node: Current Treap node.
        :param name_key: The key to search for (e.g., 'Small', 'VIP', 'Free').
        :param search_type: The type of search ('room_type' or 'status').
        :return: List of matching rooms.
        """
        if node is None:
            return []

        matching_rooms = []

        if search_type == 'room_type' and node.room_type == name_key:
            matching_rooms.append(node)
        elif search_type == 'status' and node.status == name_key:
            matching_rooms.append(node)

        matching_rooms.extend(self.search_by_name(node.left, name_key, search_type))
        matching_rooms.extend(self.search_by_name(node.right, name_key, search_type))

        return matching_rooms

    def update_status(self, key, status):
        node = self.search(self.root, key)
        if node:
            node.status = status
        else:
            print("Room not found.")

    def in_order_traversal(self, node, result=[]):
        if node:
            self.in_order_traversal(node.left, result)
            result.append(f"Hotel {node.hotel_id} Room {node.key} ({node.room_type}): {node.status}")
            self.in_order_traversal(node.right, result)
        return result

# Creating Treap and adding rooms for 3 hotels
treap = Treap()
room_id = 1
room_types = ['Small', 'Large', 'VIP']

for hotel_id in range(1, 4):
    for room_type, count in zip(room_types, [12, 5, 3]):
        for _ in range(count):
            treap.root = treap.insert(treap.root, room_id, room_type, hotel_id)
            room_id += 1

# Example: Search for all 'Small' rooms across all hotels
small_rooms = treap.search_by_name(treap.root, 'Small', 'room_type')
for room in small_rooms:
    print(f"Hotel {room.hotel_id} Room {room.key} ({room.room_type}): {room.status}")

# Example: Search for all 'Free' rooms across all hotels
free_rooms = treap.search_by_name(treap.root, 'Free', 'status')
for room in free_rooms:
    print(f"Hotel {room.hotel_id} Room {room.key} ({room.room_type}): {room.status}")