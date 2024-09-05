import streamlit as st
import pandas as pd
import time
from treap_structure import Treap
import graphviz

treap = Treap()

def visualize_treap(treap_root):
    """
    Creates a Graphviz representation of the Treap and displays it in Streamlit.

    Args:
        treap_root: The root node of the Treap.
    """
    graph = graphviz.Digraph()
    graph.attr('node', shape='record')

    def add_node(node, parent_id=None):
        node_id = str(node.key)
        graph.node(node_id, label=f"{node.key}|{node.priority}")
        if parent_id:
            graph.edge(parent_id, node_id)
        if node.left:
            add_node(node.left, node_id)
        if node.right:
            add_node(node.right, node_id)

    add_node(treap_root)
    graph.render('treap.gv', view=True)

def search_by_type(select, room_type):
    start_time = time.time()
    st.session_state.rooms = treap.search_by_name(treap.root, select, room_type)
    end_time = time.time()
    runtime = end_time - start_time
    st.toast(f"Operation Run Time: {runtime:.6f}s")

def display_all_rooms():
    st.session_state.rooms = treap.get_all_rooms(treap.root)

def room_status(value):
    return {
        value == "Available": f"background-color: green",
        value == "Occupy": f"background-color: red",
    }.get(True, None)

def display_table():
    if 'rooms' not in st.session_state:
        display_all_rooms()

    rooms = []
    for room in st.session_state.rooms:
        rooms.append({
            "Hotel Name": room.hotel_id,
            "Hotel Room": room.key,
            "Firstname": room.firstname,
            "Lastname": room.lastname,
            "ID Card": room.id_card,
            "Date of Birth": room.dob,
            "Room Type": room.room_type,
            "Priority": room.priority,
            "Status": room.status,
        })

    df = pd.DataFrame(rooms, columns=(
        "Hotel Name", "Hotel Room", "Firstname", "Lastname", 
        "ID Card", "Date of Birth", "Room Type", "Priority", "Status"
    ))

    # st.dataframe(df.style.map(room_status), use_container_width=True, hide_index=True)
    st.dataframe(df.style.map(room_status), height=650, hide_index=True)

# Sidebar logic to trigger table refresh
def sidebar():
    with st.sidebar:
        with st.form('search_form'):
            st.title("Search")
            # Initialize session state variables for selected hotel and room type if not already set
            if 'selected_hotel' not in st.session_state:
                st.session_state.selected_hotel = "VIP"
            if 'selected_room_type' not in st.session_state:
                st.session_state.selected_room_type = "room_type"
            
            # Sidebar selection with session state binding
            st.session_state.selected_hotel = st.text_input("Search", placeholder="Enter Search Value")
            st.session_state.selected_room_type = st.radio(
                "Search Type",
                options=[
                    "room_type",
                    "firstname",
                    "lastname",
                    "id_card",
                    "priority",
                    "status",
                ],
            )
            # Apply button for filter changes
            if st.form_submit_button("Search"):
                search_by_type(st.session_state.selected_hotel, st.session_state.selected_room_type)

        with st.form("insert_form"):
            st.title("Insert")
            # Input fields with labels and descriptions
            key = st.text_input("Hotel Room", placeholder="Enter Hotel Room")
            room_type = st.radio("Room Type", options=["VIP", "Small", "Large"])
            hotel_id = st.text_input(
                "Hotel ID or Branch Name", placeholder="Enter Hotel ID or Branch Name"
            )
            first_name = st.text_input(
                "First Name", placeholder="Enter Customer First Name"
            )
            last_name = st.text_input("Last Name", placeholder="Enter Customer Last Name")
            id_card = st.text_input("ID Card", placeholder="Enter Customer ID Card")
            dob = st.date_input("Date of Birth", format="MM.DD.YYYY", value=None)
            room_s = st.radio("Room Status", options=["Available", "Occupy"])
            # priority = st.number_input(
            #     "Priority",
            #     value=None,
            #     placeholder="Treap Priority",
            #     min_value=1,
            #     max_value=150,
            # )

            if st.form_submit_button(label="Submit"):
                result = treap.insert(
                    treap.root,
                    key,
                    room_type,
                    hotel_id,
                    first_name,
                    last_name,
                    dob,
                    id_card,
                    room_s,
                    # priority
                )
                if result:
                    display_all_rooms()  # Get All Rooms Data
                    st.success("Insert Successfully")

        with st.form("delete_form"):
            st.title("Delete")
            key = st.text_input("Hotel Room", placeholder="Enter Hotel Room")
            submitted = st.form_submit_button(label="Submit")
            if submitted:
                start_time = time.time()
                result = treap.deleteNode(treap.root, key)
                end_time = time.time()
                runtime = end_time - start_time
                st.toast(f"Operation Run Time: {runtime:.6f}s")
                if result:
                    display_all_rooms()  # Get All Rooms Data
                    delete_success = st.success(f"Delete Hotel Room {key} Successfully")
                    time.sleep(1)
                    delete_success.empty()

        with st.form("generate_treap"):
            st.title("Treap Structure (Debug)")
            """
            Display the Treap structure (for debugging purposes).
            """
            if st.form_submit_button(label="Visualize Treap"):
                visualize_treap(treap.root)
# Main App
st.spinner("Loading...")
rooms_data = pd.read_csv("mock_data.csv")
for row in rooms_data.itertuples():
    treap.root = treap.insert(
        treap.root,
        row.key,
        row.room_type,
        row.hotel_id,
        row.firstname,
        row.lastname,
        row.dob,
        row.id_card,
        row.room_status,
        # row.priority
    )

sidebar()
display_table()