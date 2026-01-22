from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename
from main import generate_wordcloud

app = Flask(__name__)
app.secret_key = 'wordcloud_secret_key_2024'  # 보안을 위한 시크릿 키

# 업로드 설정
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

# 폴더 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

def allowed_file(filename):
    """허용된 파일 확장자인지 확인"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """메인 페이지 - 파일 업로드 폼"""
    if request.method == 'POST':
        # 파일이 있는지 확인
        if 'file' not in request.files:
            flash('파일이 선택되지 않았습니다.')
            return redirect(request.url)

        file = request.files['file']

        # 파일명이 비어있는지 확인
        if file.filename == '':
            flash('파일이 선택되지 않았습니다.')
            return redirect(request.url)

        # 파일이 허용된 형식인지 확인
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # 파일 내용 읽기
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # 워드클라우드 생성
                unique_id = str(uuid.uuid4())
                output_filename = f"wordcloud_{unique_id}.png"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

                generate_wordcloud(text, output_path)

                # 임시 파일 삭제
                os.remove(file_path)

                # 다운로드 페이지로 리다이렉트
                return redirect(url_for('download', filename=output_filename))

            except Exception as e:
                # 오류 발생 시 파일 삭제
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash(f'워드클라우드 생성 중 오류가 발생했습니다: {str(e)}')
                return redirect(request.url)
        else:
            flash('지원하지 않는 파일 형식입니다. .txt 파일만 업로드 가능합니다.')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    """워드클라우드 이미지 다운로드"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        flash('파일을 찾을 수 없습니다.')
        return redirect(url_for('index'))

    try:
        return send_file(
            file_path,
            as_attachment=True,
            download_name='wordcloud.png',
            mimetype='image/png'
        )
    except Exception as e:
        flash(f'다운로드 중 오류가 발생했습니다: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)