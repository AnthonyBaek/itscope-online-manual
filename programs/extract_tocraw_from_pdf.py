import re
import pdfplumber
import os

PDF_PATH = "public/base_files/itscope_pmo_manual.pdf"
OUTPUT_PATH = "public/manual_toc_raw.md"

# 목차 패턴: 1. / 1.1. / 1.1.1. ...
TOC_PATTERN = re.compile(r"^(\d+(?:\.\d+)*\.)\s+(.+)$")

START_PAGE_IDX = 4  # 0-based index, 5페이지부터 시작

def extract_toc_from_pdf(pdf_path):
    toc_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[START_PAGE_IDX:]:
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                if TOC_PATTERN.match(line.strip()):
                    toc_lines.append(line.strip())
    return toc_lines

def save_toc_to_md(toc_lines, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for line in toc_lines:
            f.write(line + "\n")

def main():
    if not os.path.exists(PDF_PATH):
        print(f"[오류] {PDF_PATH} 파일이 존재하지 않습니다.")
        return
    toc_lines = extract_toc_from_pdf(PDF_PATH)
    if not toc_lines:
        print("[경고] 추출된 목차가 없습니다.")
    else:
        save_toc_to_md(toc_lines, OUTPUT_PATH)
        print(f"목차 Raw 데이터가 {OUTPUT_PATH}로 저장되었습니다.")

if __name__ == "__main__":
    main() 