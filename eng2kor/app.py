`import io
import os
from flask import Flask, render_template, request, send_file
from main import translate_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/translate", methods=["POST"])
def translate():
    if "file" not in request.files:
        return "파일이 선택되지 않았습니다.", 400

    file = request.files["file"]
    if file.filename == "":
        return "파일이 선택되지 않았습니다.", 400

    try:
        content = file.read().decode("utf-8")
    except UnicodeDecodeError:
        try:
            content = file.read().decode("cp949")
        except UnicodeDecodeError:
            return "지원하지 않는 파일 인코딩입니다. UTF-8 또는 CP949를 사용해 주세요.", 400

    translated = translate_text(content)

    # 다운로드할 파일명: 원본명_한글.txt
    base, _ = os.path.splitext(file.filename)
    output_name = f"{base}_한글.txt"

    buffer = io.BytesIO(translated.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=output_name,
        mimetype="text/plain; charset=utf-8",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
