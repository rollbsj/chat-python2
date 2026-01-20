# -*- coding: utf-8 -*-
import io
import os

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# OpenCV 얼굴 검출 캐스케이드 경로
CASCADE_PATH = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


def apply_face_mosaic(image_bytes):
    """이미지 바이트를 받아 얼굴 영역에 모자이크를 적용한 이미지 바이트 반환"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_roi = image[y : y + h, x : x + w]
        face_roi = cv2.resize(face_roi, (50, 20))
        face_roi = cv2.resize(face_roi, (w, h), interpolation=cv2.INTER_AREA)
        image[y : y + h, x : x + w] = face_roi

    _, buf = cv2.imencode(".png", image)
    return buf.tobytes()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"ok": False, "error": "이미지 파일이 없습니다."}), 400

    f = request.files["image"]
    if f.filename == "":
        return jsonify({"ok": False, "error": "파일을 선택해주세요."}), 400

    ext = (os.path.splitext(f.filename)[1] or "").lower()
    if ext not in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
        return jsonify({"ok": False, "error": "지원 형식: JPG, PNG, BMP, WEBP"}), 400

    try:
        raw = f.read()
        out = apply_face_mosaic(raw)
        if out is None:
            return jsonify({"ok": False, "error": "이미지를 읽을 수 없습니다."}), 400

        base = os.path.splitext(f.filename)[0]
        download_name = f"{base}_mosaic.png"
        return send_file(
            io.BytesIO(out),
            mimetype="image/png",
            as_attachment=True,
            download_name=download_name,
        )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
