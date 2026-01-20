import cv2
import numpy as np
import os

# 현재 파일이 있는 디렉터리로 작업 디렉터리 변경
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 이미지 읽기 (같은 폴더에 photo.jpg가 있어야 합니다)
image = cv2.imread("photo.jpg")

# 이미지가 제대로 읽혔는지 확인
if image is None:
    raise FileNotFoundError("이미지 파일 'photo.jpg'를 찾을 수 없습니다.")

# 얼굴 검출용 캐스케이드 로드 (opencv-python에 포함된 기본 경로 사용)
cascade_file = "haarcascade_frontalface_default.xml"
cascade_path = os.path.join(getattr(cv2.data, "haarcascades", ""), cascade_file)
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise FileNotFoundError(
        f"캐스케이드 파일을 찾을 수 없습니다: '{cascade_path}'. "
        "opencv-python가 설치되어 있는지, 또는 캐스케이드 XML 파일이 있는지 확인하세요."
    )

# 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 얼굴 검출
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# 검출된 얼굴 영역만 블러 효과 (리사이즈 방식으로 처리)
for (x, y, w, h) in faces:
    face_roi = image[y : y + h, x : x + w]
    face_roi = cv2.resize(face_roi, (50, 5))
    face_roi = cv2.resize(face_roi, (w, h), interpolation=cv2.INTER_AREA)
    image[y : y + h, x : x + w] = face_roi

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()