# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

배당 ETF 대시보드 - 여러 위젯으로 구성된 대시보드로 ETF 수익률, 배당 정보, 포트폴리오 현황 등을 시각화합니다.

## 기술 스택

- **Frontend**: Vue 3 + Vite + TypeScript + Tailwind CSS
- **Chart Library**: Vue-ChartJS (Chart.js wrapper)
- **UI Framework**: Vuetify
- **Backend**: Python 3.12 + FastAPI
- **Database**: SQLite (SQLAlchemy ORM)

## 주요 명령어

### Quick Start

```bash
# Backend (localhost:8000)
cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload

# Frontend (localhost:5173)
cd frontend && npm run dev
```

## 프로젝트 구조

```
module_6/
├── frontend/           # Vue 3 프론트엔드
│   ├── src/
│   │   ├── components/ # 위젯 컴포넌트
│   │   ├── views/      # 페이지
│   │   ├── services/   # API 호출
│   │   ├── types/      # TypeScript 타입
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.ts
│
└── backend/            # FastAPI 백엔드
    ├── app/
    │   ├── main.py          # FastAPI 앱 진입점
    │   ├── database.py      # SQLAlchemy 설정
    │   ├── models/          # ORM 모델
    │   ├── schemas/         # Pydantic 스키마
    │   └── routers/         # API 엔드포인트
    └── requirements.txt
```

## 주요 기능

### 대시보드 위젯

1. **수익률 랭킹**
   - 일간/주간/월간/연간 수익률 TOP 5
   - 배당 수익률 TOP 5

2. **포트폴리오 요약**
   - 총 투자금액 / 평가금액
   - 실현/미실현 손익
   - 월간 예상 배당금

3. **배당 캘린더**
   - 배당락일, 지급일 표시
   - 월별 배당 스케줄

4. **섹터/지역 분산**
   - 파이 차트로 섹터별 비중
   - 지역별 분산도

5. **개별 ETF 상세 카드**
   - 현재가, 변동률, 거래량
   - 배당률, 배당 주기
   - 비용 비율, 운용자산

6. **성과 비교 차트**
   - 여러 ETF 수익률 비교
   - 벤치마크 대비 성과

## API 문서

백엔드 실행 후 http://localhost:8000/docs 에서 Swagger UI로 API 문서 확인 가능합니다.

## 데이터베이스

SQLite 파일(`app.db`)은 backend 폴더에 생성됩니다. 서버 첫 실행 시 테이블이 자동 생성됩니다.

## 개발 가이드

### 프론트엔드 개발

- Vue 3 Composition API 사용
- TypeScript로 타입 안정성 확보
- Vuetify 컴포넌트로 일관된 UI
- Vue-ChartJS로 차트 구현

### 백엔드 개발

- FastAPI 비동기 처리 활용
- Pydantic으로 데이터 검증
- SQLAlchemy ORM으로 DB 작업
- RESTful API 설계 원칙 준수

## 코딩 규칙

- 간결하고 읽기 쉬운 코드 작성
- 필요한 기능만 구현 (over-engineering 지양)
- 타입 힌트 사용 (Python, TypeScript)
- 의미 있는 변수명/함수명 사용
