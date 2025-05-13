import os
import json
from pathlib import Path
import re

# 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
TOC_JSON = BASE_DIR / 'public' / '02_outputs' / 'manual_toc_json.json'
MD_DIR = BASE_DIR / 'public' / '02_outputs' / 'manual_md'

# manual_toc_json.json 로드
with open(TOC_JSON, encoding='utf-8') as f:
    toc = json.load(f)

# 4레벨 md 파일에 5레벨 H2 목차 삽입 및 기존 5레벨 링크 삭제

def find_4th_and_5th_nodes():
    result = []  # (4레벨 node, [5레벨 children])
    def traverse(node):
        if node.get('level') == 4:
            fifth = [child for child in node.get('children', []) if child.get('level') == 5]
            if fifth:
                result.append((node, fifth))
        for child in node.get('children', []):
            traverse(child)
    for top in toc:
        traverse(top)
    return result

for node4, children5 in find_4th_and_5th_nodes():
    md_file = node4.get('file')
    md_path = MD_DIR / md_file
    if not md_path.exists():
        continue
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    content = ''.join(lines)
    # 기존 5레벨 링크(ul/li, <!--5th-toc-->) 블록 삭제
    content = re.sub(r'<!--5th-toc-->.*?<\/ul>\s*', '', content, flags=re.DOTALL)
    lines = content.splitlines(keepends=True)
    # 이미 5레벨 H2가 있으면 중복 삽입 방지 (주석 태그로 구분)
    if any('<!--5th-h2-toc-->' in l for l in lines[:10]):
        with open(md_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        continue
    # 5레벨 H2 생성
    toc_lines = ['<!--5th-h2-toc-->\n']
    for c in children5:
        title = c.get('title', '')
        toc_lines.append(f'## {title}\n\n')
    # H1 아래에 삽입
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_idx = i + 1
            break
    else:
        insert_idx = 1
    new_lines = lines[:insert_idx] + toc_lines + lines[insert_idx:]
    with open(md_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines) 