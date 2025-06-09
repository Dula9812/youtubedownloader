from flask import Flask, request, render_template, send_file, url_for
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        url = request.form['youtube_url']
        format_type = request.form['format']
        try:
            yt = YouTube(url)
            if format_type == 'mp3':
                stream = yt.streams.filter(only_audio=True).first()
                out_file = stream.download(output_path=DOWNLOAD_FOLDER)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                new_file = stream.download(output_path=DOWNLOAD_FOLDER)

            filename = os.path.basename(new_file)
            return render_template('download.html', filename=filename)
        except Exception as e:
            error = str(e)
    return render_template('index.html', error=error)

@app.route('/download/<filename>')
def download_file(filename):
    ad_url = "https://databoilrecommendation.com/uz2vchu6id?key=28565a3b0fd6701ddb0dffa3e9e84cb8"
    return render_template("ad_redirect.html", ad_url=ad_url, file_url=url_for('serve_file', filename=filename))

@app.route('/file/<filename>')
def serve_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
