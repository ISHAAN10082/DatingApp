import streamlit as st
import httpx
import folium
import asyncio
from streamlit_folium import folium_static

BASE_URL = "http://127.0.0.1:8000"

async def fetch_users(num_users: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/fetch_users/", json={"num_users": num_users})
        response.raise_for_status()
        return response.json()

async def get_random_user():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/random_user/")
        response.raise_for_status()
        return response.json()

async def get_nearest_users(uid: str, x: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/nearest_users/", params={"uid": uid, "x": x})
        response.raise_for_status()
        return response.json()

async def get_random_username():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/random_username/")
        response.raise_for_status()
        return response.json()

# Helper function to run async functions
def run_async_func(func, *args):
    return asyncio.run(func(*args))

# Streamlit app layout
st.title("Dating App User Finder")

# Section to fetch and store users
st.header("Fetch and Store Users")
num_users = st.number_input("Number of users to fetch", min_value=1, max_value=1000, value=10)
if st.button("Fetch and Store Users"):
    with st.spinner(f"Fetching and storing {num_users} users..."):
        result = run_async_func(fetch_users, num_users)
        st.success(f"Fetched and stored {num_users} users: {result['message']}")

# Section to fetch and display a random user
st.header("Get Random User")
if st.button("Get Random User"):
    with st.spinner("Fetching random user..."):
        user = run_async_func(get_random_user)
        st.write(f"Name: {user['first_name']} {user['last_name']}")
        st.write(f"Email: {user['email']}")
        st.write(f"Gender: {user['gender']}")
        st.write(f"Location: ({user['latitude']}, {user['longitude']})")

# Section to get and display nearest users
st.header("Get Nearest Users")
uid = st.text_input("Enter User ID", value="")
num_nearest_users = st.number_input("Number of nearest users", min_value=1, max_value=100, value=10)
if st.button("Get Nearest Users"):
    if not uid:
        st.error("Please enter a user ID.")
    else:
        with st.spinner(f"Fetching {num_nearest_users} nearest users..."):
            nearest_users = run_async_func(get_nearest_users, uid, num_nearest_users)
            if nearest_users:
                st.success(f"Fetched {num_nearest_users} nearest users.")

                # Create a map centered around the first user's location if available
                user_location = (nearest_users[0]['latitude'], nearest_users[0]['longitude'])
                m = folium.Map(location=user_location, zoom_start=10)

                # Add the nearest users' locations to the map
                for user in nearest_users:
                    folium.Marker(
                        location=(user['latitude'], user['longitude']),
                        popup=f"{user['first_name']} {user['last_name']}",
                        icon=folium.Icon(color="blue")
                    ).add_to(m)

                # Display the map
                folium_static(m)
            else:
                st.error("No nearest users found.")

# Section to fetch a random username
st.header("Get Random Username")
if st.button("Get Random Username"):
    with st.spinner("Fetching random username..."):
        username = run_async_func(get_random_username)
        st.write(f"Random Username: {username}")
