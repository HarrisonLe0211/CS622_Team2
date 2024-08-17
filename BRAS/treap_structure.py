import random

class TreapNode:
    def __init__(self, key, room_type, hotel_id, firstname, lastname, dob, id_card,status,):
        self.key = key  # room number
        self.room_type = room_type
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.id_card = id_card
        self.hotel_id = hotel_id
        self.status = status
        self.priority = {room_type == "VIP": 100, room_type == 'Large': 70}.get(True, 40)
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

    def insert(self, node, key, room_type, hotel_id, firstname, lastname, dob, id_card, status):
        if node is None:
            return TreapNode(key, room_type, hotel_id, firstname, lastname, dob, id_card, status)

        if key < node.key:
            node.left = self.insert(node.left, key, room_type, hotel_id, firstname, lastname, dob, id_card, status)
            if node.left.priority > node.priority:
                node = self.rotate_right(node)
        else:
            node.right = self.insert(node.right, key, room_type, hotel_id, firstname, lastname, dob, id_card, status)
            if node.right.priority > node.priority:
                node = self.rotate_left(node)
        return node

    def search_by_name(self, node, name_key, search_type):
        if node is None:
            return []

        matching_rooms = []

        if search_type == 'room_type' and node.room_type == name_key:
            matching_rooms.append(node)
        elif search_type == 'status' and node.status == name_key:
            matching_rooms.append(node)
        elif search_type == 'firstname' and node.firstname == name_key:
            matching_rooms.append(node)
        elif search_type == 'lastname' and node.lastname == name_key:
            matching_rooms.append(node)
        elif search_type == 'id_card' and node.id_card == name_key:
            matching_rooms.append(node)
        elif search_type == 'dob' and node.dob == name_key:
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

    def get_all_rooms(self, node):
        rooms = []
        if node:
            rooms.extend(self.get_all_rooms(node.left))
            rooms.append(node)
            rooms.extend(self.get_all_rooms(node.right))
        return rooms