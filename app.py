import streamlit as st
import requests

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 YouTube Downloader")
st.write("Download YouTube videos or convert to MP3 easily!")

url = st.text_input("🔗 Paste YouTube URL here:")
option = st.radio("Choose download type:", ["🎥 Video (MP4)", "🎵 Audio (MP3)"])
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

                if option == "🎵 Audio (MP3)":
                    api_url = "https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download/mp3"
                    params = {"url": url, "quality": "192"}
                    mime_type = "audio/mpeg"
                    file_ext = ".mp3"
                else:
                    api_url = "https://youtube-mp3-audio-video-downloader.p.rapidapi.com/download/mp4"
                    params = {"url": url, "quality": "720"}
                    mime_type = "video/mp4"
                    file_ext = ".mp4"

                response = requests.get(api_url, headers=headers, params=params)
                data = response.json()

                if "link" in data:
                    download_url = data["link"]
                    title = data.get("title", "video")

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