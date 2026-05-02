import streamlit as st
import requests
import time

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 YouTube Downloader")
st.write("Download YouTube videos or convert to MP3 easily!")

url = st.text_input("🔗 Paste YouTube URL here:")
option = st.radio("Choose download type:", ["🎵 Audio (MP3)", "🎵 Audio (M4A)"])
download_btn = st.button("Download")

if download_btn:
    if url == "":
        st.warning("Please enter a YouTube URL first!")
    else:
        with st.spinner("Processing... please wait ⏳"):
            try:
                api_key = st.secrets["RAPIDAPI_KEY"]

                headers = {
                    "x-rapidapi-host": "youtube-mp3-audio-video-downloader.p.rapidapi.com",
                    "x-rapidapi-key": api_key
                }

                # Extract video ID from URL
                if "v=" in url:
                    video_id = url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in url:
                    video_id = url.split("youtu.be/")[1].split("?")[0]
                else:
                    video_id = url

                if option == "🎵 Audio (MP3)":
                    api_url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/get_mp3_download_link/{video_id}"
                    params = {"quality": "low", "wait_until_the_file_is_ready": "false"}
                    mime_type = "audio/mpeg"
                    file_ext = ".mp3"
                else:
                    api_url = f"https://youtube-mp3-audio-video-downloader.p.rapidapi.com/get_m4a_download_link/{video_id}"
                    params = {}
                    mime_type = "audio/mp4"
                    file_ext = ".m4a"

                response = requests.get(api_url, headers=headers, params=params)
                data = response.json()
                st.write(data)  # debug - dekho kya aa raha hai

                if "link" in data:
                    download_url = data["link"]
                    title = data.get("title", "audio")

                    file_response = requests.get(download_url)
                    file_bytes = file_response.content

                    st.success(f"✅ Ready: **{title}**")
                    st.download_button(
                        label="⬇️ Click here to Download",
                        data=file_bytes,
                        file_name=f"{title}{file_ext}",
                        mime=mime_type
                    )
                else:
                    st.error(f"❌ Error: {data}")

            except Exception as e:
                st.error(f"❌ Error: {e}")