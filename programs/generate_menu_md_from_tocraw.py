import os
import re

TOC_RAW_PATH = "manual_toc_raw.md"
OUTPUT_DIR = "public/manual_md"

# 목차 라인 패턴: 1.1.3.   시스템 환경 설정
TOC_LINE_PATTERN = re.compile(r"^(\d+(?:\.\d+)*\.)\s+(.+)$")


def parse_toc_line(line):
    match = TOC_LINE_PATTERN.match(line.strip())
    if not match:
        return None, None
    num = match.group(1).rstrip('.')  # 마지막 점 제거
    title = match.group(2).strip()
    return num, title


def main():
    if not os.path.exists(TOC_RAW_PATH):
        print(f"[오류] {TOC_RAW_PATH} 파일이 존재하지 않습니다.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(TOC_RAW_PATH, encoding="utf-8") as f:
        for line in f:
            num, title = parse_toc_line(line)
            if not num or not title:
                continue
            filename = f"{num}.md"
            filename = filename.replace("..", ".")  # 중복된 점 방지
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as md:
                md.write(f"# {title}\n")
    print(f"모든 목차별 md 파일이 {OUTPUT_DIR}에 생성되었습니다.")

if __name__ == "__main__":
    main() 