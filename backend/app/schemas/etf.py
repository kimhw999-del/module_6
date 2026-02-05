from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class Holding(BaseModel):
    """보유 종목 정보"""
    name: str
    weight: float  # 비중 (%)


class ETFBase(BaseModel):
    ticker: str
    name: str
    current_price: float
    previous_price: float
    dividend_yield: float
    expense_ratio: float
    aum: float
    volume: int
    sector: str
    region: str
    return_1d: float
    return_1w: float
    return_1m: float
    return_1y: float


class ETFCreate(ETFBase):
    investment_strategy: Optional[str] = None
    top_holdings: Optional[List[Dict[str, Any]]] = None


class ETFResponse(ETFBase):
    id: int
    investment_strategy: Optional[str] = None
    top_holdings: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ETFRanking(BaseModel):
    """수익률 랭킹용 간소화 스키마"""
    ticker: str
    name: str
    return_value: float  # 해당 기간 수익률
    dividend_yield: Optional[float] = None

    class Config:
        from_attributes = True
