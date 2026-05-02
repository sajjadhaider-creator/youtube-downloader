import streamlit as st
import requests
import time

st.set_page_config(page_title="YouTube Downloader", page_icon="🎬")

st.title("🎬 YouTube Downloader")
st.write("Download YouTube videos or convert to MP3 easily!")

def extract_video_id(url):
    if "shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return url.strip()

def wait_for_file(file_url, max_wait=300):
    for i in range(0, max_wait, 10):
        response = requests.get(file_url)
        if response.status_code == 200:
            return response.content
        time.sleep(10)
    return None

url = st.text_input("🔗 Paste YouTube URL here:")
option = st.radio("Choose download type:", ["🎵 Audio (MP3)", "🎵 Audio (M4A)"])
download_btn = st.button("Download")

if download_btn:
    if url == "":
        st.warning("Please enter a YouTube URL first!")
    else:
        with st.spinner("Processing... please wait ⏳ (may take up to 2 minutes)"):
            try:
                api_key = st.secrets["RAPIDAPI_KEY"]
                video_id = extract_video_id(url)

                headers = {
                    "x-rapidapi-host": "youtube-mp3-audio-video-downloader.p.rapidapi.com",
                    "x-rapidapi-key": api_key
                }

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

                download_url = None
                title = "audio"

                if "link" in data:
                    download_url = data["link"]
                    title = data.get("title", "audio")
                elif "file" in data:
                    download_url = data["file"]
                    title = data.get("title", "audio")

                if download_url:
                    st.info("⏳ File ready ho rahi hai — please wait...")
                    file_bytes = wait_for_file(download_url)

                    if file_bytes:
                        st.success(f"✅ Ready: **{title}**")
                        st.download_button(
                            label="⬇️ Click here to Download",
                            data=file_bytes,
                            file_name=f"{title}{file_ext}",
                            mime=mime_type
                        )
                    else:
                        st.error("❌ File ready nahi hui — dobara try karo!")
                else:
                    st.error(f"❌ Error: {data}")

            except Exception as e:
                st.error(f"❌ Error: {e}")