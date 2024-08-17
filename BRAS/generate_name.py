import string
from faker import Faker
import random
import streamlit as st

def generate_fake_data_with_faker(num_records):
    fake = Faker()
    data = []
    for _ in range(num_records):
        data.append(f"{fake.first_name()},{fake.last_name()},{''.join(random.choices(string.ascii_letters + string.digits, k=10))},{fake.date_of_birth().strftime("%m/%d/%Y")},")
    return data
fake_data = generate_fake_data_with_faker(23)
st.write(fake_data)