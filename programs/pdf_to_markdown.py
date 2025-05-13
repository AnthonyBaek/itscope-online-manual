import re
import os

TXT_PATH = 'itscope_pmo_manual.txt'
OUTPUT_DIR = 'md_output'

# 목차 패턴: 1. / 1.1. / 1.2.1. / 1.2.1.1. / 1.2.1.1.1. ...
TOC_PATTERN = re.compile(r'^(\d+(?:\.\d+){0,4})\.\s+(.+)$')

# 목차 정보 저장용
class TocNode:
    def __init__(self, number, title, level, parent=None):
        self.number = number
        self.title = title
        self.level = level
        self.parent = parent
        self.children = []
        self.content = []

    def add_child(self, child):
        self.children.append(child)

# 텍스트에서 목차 트리 파싱
def parse_toc_and_content(lines):
    root = TocNode('root', 'root', 0)
    current_nodes = {0: root}
    last_node = root
    for i, line in enumerate(lines):
        m = TOC_PATTERN.match(line)
        if m:
            number = m.group(1)
            title = m.group(2)
            level = number.count('.') + 1
            node = TocNode(number, title, level, parent=current_nodes[level-1])
            current_nodes[level-1].add_child(node)
            current_nodes[level] = node
            last_node = node
        else:
            last_node.content.append(line)
    return root

def format_content_for_md(lines):
    result = []
    prev_type = None
    for line in lines:
        stripped = line.strip()
        # 리스트 항목 감지
        is_list = bool(re.match(r'^(- |\d+\.|\d+\)|[a-zA-Z]\.|[a-zA-Z]\))', stripped))
        # 표 감지
        is_table = stripped.startswith('|') and stripped.endswith('|')
        # 빈 줄
        if not stripped:
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

# 각 노드별로 md 파일 생성
def write_markdown_files(node, base_dir):
    if node.level == 0:
        for child in node.children:
            write_markdown_files(child, base_dir)
        return
    # 4레벨까지는 파일 생성, 5레벨부터는 4레벨 파일에 포함
    if node.level <= 4:
        filename = os.path.join(base_dir, f'{node.number}.md')
        os.makedirs(base_dir, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'# {node.number} {node.title}\n\n')
            f.write(format_content_for_md(node.content) + '\n')
            for child in node.children:
                if child.level == 5:
                    # 5레벨부터는 4레벨 파일 내에 포함
                    f.write(f'\n## {child.number} {child.title}\n\n')
                    f.write(format_content_for_md(child.content) + '\n')
                    for gchild in child.children:
                        # 6레벨 이상도 5레벨 아래에 포함
                        f.write(f'\n### {gchild.number} {gchild.title}\n\n')
                        f.write(format_content_for_md(gchild.content) + '\n')
                else:
                    # 4레벨 이하 자식은 별도 파일로 생성
                    write_markdown_files(child, base_dir)

if __name__ == '__main__':
    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    toc_root = parse_toc_and_content(lines)
    write_markdown_files(toc_root, OUTPUT_DIR)
    print(f'Markdown 파일이 {OUTPUT_DIR} 폴더에 생성되었습니다.') 