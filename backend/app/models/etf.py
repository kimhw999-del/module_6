from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime
from app.database import Base


class ETF(Base):
    __tablename__ = "etfs"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    current_price = Column(Float)
    previous_price = Column(Float)
    dividend_yield = Column(Float)  # 배당 수익률 (%)
    expense_ratio = Column(Float)  # 비용 비율 (%)
    aum = Column(Float)  # 운용자산 (억원)
    volume = Column(Integer)  # 거래량
    sector = Column(String)  # 섹터
    region = Column(String)  # 지역

    # 수익률
    return_1d = Column(Float)  # 일간 수익률 (%)
    return_1w = Column(Float)  # 주간 수익률 (%)
    return_1m = Column(Float)  # 월간 수익률 (%)
    return_1y = Column(Float)  # 연간 수익률 (%)

    # 상세 정보
    investment_strategy = Column(Text)  # 투자 전략 설명
    top_holdings = Column(JSON)  # 상위 보유 종목 리스트 [{"name": "종목명", "weight": 비중%}]

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
