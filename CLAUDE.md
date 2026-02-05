# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

배당 ETF 대시보드 - 사용자 정의 가능한 위젯 기반 대시보드로 ETF 수익률, 배당 정보, 포트폴리오 현황 등을 시각화합니다.

## 기술 스택

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Language**: TypeScript
- **UI Framework**: Vuetify 3
- **Styling**: Tailwind CSS
- **Charts**: Chart.js + vue-chartjs
- **Utilities**: @vueuse/core
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: SQLite

## 주요 명령어

### Quick Start

```bash
# Backend (localhost:8000)
cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload

# Frontend (localhost:5173)
cd frontend && npm run dev
```

### 개발 환경 설정

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.init_sample_data  # 샘플 데이터 생성

# Frontend
cd frontend
npm install
```

## 프로젝트 구조

```
module_6/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── widgets/
│   │   │   │   ├── ETFTable.vue           # ETF 목록 테이블 (미니차트, 상세정보)
│   │   │   │   ├── PerformanceComparison.vue  # 성과 비교 차트
│   │   │   │   ├── DividendCalendar.vue   # 배당 캘린더
│   │   │   │   ├── SectorAllocation.vue   # 섹터/지역 분산
│   │   │   │   ├── ReturnRanking.vue      # 수익률 랭킹
│   │   │   │   └── PortfolioSummary.vue   # 포트폴리오 요약
│   │   │   └── DebugInfo.vue
│   │   ├── views/
│   │   │   └── Dashboard.vue          # 메인 대시보드 (위젯 관리)
│   │   ├── services/
│   │   │   └── api.ts                # API 클라이언트
│   │   └── types/
│   │       └── index.ts              # TypeScript 타입 정의
│   └── package.json
│
└── backend/
    ├── app/
    │   ├── main.py                   # FastAPI 앱 진입점
    │   ├── database.py               # SQLAlchemy 설정
    │   ├── models/
    │   │   ├── etf.py               # ETF 모델 (투자전략, 보유종목)
    │   │   ├── portfolio.py
    │   │   └── dividend.py
    │   ├── schemas/
    │   │   ├── etf.py               # ETF 스키마
    │   │   ├── portfolio.py
    │   │   └── dividend.py
    │   ├── routers/
    │   │   ├── etfs.py              # ETF API 라우터
    │   │   ├── portfolios.py
    │   │   └── dividends.py
    │   └── init_sample_data.py      # 샘플 데이터 생성
    └── requirements.txt
