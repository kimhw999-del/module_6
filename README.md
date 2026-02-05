# 배당 ETF 대시보드 💰

실시간 배당 ETF 정보를 시각화하고 분석하는 **사용자 정의 가능한** 종합 대시보드입니다. 50개 이상의 배당 ETF 데이터를 제공하며, 투자 전략, 보유 종목, 수익률 등을 한눈에 확인할 수 있습니다.

## ✨ 주요 특징

### 🎛️ 편집 가능한 대시보드
- **드래그 앤 드롭**: 위젯 순서를 자유롭게 변경
- **위젯 관리**: 원하는 위젯만 표시/숨김
- **자동 저장**: 레이아웃 설정이 브라우저에 저장
- **초기화**: 원클릭으로 기본 레이아웃 복원

### 📊 ETF 테이블
- **미니 타임라인 차트**: 1주일 가격 추이 시각화
- **컬럼 커스터마이징**: 원하는 컬럼만 선택 표시
- **상세 정보 모달**: 티커 클릭 시 투자 전략 및 보유 종목 표시
- **검색 및 정렬**: 실시간 검색, 모든 컬럼 정렬 가능

### 📈 성과 비교 차트
- **다중 비교**: 최대 8개 ETF 동시 비교
- **빠른 선택**: 높은 배당률/수익률 TOP 5
- **차트/테이블 뷰**: 토글로 전환
- **섹터 필터링**: 특정 섹터만 선택

### 📅 배당 캘린더
- **월별 캘린더**: 월/연도 선택기
- **다가오는 배당**: 향후 30일 일정
- **임박 알림**: 7일 이내 배당 강조
- **월별 통계**: 배당 건수, 평균 수익률, 총액

### 🥧 섹터/지역 분산
- **도넛 차트**: 섹터 또는 지역별 분포
- **상세 통계**: 총 ETF, 카테고리 수, 최대 비중
- **다양성 평가**: 우수/적정/낮음 자동 평가
- **개수/비율 전환**: 토글로 표시 방식 변경

### 🏆 추가 위젯
- **수익률 랭킹**: 일간/주간/월간/연간 TOP 5
- **포트폴리오 요약**: 투자 현황 및 예상 배당금
- **디버그 정보**: API 상태 실시간 모니터링

## 🛠️ 기술 스택

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Language**: TypeScript
- **UI Library**: Vuetify 3
- **Styling**: Tailwind CSS
- **Charts**: Chart.js + vue-chartjs
- **Utilities**: @vueuse/core
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Validation**: Pydantic

## 설치 및 실행

### 백엔드 설정

```bash
cd backend

# 가상환경 생성 및 활성화 (Windows)
python -m venv .venv
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 샘플 데이터 초기화 (최초 1회 실행)
python -m app.init_sample_data

# 서버 실행 (http://localhost:8000)
uvicorn app.main:app --reload
```

