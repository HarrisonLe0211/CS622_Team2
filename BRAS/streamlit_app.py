import streamlit as st
import pandas as pd
import time
from treap_structure import Treap

treap = Treap()


def search_by_type(select, type):
    start_time = time.time()
    st.session_state.rooms = treap.search_by_name(treap.root, select, type)
    end_time = time.time()
    runtime = end_time - start_time
    st.toast(f"Operation Run Time: {runtime:.6f}")


def display_all_rooms():
    st.session_state.rooms = treap.get_all_rooms(treap.root)


def room_status(value):
    return {
        value == "Available": f"background-color: green",
        value == "Occupy": f"background-color: red",
    }.get(True, None)


@st.fragment
def display_table():

    rooms = list()

    for room in st.session_state.rooms:
        rooms.append(
            {
                "Hotel Name": room.hotel_id,
                "Hotel Room": room.key,
                "Firstname": room.firstname,
                "Lastname": room.lastname,
                "ID Card": room.id_card,
                "Date of Birth": room.dob,
                "Room Type": room.room_type,
                "Priority": room.priority,
                "Status": room.status,
            }
        )

    df = pd.DataFrame(
        rooms,
        columns=(
            "Hotel Name",
            "Hotel Room",
            "Firstname",
            "Lastname",
            "ID Card",
            "Date of Birth",
            "Room Type",
            "Priority",
            "Status",
        ),
    )
    st.dataframe(
        df.style.map(room_status),
        use_container_width=True,
        hide_index=True,
    )
    st.button("Reload")


# Creating Treap and adding rooms for 3 hotels
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
        row.priority,
    )

time.sleep(2)  # 2 Seconds Loading
success = st.success("Done!")  # Success Loading Message


display_all_rooms()  # Get All Rooms Data
display_table()  # Display Rooms Data

with st.sidebar:
    with st.form("search_form"):
        st.title("Search")

        search_value = st.text_input("Search", placeholder="Enter Search Value")
        search_type = st.radio(
            "Search Type",
            options=[
                "firstname",
                "lastname",
                "id_card",
                "priority",
                "room_type",
                "status",
            ],
        )
        submitted = st.form_submit_button(label="Submit")
        if submitted:
            search_by_type(search_value, search_type)
            search_success = st.success(f"Success {search_value}")
            time.sleep(1)
            search_success.empty()

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
        priority = st.number_input(
            "Priority",
            value=None,
            placeholder="Treap Priority",
            min_value=1,
            max_value=100,
        )

        submitted = st.form_submit_button(label="Submit")

        if submitted:
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
            )
            if result:
                display_all_rooms()  # Get All Rooms Data
                st.success("Insert Successfully")

    with st.form("update_form"):
        st.title("Update")
        first_name = st.text_input(
            "First Name", placeholder="Enter Customer First Name"
        )
        last_name = st.text_input("Last Name", placeholder="Enter Customer Last Name")
        id_card = st.text_input("ID Card", placeholder="Enter Customer ID Card")
        dob = st.date_input("Date of Birth", format="MM.DD.YYYY", value=None)
        room_s = st.radio("Room Status", options=["Available", "Occupy"])
        submitted = st.form_submit_button(label="Submit")

        if submitted:
            result = treap.update(
                treap.root,
                key,
                first_name,
                last_name,
                dob,
                id_card,
                room_s,
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
            st.toast(f"Operation Run Time: {runtime:.6f}")
            if result:
                display_all_rooms()  # Get All Rooms Data
                delete_success = st.success(f"Delete Hotel Room {key} Successfully")
                time.sleep(1)
                delete_success.empty()


time.sleep(1)  # 1 Seconds before closing succcess message
success.empty()  # Close succes message