```

## 주요 기능

### 1. 편집 가능한 대시보드
- **위젯 관리**: 표시/숨김 토글
- **드래그 앤 드롭**: 위젯 순서 변경
- **레이아웃 저장**: localStorage에 자동 저장
- **초기화**: 기본 레이아웃으로 복원

### 2. ETF 테이블 (ETFTable.vue)
- **검색 및 정렬**: 티커, 이름, 섹터 등 전체 검색
- **미니 타임라인 차트**: 1주일 가격 추이 시각화
- **컬럼 커스터마이징**: 사용자가 원하는 컬럼만 표시
- **상세 정보 다이얼로그**:
  - 티커 클릭 시 모달 표시
  - 투자 전략 설명
  - 상위 보유 종목 TOP 10 (도넛 차트)
  - 주요 지표 요약

### 3. 성과 비교 차트 (PerformanceComparison.vue)
- **다중 ETF 비교**: 최대 8개 동시 비교
- **빠른 선택**: 높은 배당률/수익률 TOP 5
- **검색 및 필터**: 섹터별 필터링
- **차트/테이블 뷰**: 토글 전환
- **평균 수익률 통계**: 선택된 ETF들의 평균 계산

### 4. 배당 캘린더 (DividendCalendar.vue)
- **월별 캘린더**: 월/연도 선택
- **다가오는 배당**: 향후 30일 이내 일정
- **임박 알림**: 7일 이내 배당락일 강조
- **월별 통계**: 배당 건수, 평균 수익률, 총 배당금
- **타임라인 UI**: 시각적으로 일정 표시

### 5. 섹터/지역 분산 (SectorAllocation.vue)
- **섹터 ↔ 지역 전환**: 토글 버튼
- **도넛 차트**: 중앙에 총 ETF 개수 표시
- **통계 카드**: 총 ETF, 카테고리 수, 최대 비중
- **상세 분포**: 프로그레스 바 + 개수/비율 토글
- **다양성 지표**: 우수/적정/낮음 평가

### 6. 수익률 랭킹 (ReturnRanking.vue)
- 일간/주간/월간/연간 수익률 TOP 5
- 배당 수익률 TOP 5
- 색상 코딩으로 직관적 표시

### 7. 포트폴리오 요약 (PortfolioSummary.vue)
- 총 투자금액 vs 현재 평가금액
- 실현/미실현 손익
- 월간 예상 배당금
- 수익률 게이지 차트

## API 엔드포인트

### ETF API
- `GET /api/etfs` - 전체 ETF 목록
- `GET /api/etfs/{id}` - ETF 상세 정보 (투자전략, 보유종목)
- `GET /api/etfs/ranking/return/{period}` - 수익률 랭킹
- `GET /api/etfs/ranking/dividend` - 배당 수익률 랭킹
- `GET /api/etfs/sector/allocation` - 섹터별 분산도
- `GET /api/etfs/region/allocation` - 지역별 분산도

### Portfolio API
- `GET /api/portfolios` - 보유 ETF 목록
- `GET /api/portfolios/summary` - 포트폴리오 요약

### Dividend API
- `GET /api/dividends/calendar` - 배당 캘린더
- `GET /api/dividends/upcoming` - 다가오는 배당 일정

**API 문서**: http://localhost:8000/docs

## 데이터베이스 스키마

### ETF 테이블
- 기본 정보: ticker, name, current_price, dividend_yield
- 수익률: return_1d, return_1w, return_1m, return_1y
- 상세 정보: investment_strategy, top_holdings (JSON)
- 기타: sector, region, expense_ratio, aum, volume

### Portfolio 테이블
- etf_id (FK), shares, avg_price, total_invested

### Dividend 테이블
- etf_id (FK), ex_dividend_date, payment_date
- dividend_per_share, frequency

## 개발 가이드

### 컴포넌트 개발
```typescript
// markRaw로 컴포넌트를 반응형에서 제외
import { markRaw } from 'vue'
import MyComponent from './MyComponent.vue'

const widgets = ref([
  {
    component: markRaw(MyComponent)  // 중요!
  }
])
```

### localStorage 사용
```typescript
// 위젯 설정 저장
const WIDGETS_KEY = 'dashboard-widgets-v2'
localStorage.setItem(WIDGETS_KEY, JSON.stringify(data))
```

### 차트 구현
```typescript
// Chart.js 등록
import { Chart as ChartJS, ... } from 'chart.js'
ChartJS.register(...)

// 도넛 차트에 markRaw 사용
import { Doughnut } from 'vue-chartjs'
```

## 코딩 규칙

### 일반 원칙
- 간결하고 읽기 쉬운 코드
- 필요한 기능만 구현 (over-engineering 지양)
- 타입 힌트 사용 (Python, TypeScript)
- 의미 있는 변수명/함수명

### Vue 3 특화
- Composition API 사용
- `markRaw`로 컴포넌트 래핑
- `computed`로 파생 상태 관리
- `watch`로 부수 효과 처리

### 상태 관리
- localStorage로 사용자 설정 저장
- ref/reactive로 로컬 상태 관리
- props/emit으로 부모-자식 통신

## 샘플 데이터

- **ETF**: 50개 이상 실제 배당 ETF
- **주요 ETF**: JEPQ, QYLD, SCHD (투자전략 포함)
- **포트폴리오**: 5개 ETF 보유 샘플
- **배당 일정**: 15개 배당 스케줄

## 참고사항

- Vue 컴포넌트는 반드시 `markRaw`로 래핑
- localStorage 키는 버전 관리 (`-v2` 접미사)
- Chart.js는 사용 전 등록 필요
- 편집 모드는 네이티브 드래그 앤 드롭 사용
