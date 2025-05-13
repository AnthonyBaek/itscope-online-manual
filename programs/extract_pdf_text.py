import pdfplumber
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, '..', 'public', '01_inputs', 'itscope_manual_pdf.pdf')
OUTPUT_PATH = os.path.join(BASE_DIR, '..', 'public', '02_outputs', 'itscope_manual_txt.txt')

def table_to_markdown(table):
    if not table or not table[0]:
        return ''
    # 셀 값이 None이면 빈 문자열로 변환
    def clean(cell):
        return (cell or '').replace('\n', ' ').replace('\r', '').strip()
    header = '| ' + ' | '.join(clean(cell) for cell in table[0]) + ' |'
    separator = '| ' + ' | '.join('---' for _ in table[0]) + ' |'
    rows = []
    for row in table[1:]:
        rows.append('| ' + ' | '.join(clean(cell) for cell in row) + ' |')
    # 표와 표, 표와 문단 사이에 빈 줄 추가
    return '\n'.join(['', header, separator] + rows + [''])

def convert_line_to_md(line):
    # 계층적 불릿/번호 리스트 변환
    indent = 0
    while line.startswith(' ') or line.startswith('\t'):
        if line.startswith('    '):  # 4칸
            indent += 1
            line = line[4:]
        elif line.startswith('\t'):
            indent += 1
            line = line[1:]
        elif line.startswith(' '):
            line = line[1:]
    # 불릿 문자 패턴
    bullet_pattern = r'^[•●○\u2022\u25CF\u25CB\u25A0\u25E6\u25AA\u25AB\u25B6\u25C6\u25C7\u25A1\u25A3\u25A4\u25A5\u25A6\u25A7\u25A8\u25A9\u25B2\u25B3\u25B4\u25B5\u25B8\u25B9\u25BA\u25BB\u25BC\u25BD\u25BE\u25BF\u2605\u2606\u2736\u2737\u2738\u2739\u273A\u273B\u273C\u273D\u273E\u273F\u2740\u2741\u2742\u2743\u2744\u2745\u2746\u2747\u2748\u2749\u274A\u274B]+'
    if re.match(bullet_pattern, line):
        line = re.sub(bullet_pattern, '', line).lstrip()
        return '  ' * indent + '- ' + line
    # 번호 리스트(1. 2. 1) 등)
    number_pattern = r'^(\d+\.\s|\d+\)\s|[a-zA-Z]\.\s|[a-zA-Z]\)\s)'
    if re.match(number_pattern, line):
        return '  ' * indent + line
    return line

def extract_text_from_pdf(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ''
        for page in pdf.pages[4:]:
            # 표 추출
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    all_text += table_to_markdown(table) + '\\n'
            # 일반 텍스트 추출 및 리스트 변환
            text = page.extract_text()
            if text:
                for line in text.split('\\n'):
                    all_text += convert_line_to_md(line) + '\\n'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(all_text)

if __name__ == '__main__':
    extract_text_from_pdf(PDF_PATH, OUTPUT_PATH)
    print(f'PDF 텍스트가 {OUTPUT_PATH} 파일로 저장되었습니다.') 