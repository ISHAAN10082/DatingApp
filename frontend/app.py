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
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
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
    def get_user_count():
        # Fetch user count data
        response = make_request("GET", "/user_count/")
        if response is not None:
            # Display user count with additional insights
            st.write("### User Count Overview")
            st.write(f"**Total Users:** {response}")

            # Create a simple line chart to show user growth over time (mock data for illustration)
            growth_data = {"Days": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
                           "User Count": [response - 5, response - 3, response, response + 2, response + 5]}
            st.line_chart(growth_data)

    @staticmethod
    def get_gender_distribution():
        # Fetch gender distribution data
        response = make_request("GET", "/gender_distribution/")
        if response:
            # Create a pie chart for gender distribution
            labels = list(response.keys())
            sizes = list(response.values())
            colors = ['#ff9999','#66b3ff','#99ff99']  # Example colors for the pie chart
            
            # Display the pie chart using Streamlit
            st.write("Gender Distribution:")
            st.pyplot(plt.figure(figsize=(6, 6)))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot()
                
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
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(density.keys(), density.values(), color='skyblue')
            ax.set_title("User Density by Region")
            ax.set_xlabel("Region")
            ax.set_ylabel("Number of Users")
            plt.xticks(rotation=45)
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            st.pyplot(fig)

    @staticmethod
    def display_user_map():
        users = make_request("GET", "/all_users/")
        if users:
            # Using a different mapping library or approach
            map_data = [{"name": f"{user['first_name']} {user['last_name']}", 
                          "location": [user['latitude'], user['longitude']], 
                          "email": user['email']} for user in users]
            
            # Create a map centered on the average location of users
            avg_lat = sum(user['latitude'] for user in users) / len(users)
            avg_lon = sum(user['longitude'] for user in users) / len(users)
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)

            for data in map_data:
                folium.Marker(
                    location=data['location'],
                    popup=data['name'],
                    tooltip=data['email']
                ).add_to(m)
            folium_static(m)
            
            
def dummy_function():
    pass
















                    