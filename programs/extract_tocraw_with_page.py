import re
import pdfplumber
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, '..', 'public', '01_inputs', 'itscope_manual_pdf.pdf')
OUTPUT_PATH = os.path.join(BASE_DIR, '..', 'public', '02_outputs', 'manual_toc_raw_with_page.md')

# 목차 패턴: 1. / 1.1. / 1.1.1. ...
TOC_PATTERN = re.compile(r"^(\d+(?:\.\d+)*\.)\s+(.+)$")

START_PAGE_IDX = 4  # 0-based index, 5페이지부터 시작

# 로고(왼쪽 하단) bbox 필터 기준 (extract_images_by_section.py에서 복사)
LOGO_X0_MAX = 120  # px
LOGO_BOTTOM_MIN_RATIO = 0.88  # 페이지 높이의 88% 이상(아래쪽)
LOGO_HEIGHT_MAX = 60  # px (로고 높이 제한)

def is_logo_image(img, page_height):
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

def find_toc_y(toc_line, words):
    toc_line_stripped = toc_line.strip()
    # 1. 완전 일치
    for w in words:
        if w['text'].replace(' ', '') == toc_line_stripped.replace(' ', ''):
            return w['top']
    # 2. 포함(부분일치)
    for w in words:
        if toc_line_stripped.replace(' ', '') in w['text'].replace(' ', ''):
            return w['top']
    # 3. 첫 단어 기준
    split_words = toc_line_stripped.split()
    if len(split_words) > 1:
        first_word = split_words[1]
    else:
        first_word = split_words[0]
    toc_word = next((w for w in words if w['text'].startswith(first_word)), None)
    return toc_word['top'] if toc_word else None

def extract_toc_with_page(pdf_path):
    toc_with_page = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[START_PAGE_IDX:], START_PAGE_IDX+1):
            text = page.extract_text()
            if not text:
                continue
            words = page.extract_words()  # y좌표 추출용
            images = [img for img in page.images if not is_logo_image(img, float(page.height))]
            toc_entries = []
            for line in text.splitlines():
                m = TOC_PATTERN.match(line.strip())
                if m:
                    toc_title = line.strip()
                    toc_y = find_toc_y(toc_title, words)
                    toc_entries.append({'title': toc_title, 'y': toc_y})
            toc_entries = [e for e in toc_entries if e['y'] is not None]
            # 논리적 순서 유지
            # 1. 각 이미지의 중심 y좌표 계산
            img_centers = [((img['top'] + img['bottom']) / 2) for img in images]
            # 2. 각 이미지 중심 y좌표를 가장 가까운(아래쪽) 섹션에만 매핑
            img_to_section = [-1] * len(images)  # 각 이미지가 매핑될 섹션 idx
            for img_idx, center_y in enumerate(img_centers):
                min_dist = float('inf')
                min_idx = -1
                for idx, entry in enumerate(toc_entries):
                    start_y = entry['y']
                    end_y = toc_entries[idx+1]['y'] if idx+1 < len(toc_entries) else float(page.height)
                    if start_y < center_y < end_y:
                        dist = abs(center_y - start_y)
                        if dist < min_dist:
                            min_dist = dist
                            min_idx = idx
                img_to_section[img_idx] = min_idx
            # 3. 각 섹션별로 매핑된 이미지가 있으면 [img] 표시
            for idx, entry in enumerate(toc_entries):
                matched_imgs = [img for img_idx, img in enumerate(images) if img_to_section[img_idx] == idx]
                if matched_imgs:
                    toc_with_page.append(f"{entry['title']} (p{i}-p{i})[img]")
                    print(f"[DEBUG] 섹션 '{entry['title']}' (p{i})에 이미지 매핑됨: {len(matched_imgs)}개, 이미지 center: {[ ((img['top']+img['bottom'])/2) for img in matched_imgs ]}")
                else:
                    toc_with_page.append(f"{entry['title']} (p{i}-p{i})")
    return toc_with_page

def save_toc_with_page(toc_lines, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for line in toc_lines:
            f.write(line + "\n")

def main():
    if not os.path.exists(PDF_PATH):
        print(f"[오류] {PDF_PATH} 파일이 존재하지 않습니다.")
        return
    toc_lines = extract_toc_with_page(PDF_PATH)
    if not toc_lines:
        print("[경고] 추출된 목차가 없습니다.")
    else:
        save_toc_with_page(toc_lines, OUTPUT_PATH)
        print(f"목차+페이지 정보가 {OUTPUT_PATH}로 저장되었습니다.")

if __name__ == "__main__":
    main() 