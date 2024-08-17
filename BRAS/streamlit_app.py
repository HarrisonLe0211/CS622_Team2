import streamlit as st
import pandas as pd
import time
from treap_structure import Treap

treap = Treap()
def search_by_type(select, type):
    st.session_state.rooms = treap.search_by_name(treap.root, select, type)
    
def display_all_rooms():
    st.session_state.rooms = treap.get_all_rooms(treap.root)

def room_status(value):
    return {value == "Available": f"background-color: green", value == 'Occupy': f"background-color: red"}.get(True, None)

def dispaly_table():
    
    rooms = list()

    for room in st.session_state.rooms:
        rooms.append({"Hotel Name": room.hotel_id,
                    "Firstname": room.firstname, 
                    "Lastname": room.lastname, 
                    "ID Card": room.id_card, 
                    "Date of Birth": room.dob, 
                    "Room Type": room.room_type, 
                    "Priority": room.priority, 
                    "Status": room.status})

    df = pd.DataFrame(rooms, columns=( 'Hotel Name', 
                                    "Firstname", 
                                    "Lastname", 
                                    "ID Card", 
                                    "Date of Birth",
                                    'Room Type', 
                                    'Priority', 
                                    'Status'))
    st.dataframe(df.style.map(room_status), use_container_width=True, hide_index=True,)


# Creating Treap and adding rooms for 3 hotels
st.spinner("Loading...")
rooms_data = pd.read_csv("mock_data.csv")
for row in rooms_data.itertuples():
    treap.root = treap.insert(treap.root, 
                            row.key, 
                            row.room_type, 
                            row.hotel_id, 
                            row.firstname, 
                            row.lastname, 
                            row.dob, 
                            row.id_card, 
                            row.room_status)

time.sleep(2) # 2 Seconds Loading
success = st.success("Done!") # Success Loading Message

display_all_rooms() # Get All Rooms Data
dispaly_table() # Display Rooms Data 

time.sleep(1) # 1 Seconds before closing succcess message
success.empty() # Close succes message