### 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행 (http://localhost:5173)
npm run dev
```

## 📋 주요 기능

### 0. 편집 가능한 대시보드 (Dashboard.vue) 🆕

#### 위젯 관리
- **표시/숨김 토글**: 원하는 위젯만 선택하여 표시
- **체크박스 UI**: 직관적인 ON/OFF 전환
- **실시간 적용**: 즉시 대시보드에 반영

#### 드래그 앤 드롭
- **순서 변경**: 위젯을 드래그하여 순서 조정
- **편집 모드**: "편집" 버튼으로 활성화
- **시각적 피드백**: 드래그 중 반투명 표시

#### 자동 저장
- **localStorage 저장**: 위젯 순서와 가시성 자동 저장
- **새로고침 유지**: 브라우저 재시작 후에도 설정 유지
- **버전 관리**: `dashboard-widgets-v2` 키로 관리

#### 레이아웃 복원
- **기본값 복원**: 원클릭으로 초기 레이아웃
- **확인 다이얼로그**: 실수 방지

### 1. ETF 테이블 (ETFTable.vue)

#### 기본 기능
- **검색**: 티커, 이름, 섹터 등 전체 텍스트 검색
- **정렬**: 모든 컬럼 클릭으로 정렬 가능
- **페이지네이션**: 10/20/50/100개 또는 전체 표시 선택
- **반응형**: 모바일/태블릿/데스크톱 최적화

#### 고급 기능
- **미니 타임라인 차트** 🆕
  - 각 ETF의 1주일 가격 추이를 미니 차트로 표시
  - 상승 추세는 초록색, 하락 추세는 빨간색
  - 마우스 오버 시 일별 가격 정보 툴팁

- **컬럼 표시 설정** 🆕
  - 사용자가 원하는 컬럼만 선택하여 표시
  - 설정은 브라우저 localStorage에 자동 저장
  - 티커/이름은 필수 컬럼으로 항상 표시

- **상세 정보 다이얼로그** 🆕
  - 티커 클릭 시 상세 정보 모달 표시
  - 투자 전략: ETF의 운용 방식 및 목표 설명
  - 상위 보유 종목: TOP 10 종목 및 비중
  - 도넛 차트: 보유 종목 비중 시각화
  - 주요 지표: 현재가, 배당수익률, 수익률, 운용자산

### 2. 성과 비교 차트 (PerformanceComparison.vue) 🆕

#### 다중 ETF 비교
- **최대 8개**: 여러 ETF 동시 비교
- **선택 UI**: 클릭으로 간편하게 추가/제거
- **색상 구분**: 각 ETF별 고유 색상

#### 빠른 선택
- **높은 배당률 TOP 5**: 원클릭으로 선택
- **높은 수익률 TOP 5**: 원클릭으로 선택
- **초기화**: 선택 해제

#### 필터링 및 검색
- **섹터 필터**: 드롭다운으로 섹터 선택
- **실시간 검색**: 티커/이름으로 검색
- **동적 필터링**: 검색 결과만 표시

#### 차트/테이블 뷰
- **라인 차트**: 시간대별 수익률 비교
- **테이블 뷰**: 모든 기간 한눈에 비교
- **평균 통계**: 선택된 ETF들의 평균 계산

### 3. 배당 캘린더 (DividendCalendar.vue) 🆕

#### 월별 캘린더
- **월/연도 선택**: 드롭다운으로 기간 선택
- **월별 통계**: 배당 건수, 평균 수익률, 총 배당금
- **타임라인 UI**: 시각적으로 일정 표시

#### 다가오는 배당
- **향후 30일**: 다가오는 배당 일정만 표시
- **임박 알림**: 7일 이내 배당락일 강조 (초록색)
- **뷰 전환**: 캘린더 ↔ 다가오는 배당

#### 배당 정보
- **배당락일**: Ex-Dividend Date
- **지급일**: Payment Date
- **주당 배당금**: 금액 표시
- **배당 주기**: 월/분기/연 표시

### 4. 섹터/지역 분산 (SectorAllocation.vue) 🆕

#### 도넛 차트
- **섹터 ↔ 지역**: 토글 버튼으로 전환
- **중앙 통계**: 총 ETF 개수 표시
- **색상 구분**: 10가지 색상으로 분류

#### 통계 카드
- **총 ETF 개수**: 전체 ETF 수
- **카테고리 수**: 섹터/지역 개수
- **최대 비중**: 가장 많은 카테고리 및 비율

#### 상세 분포
- **프로그레스 바**: 비율 시각화
- **개수/비율 토글**: 표시 방식 전환
- **정렬**: 비중 순으로 자동 정렬

#### 다양성 지표
- **우수**: 5개 이상 카테고리
- **적정**: 3~4개 카테고리
- **낮음**: 2개 이하 카테고리

### 5. 수익률 랭킹 (ReturnRanking.vue)
- 일간/주간/월간/연간 수익률 TOP 5
- 배당 수익률 TOP 5
- 색상 코딩으로 수익률 직관적 표시

### 6. 포트폴리오 요약 (PortfolioSummary.vue)
- 총 투자금액 vs 현재 평가금액
- 실현/미실현 손익
- 월간 예상 배당금
- 수익률 게이지 차트

### 7. 디버그 정보 (DebugInfo.vue)
- API 상태 실시간 모니터링
- 연결 상태 표시
- 에러 메시지 표시


## 🌐 API 엔드포인트

백엔드 실행 후 **Swagger UI**: http://localhost:8000/docs

### ETF API (`/api/etfs`)
- `GET /api/etfs` - 전체 ETF 목록 조회
- `GET /api/etfs/{etf_id}` - ETF 상세 정보 조회 (투자 전략, 보유 종목 포함)
- `POST /api/etfs` - ETF 생성
- `GET /api/etfs/ranking/return/{period}` - 수익률 랭킹 (1d/1w/1m/1y)
- `GET /api/etfs/ranking/dividend` - 배당 수익률 랭킹
- `GET /api/etfs/sector/allocation` - 섹터별 분산도
- `GET /api/etfs/region/allocation` - 지역별 분산도

### Portfolio API (`/api/portfolios`)
- `GET /api/portfolios` - 보유 ETF 목록
- `GET /api/portfolios/summary` - 포트폴리오 요약 통계

### Dividend API (`/api/dividends`)
- `GET /api/dividends/calendar` - 배당 캘린더
- `GET /api/dividends/upcoming` - 다가오는 배당 일정

## 💾 데이터베이스 스키마

### ETF Table
```python
- id: Integer (PK)
- ticker: String (Unique)
- name: String
- current_price: Float
- previous_price: Float
- dividend_yield: Float
- expense_ratio: Float
- aum: Float (운용자산)
- volume: Integer
- sector: String
- region: String
- return_1d/1w/1m/1y: Float (수익률)
- investment_strategy: Text 🆕 (투자 전략)
- top_holdings: JSON 🆕 (상위 보유 종목)
- created_at: DateTime
- updated_at: DateTime
```

### Portfolio Table
```python
- id: Integer (PK)
- etf_id: Integer (FK)
- shares: Integer
- avg_price: Float
- total_invested: Float
```

### Dividend Table
```python
- id: Integer (PK)
- etf_id: Integer (FK)
- ex_dividend_date: Date
- payment_date: Date
- dividend_per_share: Float
- frequency: String (monthly/quarterly)
```

## 📁 프로젝트 구조

```
module_6/
├── frontend/                           # Vue 3 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   │   ├── widgets/
│   │   │   │   ├── ETFTable.vue       # 🆕 ETF 목록 테이블 (미니차트, 상세정보)
│   │   │   │   ├── ReturnRanking.vue  # 수익률 랭킹
│   │   │   │   ├── PortfolioSummary.vue  # 포트폴리오 요약
│   │   │   │   ├── DividendCalendar.vue  # 배당 캘린더
│   │   │   │   ├── SectorAllocation.vue  # 섹터 분산
│   │   │   │   └── PerformanceComparison.vue  # 성과 비교
│   │   │   └── DebugInfo.vue
│   │   ├── views/
│   │   │   └── Dashboard.vue          # 메인 대시보드
│   │   ├── services/
│   │   │   └── api.ts                 # API 클라이언트
│   │   ├── types/
│   │   │   └── index.ts               # 🆕 TypeScript 타입 정의
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                            # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py                    # FastAPI 앱 진입점
│   │   ├── database.py                # SQLAlchemy 설정
│   │   ├── models/
│   │   │   ├── etf.py                 # 🆕 ETF 모델 (투자전략, 보유종목)
│   │   │   ├── portfolio.py
│   │   │   └── dividend.py
│   │   ├── schemas/
│   │   │   ├── etf.py                 # 🆕 ETF 스키마 (Holding 타입)
│   │   │   ├── portfolio.py
│   │   │   └── dividend.py
│   │   ├── routers/
│   │   │   ├── etfs.py                # ETF API 라우터
│   │   │   ├── portfolios.py
│   │   │   └── dividends.py
│   │   └── init_sample_data.py        # 🆕 샘플 데이터 (투자전략 포함)
│   ├── requirements.txt
│   └── app.db                         # SQLite 데이터베이스
│
├── .claude/
│   ├── docs/
│   │   └── progress.md                # 작업 진행 상황
│   └── skills/
│       └── git_commit/                # Git 커밋 워크플로우
│
├── CLAUDE.md                          # Claude Code 가이드
├── README.md
└── task.md                            # 태스크 목록
```

## 🚀 빠른 시작

### 1. 백엔드 설정 및 실행

```bash
cd backend

