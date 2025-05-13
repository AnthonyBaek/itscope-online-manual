import os
import json
from pathlib import Path

# 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
TOC_JSON = BASE_DIR / 'public' / '02_outputs' / 'manual_toc_json.json'
MD_DIR = BASE_DIR / 'public' / '02_outputs' / 'manual_md'

# manual_toc_json.json 로드
with open(TOC_JSON, encoding='utf-8') as f:
    toc = json.load(f)

# md 파일명 -> breadcrumb 경로 매핑 생성
def build_breadcrumb_map():
    mapping = {}
    def traverse(node, path):
        current_path = path + [node['title']]
        md_file = node.get('file')
        if md_file:
            mapping[md_file] = current_path
        for child in node.get('children', []):
            traverse(child, current_path)
    for top in toc:
        traverse(top, [])
    return mapping

breadcrumb_map = build_breadcrumb_map()

# 모든 md 파일에 대해 breadcrumb 추가
for md_file, breadcrumb in breadcrumb_map.items():
    md_path = MD_DIR / md_file
    if not md_path.exists():
        continue
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    # 이미 breadcrumb가 있으면 건너뜀 (중복 방지)
    if lines and lines[0].startswith('<!--breadcrumb:'):
        continue
    # breadcrumb 텍스트 생성
    breadcrumb_text = ' / '.join(breadcrumb[:-1])  # 마지막(자기자신) 제외
    if breadcrumb_text.strip():
        # HTML 주석으로 마킹 + 실제 표시 텍스트
        breadcrumb_line = f'<!--breadcrumb:{breadcrumb_text}--><span class="md-breadcrumb">{breadcrumb_text}</span>\n'
    else:
        breadcrumb_line = ''
    # H1 위에 삽입
    if breadcrumb_line:
        new_lines = [breadcrumb_line] + lines
        with open(md_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines) 