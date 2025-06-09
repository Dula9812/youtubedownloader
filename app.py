from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['youtube_url']
        format_type = request.form['format']

        try:
            unique_id = str(uuid.uuid4())
            output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

            ydl_opts = {
                'outtmpl': output_path,
                'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio' if format_type == 'mp3' else 'FFmpegVideoConvertor',
                    'preferredcodec': 'mp3' if format_type == 'mp3' else 'mp4',
                    'preferredquality': '192' if format_type == 'mp3' else None
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if format_type == 'mp3':
                    filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
                else:
                    filename = filename.rsplit('.', 1)[0] + '.mp4'

            return render_template('download.html', filename=os.path.basename(filename))

        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
