import pymupdf
import os


def pdf_to_text_file(pdf_file_path):
    pdf_file = pymupdf.open(pdf_file_path)

    pdf_contents = ""
    for page in pdf_file:
        pdf_contents += page.get_text()

    txt_file_path = pdf_file_path.replace(".pdf", ".txt")
    with open(txt_file_path, "w", encoding="utf-8") as f:
        f.write(pdf_contents)

    return os.path.abspath(txt_file_path)


if __name__ == "__main__":
    text_file_path = pdf_to_text_file("./data/crop-model.pdf")
    print(text_file_path)
