# 배당 ETF 대시보드

여러 위젯으로 구성된 배당 ETF 대시보드 프로젝트

## 기술 스택

- **Frontend**: Vue 3 + Vite + TypeScript + Vuetify + Tailwind CSS
- **Backend**: Python 3.12 + FastAPI
- **Database**: SQLite (SQLAlchemy ORM)

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

## 주요 기능

### 대시 보드 위젯
- ETF 배당 수익률 TOP 5 랭킹 차트
- ETF 배당 수익률 TOP 5 랭킹 1개월 추이 차트
- 각 배당 ETF 별 캘린더 및 스케줄


## API 문서

백엔드 실행 후 http://localhost:8000/docs 에서 Swagger UI 확인

## 프로젝트 구조

```
module_6/
├── frontend/           # Vue 3 프론트엔드
│   ├── src/
│   │   ├── components/ # 위젯 컴포넌트
│   │   ├── views/      # 페이지
│   │   ├── services/   # API 호출
│   │   └── types/      # TypeScript 타입
│   └── package.json
│
└── backend/            # FastAPI 백엔드
    ├── app/
    │   ├── main.py     # 진입점
    │   ├── models/     # DB 모델
    │   ├── schemas/    # Pydantic 스키마
    │   └── routers/    # API 엔드포인트
    └── requirements.txt
```
