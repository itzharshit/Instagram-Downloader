import streamlit as st
import requests 
import random

# Function for random balloon animation
def random_celeb():
    return random.choice([st.balloons()])

# Function for downloading dp 
def download_dp(username):
    username.replace('@', '')
    url = f'https://instagram.com/{username}/?__a=1'
    try:
        visit = requests.get(url).json()
        profilePic = visit['graphql']['user']['profile_pic_url_hd']
        st.download_button('Download DP', ProfilePic, file_name='profile_pic.jpg')
    except Exception as e:
        st.error(e)

# Function for downloading media
def download_media(url):
    if '?' in url:
        url += '&__a=1'
    else:
        url += '?__a=1'

    try:
        visit = requests.get(url).json()
        is_video = visit['graphql']['shortcode_media']['is_video']
        try:
            posts = visit["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
            for post in posts:
                is_video = post["node"]["is_video"]
                if is_video:
                    videoFile = post["node"]["video_url"]
                    st.download_button('Download Video', videoFile, file_name='video.mp4')
                else:
                    postFile = post["node"]["display_url"]
                    st.download_button('Download post', postFile, file_name='post.jpg')
        except:
            if is_video:
                videoFile = visit["graphql"]["shortcode_media"]["video_url"]
                st.download_button('Download Video', videoFile, file_name='video.mp4')
            else:
                postFile = visit["graphql"]["shortcode_media"]["display_url"]
                st.download_button('Download post', postFile, file_name='post.jpg')
    except Exception as e:
        st.error(e)

# Integrating and calling all above functions
st.title("Instagram Downloader")
url = st.text_input(label="Paste URL for media or username for DP")
if st.button("Download"):
    if url:
        try:
            with st.spinner("Loading..."):
                if 'http' in url:
                    download_media(url)
                elif '@' in url:
                    download_dp(url)
                else:
                    st.error('No Instagram username or URL found.')
            random_celeb()
        except Exception as e:
            st.error(e)

