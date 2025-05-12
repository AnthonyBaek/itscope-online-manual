# Project Requirements

## 0. Project Overview

## 1. Environment & Assumptions

### 1.1. Terms

- `tocraw`: PDF 파일에서 추출한 목차(toc)의 raw 파일을 의미
- `menutree`: 추출한 `tocraw`를 기반으로 매뉴얼 내에서 사용 될(및 렌더링 될) 트리 형태의 메뉴 데이터 구조
- `left_menu`: 매뉴얼 앱의 왼편 사이드메뉴로, PDF로부터 추출한 `menutree`를 트리 형태로 렌더링하고, 우측 `content_area`에 해당 메뉴의 md파일을 열 수 있도록 트리 내 링크를 제공
- `content_area`: 매뉴얼 컨텐츠를 보여주는 영역으로, 해당 목차 번호에 맞는 마크다운(`*.md`) 파일을 렌더링하여 출력

### 1.2. Project Structure

- `/programs`: 입력(/public/01_inputs/) 파일을 대상으로 `tocraw`와 `menutree`를 추출하기 위한 파이썬 프로그램
- `public`
   - `01_inputs`: 프로그램 및 웹 앱이 사용하는 입력 파일
   - `02_outputs`: 프로그램 및 웹 앱에 의해 생성되는 산출물 및 기타 출력 파일
   - `03_resources`: 앱 내에서 사용될 정적 자원 (이미지 리소스 등)
   - `src`: 프로젝트 소스코드 관리 디렉토리 (html, css, js, ts 등)

### 1.3. Running Environment

- 완성된 HTML 기반의 온라인 매뉴얼은 기타 파일들과 함께 GitHub Pages를 통해 사용자에게 배포
- Chrome 및 Firefox 등의 데스크톱 웹브라우저에서 문제없이 실행되어야 함
- 현재 단계에서 모바일 운영 환경은 고려하지 않음
- 현재 단계에서 다국어 지원은 고려하지 않음

### 1.4. Programs

1. /programs/`extract_tocraw_from_pdf.py`: PDF 파일(public\01_inputs\itscope_pmo_manual.pdf)을 읽어, `tocraw`를 추출하는 Python 프로그램
   - input: public/01_inputs/itscope_pmo_manual.pdf
   - output: public/02_outputs/manual_toc_raw.md

2. /programs/`generate_menu_json_from_tocraw.py`: 

3. /programs/`generate_menu_md_from_tocraw.py`

## 2. Functional Requirements

## 3. Non-Functional Requirements

## 4. Constraints