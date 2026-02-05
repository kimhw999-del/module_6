# 프로젝트 진행 상황

## [2026-02-05 14:30] 세션 작업 내역

### 변경된 파일
- `frontend/src/components/widgets/ETFTable.vue`: 미니 차트, 컬럼 설정, 상세 정보 기능 추가
- `frontend/src/types/index.ts`: Holding 인터페이스 및 ETF 타입 확장
- `backend/app/models/etf.py`: investment_strategy, top_holdings 필드 추가
- `backend/app/schemas/etf.py`: Holding 스키마 및 ETFCreate/Response 확장
- `backend/app/init_sample_data.py`: 샘플 데이터에 투자 전략 및 보유 종목 정보 추가

### 작업 요약
- ETF 테이블에 1주일치 가격 추이 미니 타임라인 차트 추가
- 사용자가 컬럼 표시를 선택할 수 있는 설정 기능 구현 (localStorage 저장)
- ETF 티커 클릭 시 상세 정보 다이얼로그 표시
- 상세 정보에 투자 전략 및 상위 보유 종목 TOP 10 표시
- 보유 종목 비중을 도넛 차트와 리스트로 시각화
- 백엔드 데이터베이스 스키마 확장 (investment_strategy, top_holdings)
- Chart.js를 활용한 미니 차트 및 도넛 차트 구현

## 다음 스텝
- [ ] 실제 가격 히스토리 API 구현 (현재는 계산값 사용)
- [ ] 보유 종목 정보를 모든 ETF에 추가
- [ ] ETF 비교 기능 추가
- [ ] 필터링 및 정렬 고도화
- [ ] 포트폴리오 추천 기능
