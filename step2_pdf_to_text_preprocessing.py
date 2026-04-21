import pymupdf
import os


def pdf_to_text_file(pdf_file_path):
    pdf_file = pymupdf.open(pdf_file_path)

    # 머릿말과 꼬릿말 영역의 높이를 정의 (픽셀 단위)
    header_height = 80
    footer_height = 70

    pdf_contents = ""
    for page in pdf_file:
        # 페이지 크기 가져오기
        rect = page.rect

        # 본문 영역 정의
        body_rect = pymupdf.Rect(0, header_height, rect.width, rect.height - footer_height)

        # 텍스트 추출 영역 설정
        page.set_cropbox(body_rect)

        pdf_contents += page.get_text()

    txt_file_path = pdf_file_path.replace(".pdf", "-preprocessed.txt")
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write(pdf_contents)

    return os.path.abspath(txt_file_path)


if __name__ == "__main__":
    text_file_path = pdf_to_text_file("./data/crop-model.pdf")
    print(text_file_path)
