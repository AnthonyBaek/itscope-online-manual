# Project Requirements

## 0. Project Overview

PDF 파일 기반으로 작성된 ITSCOPE Manual을 웹브라우저에서 쉽게 사용할 수 있도록 전환하는 프로젝트
- 추후 관리 편의성을 위해, 매뉴얼의 섹션별로 markdown으로 관리하여 업데이트 대응 용이

## 1. Environment & Assumptions

### 1.1. Terms

- `tocraw`: PDF 파일에서 추출한 목차(toc)의 raw 파일을 의미
- `menutree`: 추출한 `tocraw`를 기반으로 매뉴얼 내에서 사용 될(및 렌더링 될) 트리 형태의 메뉴 데이터 구조
- `left_menu`: 매뉴얼 앱의 왼편 사이드메뉴로, PDF로부터 추출한 `menutree`를 트리 형태로 렌더링하고, 우측 `content_area`에 해당 메뉴의 md파일을 열 수 있도록 트리 내 링크를 제공
- `content_area`: 매뉴얼 컨텐츠를 보여주는 영역으로, 해당 목차 번호에 맞는 마크다운(`*.md`) 파일을 렌더링하여 출력
- `breadcrumb`: 각 md 파일 최상단에 표시되는, 트리 구조상의 경로(부모~자기자신 전까지)를 `/`로 구분하여 보여주는 텍스트

### 1.2. Project Structure

- `/programs`: 입력(/public/01_inputs/) 파일을 대상으로 `tocraw`와 `menutree`를 추출하기 위한 파이썬 프로그램 및 md 자동 가공 스크립트
- `public`
   - `01_inputs`: 프로그램 및 웹 앱이 사용하는 입력 파일
   - `02_outputs`: 프로그램 및 웹 앱에 의해 생성되는 산출물 및 기타 출력 파일
      - `manual_toc_json.json`: 전체 메뉴 트리 구조(JSON)
      - `manual_md/`: 각 목차별 md 파일 (예: 1.1.3.md, 00_main.md 등)
   - `03_resources`: 앱 내에서 사용될 정적 자원 (이미지 리소스, 로고, 스크린샷 등)
   - `src`: 프로젝트 소스코드 관리 디렉토리
      - `index.html`: 메인 HTML 파일 (GitHub Pages 배포를 위한 진입점)
      - `css/`: 스타일시트 파일
      - `js/`: 자바스크립트 파일
      - `ts/`: 타입스크립트 파일 (선택사항)

### 1.3. Running Environment

- /programs 내의 파이썬 프로그램들을 매뉴얼 목차 업데이트에 따라 언제든지 실행시킬 수 있도록 세팅 필요
- 완성된 온라인 매뉴얼은 서버 없이 브라우저에서 동작 가능해야 함 (Chrome 및 Firefox 등)
- 완성된 HTML 기반의 온라인 매뉴얼은 기타 파일들과 함께 GitHub Pages를 통해 사용자에게 배포
- 프로젝트 내에서 실행하는 terminal은 PowerShell을 사용하므로 터미널 사용 시 이에 맞는 명령어 필요

### 1.4. Programs

*이미 개발되어 있는 항목이므로, 추가 개발 요건이 아님

1. /programs/`extract_tocraw_from_pdf.py`: PDF 파일(public\01_inputs\itscope_pmo_manual.pdf)을 읽어, `tocraw`를 추출하는 Python 프로그램
   - input: public\01_inputs\itscope_pmo_manual.pdf
   - output: public\02_outputs\manual_toc_raw.md
   - 제약사항
      - 제공된 pdf파일의 1~4페이지는 탐색하지 않음
      - pdfplumber 사용, 목차 패턴(x.x.x…) 추출

2. /programs/`generate_menu_json_from_tocraw.py`: `tocraw` 파일(`manual_toc_raw.md`)로부터 JSON 형식을 생성하는 Python 프로그램
   - input: public\02_outputs\manual_toc_raw.md
   - output: public\02_outputs\manual_toc_json.json

