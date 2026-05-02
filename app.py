import streamlit as st
import yt_dlp
import os
import tempfile

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
        with st.spinner("Downloading... please wait ⏳"):
            try:
                tmpdir = tempfile.mkdtemp()

                po_token = st.secrets.get("PO_TOKEN", "")
                visitor_data = st.secrets.get("VISITOR_DATA", "")

                ydl_opts = {
                    'format': 'best[ext=mp4]/best' if option == "🎥 Video (MP4)" else 'bestaudio/best',
                    'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {
                        'youtube': {
                            'po_token': [f'web+{po_token}'] if po_token else [],
                            'visitor_data': [visitor_data] if visitor_data else [],
                        }
                    },
                }

                if option == "🎵 Audio (MP3)":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                    mime_type = "audio/mpeg"
                    file_ext = ".mp3"
                else:
                    mime_type = "video/mp4"
                    file_ext = ".mp4"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'file')

                files = os.listdir(tmpdir)
                if files:
                    file_path = os.path.join(tmpdir, files[0])
                    with open(file_path, 'rb') as f:
                        file_bytes = f.read()

                    st.success(f"✅ Ready: **{title}**")
                    st.download_button(
                        label="⬇️ Click here to Download",
                        data=file_bytes,
                        file_name=f"{title}{file_ext}",
                        mime=mime_type
                    )

            except Exception as e:
                st.error(f"❌ Error: {e}")