# 가상환경 생성 (최초 1회)
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 샘플 데이터 초기화 (최초 1회)
python -m app.init_sample_data

# 서버 실행
uvicorn app.main:app --reload
```

**Backend**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### 2. 프론트엔드 설정 및 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**Frontend**: http://localhost:5173

## 💡 개발 가이드

### 새로운 위젯 추가하기

1. `frontend/src/components/widgets/` 에 컴포넌트 생성
2. `Dashboard.vue`에 import 및 배치
3. 필요 시 API 엔드포인트 추가

### 데이터베이스 스키마 변경

1. `backend/app/models/` 에서 모델 수정
2. `backend/app/schemas/` 에서 스키마 수정
3. 기존 `app.db` 삭제
4. `python -m app.init_sample_data` 재실행

### 새로운 ETF 추가

`backend/app/init_sample_data.py`의 `sample_etfs` 리스트에 추가:

```python
{
    "ticker": "SPY",
    "name": "SPDR S&P 500 ETF Trust",
    "current_price": 450000,
    "dividend_yield": 1.5,
    # ... 기타 필드
    "investment_strategy": "S&P 500 지수를 추종하는...",
    "top_holdings": [
        {"name": "Apple Inc.", "weight": 7.2},
        {"name": "Microsoft Corp.", "weight": 6.5},
        # ...
    ]
}
```

## 📊 샘플 데이터

- **ETF**: 50개 이상의 실제 배당 ETF (JEPQ, QYLD, SCHD, VYM, SPYD 등)
- **포트폴리오**: 5개 ETF 보유 샘플
- **배당 일정**: 15개 배당 스케줄

일부 주요 ETF에는 실제 투자 전략 및 상위 보유 종목 데이터 포함

## 🔧 기술적 특징

- **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원
- **타입 안정성**: TypeScript로 타입 검증
- **데이터 지속성**: localStorage로 사용자 설정 저장
- **실시간 차트**: Chart.js 활용한 동적 시각화
- **비동기 처리**: FastAPI의 async/await 활용
- **자동 리로드**: Vite HMR + Uvicorn --reload

## 📝 라이센스

MIT License

## 🤝 기여

이슈 및 PR은 언제나 환영합니다!

---

**Repository**: https://github.com/kimhw999-del/module_6
**Last Updated**: 2026-02-05