3. /programs/`generate_menu_md_from_tocraw.py`: `tocraw` 파일(`manual_toc_raw.md`)로부터 각 목차 항목별 .md 파일을 생성하는 Python 프로그램
   - input: public\02_outputs\manual_toc_raw.md
   - output: public\02_outputs\manual_md\
   - file_name: 목차번호.md (예: 1.1.3.md, 중복된 점(.) 금지)
   - 제약사항
      - 각 md 파일의 첫 줄은 목차 제목을 H1 스타일로 입력
      - md 파일별로 구체적인 컨텐츠는 포함하지 않음 (H1 제목만)

4. /programs/`add_breadcrumb_to_md.py`: 각 md 파일에 breadcrumb(트리 경로) 자동 삽입

5. /programs/`add_5th_level_toc_to_4th_md.py`: 4레벨 md 파일 내에 5레벨 목차를 H2 마크다운(## 제목)으로 자동 삽입하는 Python 프로그램
   - input: public/02_outputs/manual_toc_json.json, public/02_outputs/manual_md/*.md
   - output: public/02_outputs/manual_md/ 내 4레벨 md 파일(5레벨 children이 있는 경우)
   - 동작:
      - 5레벨 children이 존재하는 4레벨 md 파일의 H1 아래에 각 5레벨 제목을 H2(##)로 삽입
      - 기존에 삽입된 5레벨 링크(ul/li, <!--5th-toc--> 주석 포함) 블록이 있으면 자동 삭제
      - 중복 삽입 방지(주석 태그로 구분)
   - 제약사항: 추후 각 H2 하위에 PDF 컨텐츠를 추가할 수 있도록 구조만 생성

6. /programs/`extract_pdf_text.py`: PDF 파일에서 텍스트와 표를 추출하여 마크다운 형식으로 변환하는 Python 프로그램
   - input: public/resource/itscope_pmo_manual.pdf
   - output: itscope_pmo_manual.txt
   - 기능:
      - PDF의 표를 마크다운 테이블로 변환
      - 리스트(불릿/번호) 항목을 마크다운 리스트로 변환
      - 5페이지부터 끝까지 처리
   - 제약사항: 텍스트와 표를 구분하여 추출

7. /programs/`format_md_files.py`: 마크다운 파일의 구조를 정리하는 Python 프로그램
   - input: md_output/*.md
   - output: md_output/*.md (같은 파일에 덮어쓰기)
   - 기능:
      - 리스트(불릿/번호) 계층 구조 정리
      - 표와 일반 텍스트, 리스트 간 구분을 위한 빈 줄 추가
      - 들여쓰기 정규화
   - 제약사항: 파일별로 정리된 결과를 다시 저장

8. /programs/`pdf_to_markdown.py`: 텍스트 파일을 목차 구조에 따라 마크다운 파일로 분할하는 Python 프로그램
   - input: itscope_pmo_manual.txt
   - output: md_output/*.md
   - 기능:
      - 목차 패턴 인식 및 트리 구조화
      - 4레벨까지는 별도 파일로, 5레벨부터는 상위 파일에 포함
      - 각 노드별로 제목, 내용, 하위 목차를 마크다운으로 저장
   - 제약사항: 5레벨 이상은 상위 파일에 포함

9. /programs/`format_bullet_md.py`: 마크다운 파일 내 특수문자 bullet(⚫, ✓ 등)을 마크다운 bullet(-)로 변환하고, 계층에 따라 들여쓰기를 적용하는 Python 프로그램
   - input: public/02_outputs/manual_md/*.md 또는 파일 지정
   - output: 같은 파일에 덮어쓰기
   - 기능:
     - ⚫, ●, ■, ▪ 등은 상위 bullet로 `-`로 변환
     - ✓, ✔, ☑ 등은 하위 bullet로 `  -`(2칸 들여쓰기)로 변환
     - 기타 줄은 그대로 유지
     - 명령행 인자로 파일 경로를 지정하면 해당 파일만 변환, 인자가 없으면 전체 디렉토리 일괄 변환

## 2. Functional Requirements

### 2.1. Manual Features

- [FR01] `public/02_outputs/manual_toc_json.json` 파일의 menu tree를 바탕으로 `left_menu` 영역에 사용자가 접기/펼치기 가능한 트리 구조로 메뉴 UI를 구성
   - [FR01-01] `left_menu`에 표시할 메뉴 트리는 최대 4레벨(예. 2.2.1.1)까지 구성
      - 메뉴 항목 선택 시 접기/펼치기(collapse/expand) 대상 항목:
         - 1~3 레벨이며, 하위메뉴(child)를 가질 경우
      - 메뉴 항목 선택 시 해당 md 파일을 열람하는 항목:
         - 4레벨 항목은 모든 경우에 md 파일 열람 (collapse/expand 없음)
         - 1에서 3레벨의 경우에도 leaf일 경우 md 파일 열람 (collapse/expand 없음)
      - 어떠한 경우에도 5레벨(예. 2.2.2.1.1.md)을 `left_menu` 내 메뉴 트리에 렌더링하지 않음
   - [FR01-02] 트리 구조는 계단식으로 아래로 펼쳐지며, caret(>) 아이콘으로 접기/펼치기 상태를 표시
   - [FR01-03] 각 레벨별 들여쓰기, 줄간격, 폰트 크기, 높이 등은 일관성 있게 적용
   - [FR01-04] 1레벨 메뉴는 bold, 2레벨 이하 메뉴는 normal weight
   - [FR01-05] 메뉴 트리와 컨텐츠 영역은 리사이저(divider)로 구분되며, 사용자가 드래그하여 left_menu의 width를 동적으로 조절할 수 있음 (최소/최대 폭 제한)
   - [FR01-06] 메뉴 트리의 오른쪽 padding은 최소화
   - [FR01-07] left_menu와 content_area는 각각 독립적인 스크롤바를 가짐

- [FR02] 메뉴 내 텍스트 기반 검색 기능 제공
   - [FR02-01] 검색창에 키워드 입력 후 엔터키 또는 돋보기 버튼 클릭으로 검색 실행
   - [FR02-02] 검색 결과는 `left_menu`에서 해당 키워드를 제목에 포함하는 메뉴 항목만 표시 (4레벨까지만 탐색)
   - [FR02-03] 검색 결과가 없을 경우 트리 영역에 "검색 결과가 없습니다." 텍스트로 안내
   - [FR02-04] 검색 input에 텍스트 입력 시 X(지우기) 버튼이 동적으로 표시되며, 클릭 시 전체 트리로 복원
   - [FR02-05] 검색 결과가 있을 때, 해당 항목 및 부모 트리만 표시 (트리 구조 유지)

- [FR03] `left_menu` 내 메뉴 트리에서 md 파일을 열람하는(i.e., collapse/expand 없는) 목차 항목을 선택했을 경우, `content_area`에 해당 md파일을 로드 및 렌더링
   - [FR03-01] /public/02_outputs/manual_md 내의 markdown 파일 중 해당 번호에 맞는 `x.x.x.x.md` 파일을 열람
   - [FR03-01-1] 브라우저 주소창의 해시(URL #)를 통해 md 파일을 직접 지정해서 열 수 있음 (예: `http://localhost:8000/src/#2.2.2.1` → 2.2.2.1.md 자동 오픈)
   - [FR03-01-2] 메뉴 클릭 시 해시가 해당 파일명(확장자 없는 부분)으로 자동 갱신되며, 새로고침 시에도 같은 md 파일이 열림
   - [FR03-02] md 파일 내 최상단에 breadcrumb(트리 경로)가 표시되며, 중간 회색 스타일로 렌더링
   - [FR03-03] md 파일 내 이미지(스크린샷)는 반응형(width 100%), border(타이틀바 색상), border-radius, margin, hover 효과가 적용됨
   - [FR03-04] md 내 스크린샷 이미지를 클릭하면 원본 이미지를 팝업(모달)으로 띄움, 팝업 클릭 시 닫힘
   - [FR03-05] bullet, numbered list 등은 content area 내에서 적절한 들여쓰기가 적용됨
   - [FR03-06] H1, H2, H3 등 제목의 폰트 크기는 기본 대비 70%로 축소
   - [FR03-07] content area의 왼쪽 padding이 충분히 적용됨

- [FR04] 인쇄 기능
   - [FR04-01] 타이틀바 우측에 "PRINT" 버튼이 있으며, 클릭 시 content_area만 인쇄됨 (나머지 UI는 숨김)
   - [FR04-02] 인쇄 버튼은 작고 modern한 스타일로 제공

- [FR05] 반응형 및 접근성
   - [FR05-01] 화면 크기에 따라 left_menu와 content_area가 세로/가로로 유연하게 배치됨
   - [FR05-02] 모든 버튼, 입력창 등은 키보드 접근성 및 포커스 스타일을 지원

## 3. Non-Functional Requirements

### 3.1. User Interface

- [NFR01] 깔끔하고 현대적인 UI/UX 제공
   - [NFR01-01] 최소한의 외부 UI 라이브러리 사용
   - [NFR01-02] 기본적인 반응형 디자인 적용 (화면 크기에 따른 레이아웃 조정)
   - [NFR01-03] 가독성 높은 Modern UI 기반의 SPA로 구성
   - [NFR01-04] MainColor(#1E88E5)를 기본 테마 색상으로 사용
      - 타이틀바 배경색
      - 하이퍼링크 텍스트 색상
      - 버튼 배경색
      - 강조 요소 등에 일관되게 적용

- [NFR02] UI는 크게 두 가지 영역으로 구분
   - `left_menu`: 왼편의 사이드메뉴로써, 메뉴 트리를 포함
   - `content_area`: 메뉴 트리 내에서 선택한 항목을 열람하고 컨텐츠를 출력하는 영역
- [NFR03] 타이틀바는 항상 상단에 고정되어 있으며, 좌측에는 로고, 중앙에는 타이틀, 우측에는 PRINT 버튼이 배치됨
- [NFR04] left_menu와 content_area는 각각 독립적인 스크롤바를 가짐
- [NFR05] 바닥글(footer)은 별도로 제공하지 않음

### 3.2. 기타

- 현재 단계에서 모바일 운영 환경은 고려하지 않음
- 현재 단계에서 다국어 지원은 고려하지 않음

## 4. Constraints

- 본 프로젝트는 PDF 기반 매뉴얼을 웹에서 markdown 및 메뉴 트리 구조로 제공하며, 최대 4레벨까지의 목차만 탐색·렌더링·검색 대상으로 한다.
   - 본 문서에서 말하는 목차의 레벨은 다음과 같이 정의:
(아래는 예시이며, 실제 존재하지 않는 목차일 수 있음)
      - 1레벨: 1
      - 2레벨: 1.1
      - 3레벨: 1.1.1
      - 4레벨: 1.1.1.1
      - 5레벨: 1.1.1.1.1
- 5레벨 이상의 목차는 메뉴 트리 및 검색, 렌더링에서 모두 제외한다.
- 메뉴 트리, 검색, 인쇄, breadcrumb, 반응형, 리사이저, 이미지 팝업 등 모든 UI/UX 및 기능 요구사항은 본 문서에 명시된 대로 구현되어야 하며, 누락 없이 반영해야 한다.
- index.html은 public/src에 위치하며, 반드시 로컬 웹서버 환경(예: python -m http.server)에서 http://localhost:8000/src/로 접근해야 정상 동작한다. (브라우저 파일 직접 열기 불가)
- 모바일 환경 및 다국어 지원, PDF 처리, 보안, 테스트 등은 현재 범위에서 고려하지 않는다.
- 모든 주요 기능 및 구조, UI/UX, 성능, 인쇄, breadcrumb, 반응형, 리사이저, 이미지 팝업 등은 실제 구현된 대로 명확하게 문서화되어야 한다.
- URL 해시(#)를 통해 원하는 md 파일을 직접 지정해서 열람할 수 있다. (예: `http://localhost:8000/src/#2.2.2.1`)

## 5. Project Deliverables

- 완성된 온라인 매뉴얼 웹 앱
- 완성된 소스코드
- 문서화된 요구사항 및 설계 문서
- 테스트 계획 및 결과 보고서