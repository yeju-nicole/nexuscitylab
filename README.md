# 넥서스도시랩 홈페이지

주식회사 넥서스도시랩 공식 홈페이지 (정적 웹사이트, GitHub Pages로 운영)

## 페이지 구성

| 메뉴 | 파일 |
|---|---|
| 홈 | `index.html` |
| 회사소개 · 개요 / 인사말 / 비전·강점 / 협력기관 | `about.html` `greeting.html` `vision.html` `partners.html` |
| 사업소개 · 사업영역 5개 + 수행 프로세스 | `business.html` |
| 연혁 | `history.html` |
| 실적 · 41건 (분야·연도·검색 필터) | `records.html` |
| 문의 · 오시는 길 / 과업 문의 | `contact.html` |

`assets/` 폴더에 CSS, JS, 로고, 협력기관 로고가 있습니다.

## 1. GitHub Pages로 공개하기 (처음 한 번)

1. 저장소 `nexuscitylab` 첫 화면에서 **Add file → Upload files**
2. 압축을 푼 폴더 **안의 내용 전체**(index.html, assets 폴더 등)를 끌어다 놓기
   - `.nojekyll`처럼 점으로 시작하는 파일은 숨김 파일이라 안 보일 수 있습니다. 없어도 사이트는 동작합니다.
3. 아래 **Commit changes** 클릭
4. 저장소 **Settings → Pages**
   - Source: **Deploy from a branch**
   - Branch: **main** / 폴더 **/(root)** → **Save**
5. 1~3분 뒤 같은 화면 위쪽에 주소가 나타납니다: `https://yeju-nicole.github.io/nexuscitylab/`

> 무료 계정에서는 저장소가 **Public**이어야 Pages가 켜집니다. (Settings → General 맨 아래 Danger Zone → Change visibility)

## 2. 도메인 연결 (도메인 구입 후)

예: `nexuscitylab.kr`

1. **Settings → Pages → Custom domain**에 `www.nexuscitylab.kr` 입력 → Save
2. 도메인 구입처(가비아 등) DNS 관리에서 레코드 추가

   | 타입 | 호스트 | 값 |
   |---|---|---|
   | CNAME | www | `yeju-nicole.github.io` |
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |

3. DNS 반영 후(수십 분~최대 하루) **Enforce HTTPS** 체크

## 3. 내용 수정

- 문구 몇 개만 바꿀 때: GitHub에서 해당 `.html` 파일 열기 → 연필 아이콘 → 수정 → Commit
- 메뉴·푸터처럼 모든 페이지에 공통인 부분이나 실적 목록을 바꿀 때: `_build/build.py`(내용) 또는 `_build/records.json`(실적)을 고친 뒤 `python3 _build/build.py`를 실행하면 모든 페이지가 다시 만들어집니다.

## 아직 비어 있는 정보

회사소개서에 없던 항목은 화면에 넣지 않았습니다. 정해지면 추가하세요: 대표 이메일, 사업자등록번호, 사옥·현장 사진, 회사소개서 PDF.
