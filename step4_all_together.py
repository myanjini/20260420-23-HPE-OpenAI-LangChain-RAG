from step2_pdf_to_text_preprocessing import pdf_to_text_file
from step3_text_summary_to_markdown import text_summary_to_md_file

def summarize_pdf_file_to_markdown(pdf_file_path: str) -> str:
    txt_file_path = pdf_to_text_file(pdf_file_path)
    md_file_path = text_summary_to_md_file(txt_file_path)

    with open(md_file_path, "r", encoding="utf-8") as file:
        return file.read()
    
if __name__ == "__main__":
    md = summarize_pdf_file_to_markdown("./data/crop-model.pdf")
    print(md)
