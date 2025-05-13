import os
import re

IMG_DIR = os.path.join('..', 'public', '02_outputs', 'manual_images')
MD_DIR = os.path.join('..', 'public', '02_outputs', 'manual_md')
IMG_REL_PATH = '/02_outputs/manual_images/'  # 절대경로로 수정

# 이미지 파일명에서 섹션 정보 추출
# 예: 2.3.1.2.11_(1).png → (4레벨: 2.3.1.2, 5레벨: 11)
def parse_image_filename(filename):
    m = re.match(r'^(\d+(?:\.\d+)*)(?:_\((\d+)\))?\.png$', filename)
    if not m:
        return None
    section = m.group(1)  # ex: 2.3.1.2.11 or 2.3.1.2
    parts = section.split('.')
    if len(parts) == 5:
        return {
            'level': 5,
            'md_file': '.'.join(parts[:4]) + '.md',
            'h2_idx': int(parts[4]),
            'img_file': filename
        }
    elif len(parts) == 4:
        return {
            'level': 4,
            'md_file': section + '.md',
            'h2_idx': None,
            'img_file': filename
        }
    else:
        # 3레벨 이하도 하단에 삽입
        return {
            'level': len(parts),
            'md_file': section + '.md',
            'h2_idx': None,
            'img_file': filename
        }

def find_caption(lines, start_idx, end_idx):
    # start_idx ~ end_idx 범위 내에서 '그림'이 포함된 줄을 찾아 캡션 반환
    for idx in range(start_idx, end_idx):
        if '그림' in lines[idx]:
            return lines[idx].strip()
    return ''

def insert_images_to_md():
    img_files = [f for f in os.listdir(IMG_DIR) if f.endswith('.png')]
    # 섹션별로 이미지 그룹핑
    section_map = {}
    for img in img_files:
        info = parse_image_filename(img)
        if not info:
            continue
        key = (info['md_file'], info['h2_idx'])
        section_map.setdefault(key, []).append(info['img_file'])

    for (md_file, h2_idx), img_list in section_map.items():
        md_path = os.path.join(MD_DIR, md_file)
        if not os.path.exists(md_path):
            print(f'[경고] {md_path} 파일이 존재하지 않음')
            continue
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # 중복 삽입 방지: 이미 삽입된 이미지 제거
        new_lines = []
        for line in lines:
            if not any(img in line for img in img_list):
                new_lines.append(line)
        inserted = False
        # 1. '그림'이 포함된 줄 바로 아래에 삽입 (4레벨 이하)
        if h2_idx is None:
            for idx, line in enumerate(new_lines):
                if '그림' in line:
                    caption = line.strip() if line.strip() else '설명 이미지'
                    for img in img_list:
                        new_lines.insert(idx+1, f'![{caption}]({IMG_REL_PATH}{img})\n')
                        idx += 1
                    inserted = True
                    break
        # 2. 5레벨: N번째 H2(##) 섹션 하단(섹션 내 '그림' 우선)
        if h2_idx is not None:
            h2_count = 0
            insert_idx = len(new_lines)
            for idx, line in enumerate(new_lines):
                if line.strip().startswith('## '):
                    h2_count += 1
                    if h2_count == h2_idx:
                        # 섹션 내 '그림'이 있으면 그 아래, 없으면 H2 하단
                        local_inserted = False
                        # 섹션 범위: idx+1 ~ 다음 H2 또는 파일 끝
                        next_h2 = len(new_lines)
                        for j in range(idx+1, len(new_lines)):
                            if new_lines[j].strip().startswith('## '):
                                next_h2 = j
                                break
                        caption = find_caption(new_lines, idx+1, next_h2)
                        if not caption:
                            caption = '설명 이미지'
                        for j in range(idx+1, next_h2):
                            if '그림' in new_lines[j]:
                                for img in img_list:
                                    new_lines.insert(j+1, f'![{caption}]({IMG_REL_PATH}{img})\n')
                                    j += 1
                                local_inserted = True
                                break
                        if not local_inserted:
                            insert_idx = next_h2
                            for img in img_list:
                                new_lines.insert(insert_idx, f'![{caption}]({IMG_REL_PATH}{img})\n')
                                insert_idx += 1
                        inserted = True
                        break
        # 3. 못 찾으면 파일 끝에 삽입 (캡션: 설명 이미지)
        if not inserted:
            for img in img_list:
                new_lines.append(f'![설명 이미지]({IMG_REL_PATH}{img})\n')
        # 파일 저장
        with open(md_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f'[삽입 완료] {md_file} ({len(img_list)}개 이미지)')

if __name__ == '__main__':
    """
    사용법:
    1. manual_images 폴더와 manual_md 폴더가 같은 구조 내에 있어야 함
    2. 이 스크립트를 실행하면, 이미지가 규칙에 맞게 md 파일에 삽입됨
    3. 5레벨 이미지는 4레벨 md의 N번째 H2(##) 섹션 하단(섹션 내 '그림' 우선), 4레벨 이하는 '그림' 아래, 없으면 파일 하단에 삽입
    4. 중복 삽입은 방지됨
    5. IMG_REL_PATH로 경로 쉽게 변경 가능
    6. 캡션은 '그림'이 포함된 줄 전체를 사용, 없으면 '설명 이미지'로 대체
    """
    insert_images_to_md() 