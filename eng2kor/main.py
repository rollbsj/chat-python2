from googletrans import Translator

translator = Translator()


def translate_text(text: str, dest: str = "ko") -> str:
    """영어 텍스트를 한글로 번역합니다."""
    if not text or not text.strip():
        return ""
    result = translator.translate(text, dest=dest)
    return result.text


def translate_file(input_path: str, output_path: str) -> None:
    """영어 파일을 읽어 한글로 번역된 파일을 저장합니다."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    translated = translate_text(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)


if __name__ == "__main__":
    input_file_path = "input_en.txt"
    output_file_path = "output_kr.txt"
    translate_file(input_file_path, output_file_path)
