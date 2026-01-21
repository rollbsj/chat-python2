import pytesseract
from PIL import Image

# Path to the Tesseract executable (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open the image
img = Image.open("images/test.jpg")

# Run OCR
text = pytesseract.image_to_string(img, lang="kor", config="--psm 6")

print(text)
