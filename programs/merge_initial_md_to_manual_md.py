import os
import re

MANUAL_MD_DIR = '../public/02_outputs/manual_md'
INITIAL_MD_DIR = '../public/03_resources/initial_md'

def extract_header_lines(lines):
    header_end = 0
    h_count = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            h_count += 1
        if h_count >= 2:
            header_end = i + 1
            break
    if header_end == 0:
        # H2가 없으면 H1까지만
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                header_end = i + 1
                break
    return lines[:header_end], lines[header_end:]

def merge_md_files(manual_path, initial_path):
    with open(manual_path, 'r', encoding='utf-8') as f:
        manual_lines = f.readlines()
    header, _ = extract_header_lines(manual_lines)
    with open(initial_path, 'r', encoding='utf-8') as f:
        initial_lines = f.readlines()
    # initial_md에서 H1, H2, breadcrumb 등은 제거하고 본문만 추출
    _, initial_body = extract_header_lines(initial_lines)
    # manual_md의 header + initial_md의 body로 합침
    merged = header + ['\n'] + [line for line in initial_body if line.strip() != '']
    with open(manual_path, 'w', encoding='utf-8') as f:
        f.writelines(merged)
    print(f'Merged: {os.path.basename(manual_path)}')

def main():
    for fname in os.listdir(INITIAL_MD_DIR):
        if fname.endswith('.md'):
            manual_path = os.path.join(MANUAL_MD_DIR, fname)
            initial_path = os.path.join(INITIAL_MD_DIR, fname)
            if os.path.exists(manual_path):
                merge_md_files(manual_path, initial_path)

if __name__ == '__main__':
    main() 