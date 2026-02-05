# 프로젝트 진행 상황

## [2026-02-05 18:00] 세션 작업 내역

### 변경된 파일
- `frontend/src/views/Dashboard.vue`: 편집 가능한 대시보드로 완전 재구현
- `frontend/src/components/widgets/PerformanceComparison.vue`: 성과 비교 차트 대폭 개선
- `frontend/src/components/widgets/DividendCalendar.vue`: 배당 캘린더 기능 개선
- `frontend/src/components/widgets/SectorAllocation.vue`: 섹터/지역 분산 도넛 차트로 개선
- `frontend/package.json`: @vueuse/core 추가
- `CLAUDE.md`: 전체 기능 반영하여 개정
- `README.md`: 상세 기능 설명 추가

### 작업 요약
- **편집 가능한 대시보드** 구현
  - 드래그 앤 드롭으로 위젯 순서 변경
  - 위젯 표시/숨김 관리
  - localStorage 자동 저장
  - 기본 레이아웃 복원 기능
- **성과 비교 차트** 대폭 개선
  - 최대 8개 ETF 동시 비교
  - 빠른 선택 (높은 배당률/수익률 TOP 5)
  - 검색 및 섹터 필터링
  - 차트/테이블 뷰 토글
  - 평균 수익률 통계 카드
- **배당 캘린더** 기능 추가
  - 월별 캘린더 ↔ 다가오는 배당 뷰 전환
  - 임박 알림 (7일 이내 강조)
  - 월별 통계 (배당 건수, 평균 수익률, 총액)
- **섹터/지역 분산** 개선
  - 파이 차트에서 도넛 차트로 변경
  - 통계 카드 및 다양성 지표 추가
  - 개수/비율 토글 전환
  - 프로그레스 바 시각화
- **문서 개정**
  - CLAUDE.md: 개발 가이드 전면 개정
  - README.md: 주요 기능 상세 설명 추가
- **기술적 개선**
  - markRaw로 Vue 컴포넌트 반응형 제외
  - vue-grid-layout 제거, 네이티브 드래그 앤 드롭 사용
  - localStorage 키 버전 관리 (v2)

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
- [x] 성과 비교 차트 구현
- [x] 배당 캘린더 개선
- [x] 섹터/지역 분산 개선
- [x] 편집 가능한 대시보드 구현
- [x] 문서 개정 (CLAUDE.md, README.md)
- [ ] 실제 가격 히스토리 API 구현
- [ ] 보유 종목 정보를 모든 ETF에 추가
- [ ] 반응형 그리드 레이아웃 개선
- [ ] 다크 모드 지원
- [ ] 위젯 추가/제거 기능
