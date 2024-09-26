import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static

# Set the backend URL
BACKEND_URL = "http://localhost:8000"  # Adjust this if your backend is hosted elsewhere

st.set_page_config(page_title="Dating App Dashboard", page_icon=":heart:", layout="wide")

st.title("Dating App")

def make_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{BACKEND_URL}{endpoint}", **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Create two columns for the main layout
col1, col2 = st.columns(2)

with col1:
    st.header("Fetch and Store Users")
    num_users = st.number_input("Number of users to fetch", min_value=1, max_value=100, value=10)
    if st.button("Fetch Users"):
        result = make_request("POST", f"/fetch_users/?num_users={int(num_users)}")
        if result:
            st.success(result["message"])
            st.info(f"Run ID: {result['run_id']}")

    st.header("Get Random User")
    if st.button("Get Random User"):
        user = make_request("GET", "/random_user/")
        if user:
            st.write(f"Name: {user['first_name']} {user['last_name']}")
            st.write(f"Email: {user['email']}")
            st.write(f"Gender: {user['gender']}")
            st.write(f"UID: {user['uid']}")
            st.write(f"Ingestion Date: {user['datetime']}")
            m = folium.Map(location=[user['latitude'], user['longitude']], zoom_start=10)
            folium.Marker(
                [user['latitude'], user['longitude']],
                popup=f"{user['first_name']} {user['last_name']}",
                tooltip=user['email']
            ).add_to(m)
            folium_static(m)

    st.header("Get Random Username")
    if st.button("Generate Random Username"):
        username = make_request("GET", "/random_username/")
        if username:
            st.success(f"Random Username: {username}")

with col2:
    st.header("Find Nearest Users")
    email = st.text_input("Enter user email")
    x = st.number_input("Number of nearest users to find", min_value=1, max_value=10, value=5)
    if st.button("Find Nearest Users"):
        if not email or '@' not in email:
            st.error("Please enter a valid email address")
        else:
            users = make_request("GET", "/nearest_users/", params={"email": email, "x": x})
            if users:
                # Create a Folium map centered on the first user
                m = folium.Map(location=[users[0]['latitude'], users[0]['longitude']], zoom_start=10)
                
                for user in users:
                    st.write(f"Name: {user['first_name']} {user['last_name']}, Email: {user['email']}")
                    folium.Marker(
                        [user['latitude'], user['longitude']],
                        popup=f"{user['first_name']} {user['last_name']}",
                        tooltip=user['email']
                    ).add_to(m)
                
                # Display the map
                folium_static(m)

st.sidebar.info("This application interacts with a FastAPI backend to manage random user data.")

class UserManager:
    @staticmethod
    def fetch_and_store_users(num_users):
        result = make_request("POST", "/users/", json={"num_users": num_users})
        if result:
            st.success(result["message"])
            st.info(f"Run ID: {result['run_id']}")

    @staticmethod
    def get_random_user():
        user = make_request("GET", "/random_user/")
        if user:
            st.write(f"Name: {user['first_name']} {user['last_name']}")
            st.write(f"Email: {user['email']}")
            st.write(f"Gender: {user['gender']}")
            st.write(f"UID: {user['uid']}")
            st.write(f"Ingestion Date: {user['datetime']}")
            m = folium.Map(location=[user['latitude'], user['longitude']], zoom_start=10)
            folium.Marker(
                [user['latitude'], user['longitude']],
                popup=f"{user['first_name']} {user['last_name']}",
                tooltip=user['email']
            ).add_to(m)
            folium_static(m)

    @staticmethod
    def get_random_username():
        username = make_request("GET", "/random_username/")
        if username:
            st.success(f"Random Username: {username}")

    @staticmethod
    def find_nearest_users(email, x):
        if not email or '@' not in email:
            st.error("Please enter a valid email address")
        else:
            users = make_request("GET", "/nearest_users/", params={"email": email, "x": x})
            if users:
                m = folium.Map(location=[users[0]['latitude'], users[0]['longitude']], zoom_start=10)
                
                for user in users:
                    st.write(f"Name: {user['first_name']} {user['last_name']}, Email: {user['email']}")
                    folium.Marker(
                        [user['latitude'], user['longitude']],
                        popup=f"{user['first_name']} {user['last_name']}",
                        tooltip=user['email']
                    ).add_to(m)
                
                folium_static(m)


class UserAnalytics:
    @staticmethod
    def display_user_insights():
        user_data = make_request("GET", "/user_insights/")
        if user_data is not None:
            st.subheader("User Insights Dashboard")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Users", user_data['total_users'])
            with col2:
                st.metric("Active Users", user_data['active_users'], 
                          delta=user_data['active_users_change'])
            with col3:
                st.metric("New Users (Last 7 days)", user_data['new_users_week'])
            
            st.plotly_chart(create_user_growth_chart(user_data['user_growth']))
            
            st.subheader("User Demographics")
            age_col, country_col = st.columns(2)
            with age_col:
                st.bar_chart(user_data['age_distribution'])
            with country_col:
                st.map(user_data['user_locations'])

def create_user_growth_chart(growth_data):
    # Assume this function creates a Plotly line chart of user growth over time
    # Implementation details omitted for brevity
    pass















                    