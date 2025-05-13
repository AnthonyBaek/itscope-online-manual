import os
import re
import pdfplumber
import shutil
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, '..', 'public', '01_inputs', 'itscope_manual_pdf.pdf')
TOC_PAGE_PATH = os.path.join(BASE_DIR, '..', 'public', '02_outputs', 'manual_toc_raw_with_page.md')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'public', '02_outputs', 'manual_images')

# 로고(왼쪽 하단) bbox 필터 기준
LOGO_X0_MAX = 120  # px
LOGO_BOTTOM_MIN_RATIO = 0.88  # 페이지 높이의 88% 이상(아래쪽)
LOGO_HEIGHT_MAX = 60  # px (로고 높이 제한)

# [img]가 포함된 섹션-페이지 매핑 읽기
def parse_img_sections(toc_page_path):
    section_to_pages = defaultdict(list)
    pattern = re.compile(r'^(\d+(?:\.\d+)*).*\(p(\d+)-p(\d+)\).*\[img\]')
    with open(toc_page_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                section = m.group(1)
                start = int(m.group(2))
                end = int(m.group(3))
                for p in range(start, end+1):
                    section_to_pages[p].append(section)
    return section_to_pages

def is_logo_image(img, page_height):
    # 왼쪽 하단, 작은 높이, 바닥에 가까운 경우
    x0 = img['x0']
    bottom = img['bottom']
    height = img['bottom'] - img['top']
    if (
        x0 < LOGO_X0_MAX and
        bottom > page_height * LOGO_BOTTOM_MIN_RATIO and
        height < LOGO_HEIGHT_MAX
    ):
        return True
    return False

def extract_images(pdf_path, section_to_pages, output_dir):
    # 기존 폴더 삭제 후 새로 생성
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):  # 1-based page index
            if i not in section_to_pages:
                continue
            sections = section_to_pages[i]
            images = page.images
            if not images:
                continue
            page_height = float(page.height)
            filtered_images = [img for img in images if not is_logo_image(img, page_height)]
            if not filtered_images:
                continue
            for sec in sections:
                img_count = len(filtered_images)
                for idx, img in enumerate(filtered_images, 1):
                    bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                    cropped = page.within_bbox(bbox).to_image(resolution=300)
                    if img_count == 1:
                        fname = f"{sec}.png"
                    else:
                        fname = f"{sec}_({idx}).png"
                    out_path = os.path.join(output_dir, fname)
                    cropped.save(out_path, format="PNG")
                print(f"Extracted images for section {sec} (page {i})")

if __name__ == "__main__":
    section_to_pages = parse_img_sections(TOC_PAGE_PATH)
    extract_images(PDF_PATH, section_to_pages, OUTPUT_DIR)
    print(f"이미지 추출 완료: {OUTPUT_DIR}") 