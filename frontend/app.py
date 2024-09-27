import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

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
    def get_user_count():
        count = make_request("GET", "/user_count/")
        if count is not None:
            st.metric("Total Users", count)
            st.bar_chart({"Users": count})

    @staticmethod
    def get_gender_distribution():
        distribution = make_request("GET", "/gender_distribution/")
        if distribution:
            st.write("Gender Distribution:")
            for gender, count in distribution.items():
                st.write(f"{gender}: {count}")
                
    @staticmethod
    def plot_gender_distribution():
        distribution = make_request("GET", "/gender_distribution/")
        if distribution:
            fig, ax = plt.subplots()
            ax.bar(distribution.keys(), distribution.values(), color='skyblue')
            ax.set_title("Gender Distribution")
            ax.set_xlabel("Gender")
            ax.set_ylabel("Count")
            ax.set_facecolor('lightgrey')
            st.pyplot(fig)

class LocationAnalytics:
    @staticmethod
    def get_user_density():
        density = make_request("GET", "/user_density/")
        if density:
            st.write("User Density by Region:")
            for region, count in density.items():
                st.write(f"{region}: {count}")

    @staticmethod
    def plot_user_density():
        density = make_request("GET", "/user_density/")
        if density:
            fig, ax = plt.subplots()
            ax.bar(density.keys(), density.values())
            ax.set_title("User Density by Region")
            ax.set_xlabel("Region")
            ax.set_ylabel("Number of Users")
            plt.xticks(rotation=45)
            st.pyplot(fig)

    @staticmethod
    def display_user_map():
        users = make_request("GET", "/all_users/")
        if users:
            m = folium.Map(location=[0, 0], zoom_start=2)
            for user in users:
                folium.Marker(
                    [user['latitude'], user['longitude']],
                    popup=f"{user['first_name']} {user['last_name']}",
                    tooltip=user['email']
                ).add_to(m)
            folium_static(m)















                    