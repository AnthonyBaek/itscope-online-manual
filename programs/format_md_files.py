import os
import re

MD_DIR = 'md_output'

# 리스트 항목 감지 패턴
BULLET_PATTERN = re.compile(r'^( *)([-*•●○]) (.+)')
NUMBERED_PATTERN = re.compile(r'^( *)(\d+\.|\d+\)|[a-zA-Z]\.|[a-zA-Z]\)) (.+)')

def format_md_lines(lines):
    result = []
    prev_type = None
    for line in lines:
        stripped = line.rstrip('\n')
        # 리스트 항목 감지
        m_bullet = BULLET_PATTERN.match(stripped)
        m_number = NUMBERED_PATTERN.match(stripped)
        is_list = False
        if m_bullet:
            indent = len(m_bullet.group(1)) // 2  # 2칸마다 한 단계로 가정
            line = '  ' * indent + '- ' + m_bullet.group(3)
            is_list = True
        elif m_number:
            indent = len(m_number.group(1)) // 2
            line = '  ' * indent + m_number.group(2) + ' ' + m_number.group(3)
            is_list = True
        else:
            line = stripped
        # 표 감지
        is_table = line.strip().startswith('|') and line.strip().endswith('|')
        # 빈 줄
        if not line.strip():
            result.append('')
            prev_type = None
            continue
        # 타입이 바뀌면 빈 줄 추가
        if prev_type and ((prev_type == 'list' and not is_list) or (prev_type == 'table' and not is_table) or (prev_type == 'text' and (is_list or is_table))):
            result.append('')
        result.append(line.rstrip())
        if is_list:
            prev_type = 'list'
        elif is_table:
            prev_type = 'table'
        else:
            prev_type = 'text'
    return '\n'.join(result)

def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    formatted = format_md_lines(lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(formatted + '\n')

def process_all_md_files(md_dir):
    for filename in os.listdir(md_dir):
        if filename.endswith('.md'):
            process_md_file(os.path.join(md_dir, filename))

if __name__ == '__main__':
    process_all_md_files(MD_DIR)
    print('모든 md 파일의 리스트 계층 및 개행이 정리되었습니다.') 