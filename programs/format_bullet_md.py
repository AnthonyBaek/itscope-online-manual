import os
import re
import sys

MD_DIR = '../public/02_outputs/manual_md'

# 특수문자 bullet 패턴 정의
BULLET_PATTERNS = [
    (r'^\s*[⚫●■▪]', 0),  # 상위 bullet
    (r'^\s*[✓✔☑]', 1),   # 하위 bullet
]


def convert_bullets(lines):
    result = []
    for line in lines:
        original = line
        # 상위 bullet
        if re.match(BULLET_PATTERNS[0][0], line):
            text = re.sub(BULLET_PATTERNS[0][0], '', line).strip()
            result.append(f'- {text}')
        # 하위 bullet
        elif re.match(BULLET_PATTERNS[1][0], line):
            text = re.sub(BULLET_PATTERNS[1][0], '', line).strip()
            result.append(f'  - {text}')
        else:
            result.append(line.rstrip())
    return '\n'.join(result)


def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    converted = convert_bullets(lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(converted + '\n')


def process_all_md_files(md_dir):
    for filename in os.listdir(md_dir):
        if filename.endswith('.md'):
            process_md_file(os.path.join(md_dir, filename))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 파일 지정 시 해당 파일만 변환
        target_file = sys.argv[1]
        if os.path.isfile(target_file):
            process_md_file(target_file)
            print(f'{target_file} 파일의 bullet 포맷이 마크다운 스타일로 변환되었습니다.')
        else:
            print(f'지정한 파일을 찾을 수 없습니다: {target_file}')
    else:
        # 인자 없으면 전체 변환
        process_all_md_files(MD_DIR)
        print('모든 md 파일의 bullet 포맷이 마크다운 스타일로 변환되었습니다.') 