# ITSCOPE 온라인 매뉴얼

## 간단 실행 방법 (ZIP 다운로드 후 바로 실행)

1. **사전 준비**
   - Python 3.x 설치 (https://www.python.org/downloads/)
   - (선택) Git 설치: https://git-scm.com/

2. **프로젝트 코드 다운로드**
   - [GitHub에서 ZIP 다운로드] → 압축 해제
   - 또는 Git 사용 시:
     ```bash
     git clone [repository-url]
     ```

3. **Python 패키지 설치**
   - 매뉴얼을 사용만 하는 목적일 경우 설치하실 필요 없습니다.
   ```bash
   pip install pdfplumber
   ```

4. **로컬 웹서버 실행**
   ```bash
   cd public
   python -m http.server 8000
   ```

5. **웹 브라우저에서 접속**
   - http://localhost:8000/src/

6. (선택) PDF → 마크다운 자동화 프로그램 실행은 하단 "데이터 전처리 및 자동화 프로그램 목록" 참고
   - 본인이 가진 PDF 및 목차/Markdown 파일을 기준으로 매뉴얼을 업데이트하고 싶을 경우 참고

---

이 프로젝트는 ITSCOPE의 PDF 기반 매뉴얼을 웹에서 마크다운 및 메뉴 트리 구조로 제공하는 웹 애플리케이션입니다.

## 주요 기능

- **트리 기반 메뉴 구조**
  - 최대 4레벨까지의 계층적 메뉴 제공
  - 접기/펼치기 가능한 트리 구조
  - 메뉴 트리와 컨텐츠 영역 사이 리사이저로 너비 조절 가능

- **검색 기능**
  - 메뉴 내 텍스트 기반 실시간 검색
  - 검색 결과의 트리 구조 유지
  - 검색 결과 없을 때 안내 메시지

- **마크다운 기반 컨텐츠**
  - PDF에서 추출한 마크다운 문서 제공
  - 스크린샷 이미지 팝업 지원
  - 반응형 이미지 처리

- **인쇄 기능**
  - 컨텐츠 영역만 선택적 인쇄
  - 모던한 인쇄 버튼 UI

- **마크다운 bullet 정리:**
  - `programs/format_bullet_md.py`
    - 특수문자 bullet(⚫, ✓ 등)을 마크다운 bullet(-)로 변환
    - 계층에 따라 들여쓰기 적용
    - 전체 md 일괄 변환 또는 파일 지정 변환 가능

## 데이터 전처리 및 자동화 프로그램 목록

- **extract_tocraw_from_pdf.py**
  - PDF 파일에서 목차(raw)를 추출하여 텍스트 파일로 저장
  - 사용법: `python extract_tocraw_from_pdf.py`

- **generate_menu_json_from_tocraw.py**
  - tocraw 파일을 기반으로 메뉴 트리 JSON(manual_toc_json.json) 생성
  - 사용법: `python generate_menu_json_from_tocraw.py`

- **generate_menu_md_from_tocraw.py**
  - tocraw 파일을 기반으로 각 목차별 빈 마크다운 파일 생성 (H1 제목만)
  - 사용법: `python generate_menu_md_from_tocraw.py`

- **add_breadcrumb_to_md.py**
  - 각 md 파일에 breadcrumb(트리 경로) 자동 삽입
  - 사용법: `python add_breadcrumb_to_md.py`

- **add_5th_level_toc_to_4th_md.py**
  - 4레벨 md 파일 내에 5레벨 목차를 H2 마크다운(## 제목)으로 자동 삽입
  - 사용법: `python add_5th_level_toc_to_4th_md.py`

- **extract_pdf_text.py**
  - PDF 파일에서 텍스트와 표를 추출하여 마크다운 스타일로 변환
  - 사용법: `python extract_pdf_text.py`

- **pdf_to_markdown.py**
  - 텍스트 파일(itscope_pmo_manual.txt)에서 목차 구조를 인식해 각 목차별 마크다운 파일로 분할 생성
  - 사용법: `python pdf_to_markdown.py`

- **format_md_files.py**
  - 마크다운 파일의 리스트/표/텍스트 구조 및 개행을 정리
  - 사용법: `python format_md_files.py`

- **format_bullet_md.py**
  - 특수문자 bullet(⚫, ✓ 등)을 마크다운 bullet(-)로 변환, 계층에 따라 들여쓰기 적용
  - 사용법:
    - 전체 변환: `python format_bullet_md.py`
    - 특정 파일만 변환: `python format_bullet_md.py ../public/02_outputs/manual_md/1.1.md`

## 실행 예시

```bash
# PDF에서 목차(raw) 추출
python extract_tocraw_from_pdf.py

# tocraw로부터 메뉴 트리 JSON 생성
python generate_menu_json_from_tocraw.py

# tocraw로부터 각 목차별 빈 md 파일 생성
python generate_menu_md_from_tocraw.py

# md 파일에 breadcrumb 자동 삽입
python add_breadcrumb_to_md.py

# 4레벨 md 파일에 5레벨 목차(H2) 자동 삽입
python add_5th_level_toc_to_4th_md.py

# PDF에서 텍스트/표 추출 및 마크다운 변환
python extract_pdf_text.py

# 텍스트 파일을 목차별 md로 분할
python pdf_to_markdown.py

# md 파일의 리스트/표/텍스트 구조 정리
python format_md_files.py

# 특수문자 bullet을 마크다운 bullet(-)로 변환
python format_bullet_md.py
# 또는 특정 파일만 변환
python format_bullet_md.py ../public/02_outputs/manual_md/1.1.md
```

## 기술 스택

- HTML5
- CSS3
- JavaScript (Vanilla)
- Python (PDF 처리 및 마크다운 변환)

## 프로젝트 구조

```
/
├── programs/                 # PDF 처리 및 마크다운 변환 프로그램
├── public/
│   ├── 01_inputs/           # 입력 파일 (PDF 등)
│   ├── 02_outputs/          # 생성된 마크다운 파일
│   ├── 03_resources/        # 이미지 등 리소스
│   └── src/                 # 웹 애플리케이션 소스
│       ├── index.html
│       ├── css/
│       └── js/
└── requirements_rules/      # 프로젝트 요구사항 문서
```

## 설치 및 실행

1. 저장소 클론
```bash
git clone [repository-url]
```

2. Python 의존성 설치
```bash
pip install pdfplumber
```

3. PDF 처리 및 마크다운 변환
```bash
cd programs
python extract_pdf_text.py
python pdf_to_markdown.py
python format_md_files.py
```

4. 로컬 웹 서버 실행
```bash
cd public
python -m http.server 8000
```

5. 웹 브라우저에서 접속
```
http://localhost:8000/src/
```

## 개발 환경

- Python 3.x
- 웹 브라우저 (Chrome, Firefox 등)
- 로컬 웹 서버 (Python http.server)

## 제약사항

- 모바일 환경 지원 제외
- 다국어 지원 제외
- PDF 직접 처리 제외
- 보안 기능 제외

## 라이선스

© 2024 ITSCOPE. All rights reserved. 