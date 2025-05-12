import os
import re
import json

TOC_RAW_PATH = "public/manual_toc_raw.md"
OUTPUT_PATH = "public/manual_toc_json.json"

TOC_LINE_PATTERN = re.compile(r"^(\d+(?:\.\d+)*\.)\s+(.+)$")

def parse_toc_line(line):
    match = TOC_LINE_PATTERN.match(line.strip())
    if not match:
        return None
    numbers = match.group(1).rstrip('.')
    title = match.group(2).strip()
    level = numbers.count('.') + 1 if numbers else 1
    file = f"{numbers}.md"
    return {
        "numbers": numbers,
        "title": title,
        "file": file,
        "level": level,
        "children": []
    }

def build_tree(items):
    root = []
    stack = []
    for item in items:
        while stack and not item["numbers"].startswith(stack[-1]["numbers"] + "."):
            stack.pop()
        if not stack:
            root.append(item)
        else:
            stack[-1]["children"].append(item)
        stack.append(item)
    return root

def set_is_leaf(node):
    if node["children"]:
        for child in node["children"]:
            set_is_leaf(child)
        node["isLeaf"] = False
    else:
        node["isLeaf"] = True

def main():
    if not os.path.exists(TOC_RAW_PATH):
        print(f"[오류] {TOC_RAW_PATH} 파일이 존재하지 않습니다.")
        return
    items = []
    with open(TOC_RAW_PATH, encoding="utf-8") as f:
        for line in f:
            item = parse_toc_line(line)
            if item:
                items.append(item)
    tree = build_tree(items)
    for node in tree:
        set_is_leaf(node)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    print(f"목차 트리 JSON이 {OUTPUT_PATH}로 저장되었습니다.")

if __name__ == "__main__":
    main() 