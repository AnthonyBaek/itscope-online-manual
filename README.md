# ITSCOPE 온라인 매뉴얼

## 간단 실행 방법 (ZIP 다운로드 후 바로 실행)

1. **사전 준비**
   - Python 3.x 설치 (https://www.python.org/downloads/)
        - Python 설치 시 Add PATH 체크
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
   - **특정 md 파일로 바로 접속하려면 URL 뒤에 #목차번호를 붙이면 됩니다.**
     - 예시: http://localhost:8000/src/#1.2.1 → 1.2.1.md 파일이 바로 열림

6. (선택) PDF → 마크다운 자동화 프로그램 실행은 하단 "데이터 전처리 및 자동화 프로그램 목록" 참고
   - 본인이 가진 PDF 및 목차/Markdown 파일을 기준으로 매뉴얼을 업데이트하고 싶을 경우 참고

## 매뉴얼 관리 방법

만약 PDF에서 추출한 `manual_toc_raw.md` 파일만 있는 경우(PDF 파일만 있을 경우, programs/extract_tocraw_from_pdf.py 를 실행하여 `manual_toc_raw.md`를 생성할 수 있습니다. (현재 1~4 페이지는 skip하도록 되어있으므로, 전체 문서에 대해 추출을 원할 경우 프로그램 수정이 필요합니다)), 아래 순서대로 자동화 프로그램을 실행하면 전체 온라인 매뉴얼 데이터(트리, md, 이미지 등)를 일괄적으로 생성·관리할 수 있습니다.

1. **목차 트리 JSON 생성**
   ```bash
   python generate_menu_json_from_tocraw.py
   ```
   - `manual_toc_raw.md` → `manual_toc_json.json` (트리 구조)

2. **목차별 빈 마크다운 파일 생성**
   ```bash
   python generate_menu_md_from_tocraw.py
   ```
   - `manual_toc_raw.md` → `manual_md/*.md` (각 목차별 H1만 포함된 md 파일)

3. **breadcrumb(트리 경로) 자동 삽입**
   ```bash
   python add_breadcrumb_to_md.py
   ```
   - 각 md 파일 상단에 breadcrumb 추가

4. **4레벨 md에 5레벨 목차(H2) 자동 삽입**
   ```bash
   python add_5th_level_toc_to_4th_md.py
   ```
   - 4레벨 md 파일에 5레벨 목차(H2) 구조 자동 생성

5. **PDF에서 텍스트/표 추출 및 마크다운 변환**  
   (PDF 원본이 있을 경우)
   ```bash
   python extract_pdf_text.py
   ```
   - PDF → 텍스트/표 추출 및 마크다운 변환

6. **텍스트 파일을 목차별 md로 분할**
   ```bash
   python pdf_to_markdown.py
   ```
   - 추출된 텍스트를 목차 구조에 따라 md로 분할

7. **마크다운 파일 구조 정리**
   ```bash
   python format_md_files.py
   ```
   - 리스트, 표, 텍스트, 개행 등 정리

8. **특수문자 bullet(-, ●, ✓ 등) 정리**
   ```bash
   python format_bullet_md.py
   ```

9. **PDF에서 섹션별 이미지 추출**
   ```bash
   python extract_images_by_section.py
   ```
   - manual_images 폴더에 이미지 저장

10. **이미지 자동 삽입**
    ```bash
    python insert_images_to_md.py
    ```
    - manual_md/*.md에 이미지 자동 삽입

---

### 💡 참고
- 위 절차는 **manual_toc_raw.md**만 있으면 전체 매뉴얼 데이터(트리, md, 이미지 등)를 자동으로 생성·관리할 수 있도록 설계되어 있습니다.
- 각 단계별로 생성되는 파일/폴더는 README의 "주요 입력/출력 파일 및 폴더 설명"을 참고하세요.
- PDF 원본이 없는 경우, 5~6번 단계는 생략 가능합니다.

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
  - 이미지 클릭 시 팝업(모달)로 확대, 단 로고 등은 예외 처리

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

- **insert_images_to_md.py**
  - manual_images 폴더의 이미지를 manual_md 폴더의 md 파일에 섹션 규칙에 맞게 자동 삽입
  - 5레벨 이미지는 4레벨 md의 N번째 H2(##) 섹션 하단(섹션 내 '그림' 우선), 4레벨 이하는 '그림' 아래, 없으면 파일 하단에 삽입
  - 캡션이 없으면 "설명 이미지"로 대체
  - 이미지 경로는 `/02_outputs/manual_images/파일명.png`로 절대경로 사용
  - 중복 삽입 방지
  - 사용법: `python insert_images_to_md.py`

- **extract_images_by_section.py**
  - PDF에서 각 섹션별 이미지를 추출, 회사 로고(왼쪽 하단)는 자동 필터링
  - 한 페이지에 여러 섹션이 매핑될 때, 실제 이미지를 포함하는 섹션에만 이미지가 저장되도록 leaf 섹션, y좌표, 섹션 범위 등 다양한 로직 적용
  - 이미지가 1개면 _(1) 없이, 2개 이상이면 _(n) 붙이도록 파일명 규칙 적용
  - [img]가 붙은 섹션만 이미지 추출 대상으로 삼음
  - 사용법: `python extract_images_by_section.py`

- **extract_tocraw_with_page.py**
  - PDF의 목차와 페이지 (목차-페이지 맵핑), 이미지 존재여부([img])를 추출
  - y좌표 기반으로 섹션별 이미지 매핑, 해시/텍스트 순서 기반 논리적 목차 순서 유지, 이미지 중심 y좌표로 가장 가까운 섹션에만 매핑
  - 디버깅 로그, 예외처리, PDF 구조에 따른 반복 개선
  - 사용법: `python extract_tocraw_with_page.py`

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

# 이미지 추출 및 마크다운 내 자동 삽입
python extract_images_by_section.py
python insert_images_to_md.py
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

## 주요 입력/출력 파일 및 폴더 설명

### public/01_inputs/
- **itscope_manual_pdf.pdf**  
  온라인 매뉴얼로 전환하기 위해 입력하는 원본 매뉴얼 PDF 파일입니다.
- **itscope_why.jpg, itscope_products_comparison.pdf**  
  매뉴얼 내에서 활용되는 참고 이미지, 비교표 등 입력 리소스입니다.

### public/02_outputs/
- **manual_toc_raw.md**  
  PDF에서 추출한 목차(raw) 텍스트 파일입니다. 각 목차 항목이 한 줄씩 기록되어 있으며, 후속 자동화 프로그램의 입력으로 사용됩니다.  
  → `extract_tocraw_from_pdf.py`에 의해 생성
- **manual_toc_raw_with_page.md**  
  PDF에서 추출한 목차와 각 목차 항목이 등장한 페이지 정보를 함께 기록한 파일입니다. 예: `1.3.1. 클라이언트 운영 환경 (p6-p6)`  
  → `extract_tocraw_with_page.py`에 의해 생성
- **manual_toc_json.json**  
  목차(raw) 파일을 트리 구조의 JSON으로 변환한 파일입니다. 웹앱의 메뉴 트리 렌더링, 검색 등에서 사용됩니다.  
  → `generate_menu_json_from_tocraw.py`에 의해 생성
- **manual_images/**  
  PDF에서 추출된 섹션별 이미지가 저장되는 폴더입니다. 
  → 파일명 규칙 및 섹션 매핑은 `extract_images_by_section.py`에 의해 자동 관리
- **manual_md/**  
  각 목차별로 분할된 마크다운 파일들이 저장되는 폴더입니다. 예: `1.1.md`, `2.2.1.1.md` 등. 실제 온라인 매뉴얼의 본문 컨텐츠로 사용됩니다.  
  → `insert_images_to_md.py`에 의해 이미지가 자동 삽입되며, 캡션/위치/중복 방지 등 규칙이 적용됨
- **md_output/**  
  (자동화 파이프라인 중간 산출물) PDF 텍스트를 목차별로 분할한 임시 마크다운 파일들이 저장됩니다.  
  → `pdf_to_markdown.py`에 의해 생성

### public/03_resources/
- **logo-white.png, sample_screenshot.png**  
  웹앱에서 사용하는 로고, 샘플 이미지 등 정적 리소스입니다.
- **initial_md/**  
  초기 마크다운 샘플 파일들이 저장된 폴더입니다. manual_md로 컨텐츠를 병합하거나, 샘플로 활용할 수 있습니다. 