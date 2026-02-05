"""샘플 데이터 초기화 스크립트"""

from datetime import date, timedelta
from app.database import SessionLocal, Base, engine
from app.models import ETF, Portfolio, Dividend


def init_sample_data():
    # 테이블 생성
    print("데이터베이스 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("테이블 생성 완료\n")

    db = SessionLocal()

    try:
        # 기존 데이터 확인
        existing_etfs = db.query(ETF).count()
        if existing_etfs > 0:
            print("샘플 데이터가 이미 존재합니다.")
            return

        # 샘플 ETF 데이터 (50개 - 실제 배당 ETF 기반)
        sample_etfs = [
            # High Yield Monthly/Quarterly Dividend ETFs
            {"ticker": "JEPQ", "name": "JPMorgan Nasdaq Equity Premium Income ETF", "current_price": 58000, "previous_price": 57500, "dividend_yield": 10.2, "expense_ratio": 0.35, "aum": 15000, "volume": 950000, "sector": "Income", "region": "US", "return_1d": 0.87, "return_1w": 1.5, "return_1m": 3.2, "return_1y": 8.5,
             "investment_strategy": "나스닥 100 지수의 대형 성장주에 투자하면서 ELN(주식연계증권) 전략을 활용하여 월배당 수익을 창출합니다. 옵션 프리미엄 수익과 배당을 결합하여 높은 수익률을 추구하는 액티브 전략입니다.",
             "top_holdings": [
                 {"name": "Apple Inc.", "weight": 8.5},
                 {"name": "Microsoft Corp.", "weight": 7.2},
                 {"name": "Amazon.com Inc.", "weight": 5.8},
                 {"name": "NVIDIA Corp.", "weight": 5.1},
                 {"name": "Tesla Inc.", "weight": 4.3},
                 {"name": "Alphabet Inc. Class A", "weight": 3.9},
                 {"name": "Meta Platforms Inc.", "weight": 3.5},
                 {"name": "Broadcom Inc.", "weight": 2.8},
                 {"name": "Netflix Inc.", "weight": 2.4},
                 {"name": "Adobe Inc.", "weight": 2.1}
             ]},
            {"ticker": "QYLD", "name": "Global X NASDAQ 100 Covered Call ETF", "current_price": 21000, "previous_price": 20900, "dividend_yield": 11.4, "expense_ratio": 0.60, "aum": 8170, "volume": 1200000, "sector": "Technology", "region": "US", "return_1d": 0.48, "return_1w": 0.5, "return_1m": 1.2, "return_1y": 5.3,
             "investment_strategy": "나스닥 100 지수를 추종하면서 보유 주식에 대해 커버드콜 옵션을 매도하여 옵션 프리미엄 수익을 창출합니다. 주가 상승 시 수익은 제한되지만 안정적인 월배당 수익을 제공합니다.",
             "top_holdings": [
                 {"name": "Apple Inc.", "weight": 11.2},
                 {"name": "Microsoft Corp.", "weight": 9.8},
                 {"name": "Amazon.com Inc.", "weight": 6.5},
                 {"name": "NVIDIA Corp.", "weight": 5.9},
                 {"name": "Alphabet Inc. Class C", "weight": 4.2},
                 {"name": "Meta Platforms Inc.", "weight": 3.8},
                 {"name": "Tesla Inc.", "weight": 3.5},
                 {"name": "Broadcom Inc.", "weight": 2.9},
                 {"name": "Costco Wholesale Corp.", "weight": 2.3},
                 {"name": "PepsiCo Inc.", "weight": 1.9}
             ]},
            {"ticker": "SDIV", "name": "Global X SuperDividend ETF", "current_price": 14000, "previous_price": 13950, "dividend_yield": 9.6, "expense_ratio": 0.58, "aum": 3000, "volume": 220000, "sector": "Income", "region": "Global", "return_1d": 0.36, "return_1w": 0.7, "return_1m": 1.8, "return_1y": 6.5},
            {"ticker": "XYLD", "name": "Global X S&P 500 Covered Call ETF", "current_price": 45000, "previous_price": 44700, "dividend_yield": 9.2, "expense_ratio": 0.61, "aum": 2820, "volume": 580000, "sector": "Income", "region": "US", "return_1d": 0.67, "return_1w": 1.1, "return_1m": 2.3, "return_1y": 7.8},
            {"ticker": "JEPI", "name": "JPMorgan Equity Premium Income ETF", "current_price": 62000, "previous_price": 61800, "dividend_yield": 8.3, "expense_ratio": 0.35, "aum": 35000, "volume": 800000, "sector": "Income", "region": "US", "return_1d": 0.32, "return_1w": 0.8, "return_1m": 2.1, "return_1y": 9.5},
            {"ticker": "RYLD", "name": "Global X Russell 2000 Covered Call ETF", "current_price": 18500, "previous_price": 18300, "dividend_yield": 10.5, "expense_ratio": 0.61, "aum": 1500, "volume": 380000, "sector": "Income", "region": "US", "return_1d": 1.09, "return_1w": 1.8, "return_1m": 3.5, "return_1y": 6.2},
            {"ticker": "DIVO", "name": "Amplify CWP Enhanced Dividend Income ETF", "current_price": 42000, "previous_price": 41800, "dividend_yield": 5.8, "expense_ratio": 0.55, "aum": 2800, "volume": 195000, "sector": "Diversified", "region": "US", "return_1d": 0.48, "return_1w": 1.2, "return_1m": 3.1, "return_1y": 10.5},

            # Core Dividend Growth ETFs
            {"ticker": "SCHD", "name": "Schwab US Dividend Equity ETF", "current_price": 28000, "previous_price": 27800, "dividend_yield": 3.8, "expense_ratio": 0.06, "aum": 50000, "volume": 2500000, "sector": "Diversified", "region": "US", "return_1d": 0.72, "return_1w": 1.5, "return_1m": 4.2, "return_1y": 14.8,
             "investment_strategy": "Dow Jones U.S. Dividend 100 지수를 추종하며, 배당 성장성과 지속가능성이 높은 미국 기업에 투자합니다. 10년 이상 배당을 지급하고 재무 건전성이 우수한 기업을 선별하여 장기적인 배당 성장을 추구합니다.",
             "top_holdings": [
                 {"name": "Verizon Communications Inc.", "weight": 4.2},
                 {"name": "Amgen Inc.", "weight": 3.8},
                 {"name": "Merck & Co. Inc.", "weight": 3.5},
                 {"name": "Coca-Cola Co.", "weight": 3.2},
                 {"name": "PepsiCo Inc.", "weight": 3.1},
                 {"name": "AbbVie Inc.", "weight": 2.9},
                 {"name": "Texas Instruments Inc.", "weight": 2.7},
                 {"name": "Pfizer Inc.", "weight": 2.5},
                 {"name": "Lockheed Martin Corp.", "weight": 2.4},
                 {"name": "Chevron Corp.", "weight": 2.3}
             ]},
            {"ticker": "VYM", "name": "Vanguard High Dividend Yield ETF", "current_price": 130000, "previous_price": 129500, "dividend_yield": 2.9, "expense_ratio": 0.06, "aum": 60000, "volume": 1800000, "sector": "Diversified", "region": "US", "return_1d": 0.39, "return_1w": 1.2, "return_1m": 3.8, "return_1y": 13.5},
            {"ticker": "SPYD", "name": "SPDR Portfolio S&P 500 High Dividend ETF", "current_price": 45000, "previous_price": 44800, "dividend_yield": 4.5, "expense_ratio": 0.07, "aum": 8000, "volume": 3200000, "sector": "Diversified", "region": "US", "return_1d": 0.45, "return_1w": 1.1, "return_1m": 3.5, "return_1y": 11.2},
            {"ticker": "HDV", "name": "iShares Core High Dividend ETF", "current_price": 115000, "previous_price": 114500, "dividend_yield": 3.6, "expense_ratio": 0.08, "aum": 12000, "volume": 850000, "sector": "Diversified", "region": "US", "return_1d": 0.44, "return_1w": 0.9, "return_1m": 2.8, "return_1y": 10.8},
            {"ticker": "DVY", "name": "iShares Select Dividend ETF", "current_price": 132000, "previous_price": 131500, "dividend_yield": 3.4, "expense_ratio": 0.38, "aum": 20490, "volume": 620000, "sector": "Diversified", "region": "US", "return_1d": 0.38, "return_1w": 1.0, "return_1m": 3.2, "return_1y": 11.5},

            # Dividend Aristocrats & Quality
            {"ticker": "NOBL", "name": "ProShares S&P 500 Dividend Aristocrats ETF", "current_price": 95000, "previous_price": 94700, "dividend_yield": 2.6, "expense_ratio": 0.35, "aum": 11040, "volume": 780000, "sector": "Diversified", "region": "US", "return_1d": 0.32, "return_1w": 0.8, "return_1m": 2.5, "return_1y": 12.3},
            {"ticker": "SDY", "name": "SPDR S&P Dividend ETF", "current_price": 135000, "previous_price": 134500, "dividend_yield": 2.6, "expense_ratio": 0.35, "aum": 18500, "volume": 590000, "sector": "Diversified", "region": "US", "return_1d": 0.37, "return_1w": 0.9, "return_1m": 2.7, "return_1y": 11.8},
            {"ticker": "VIG", "name": "Vanguard Dividend Appreciation ETF", "current_price": 185000, "previous_price": 184200, "dividend_yield": 1.6, "expense_ratio": 0.06, "aum": 75000, "volume": 1200000, "sector": "Diversified", "region": "US", "return_1d": 0.43, "return_1w": 1.3, "return_1m": 3.8, "return_1y": 15.2},
            {"ticker": "DGRO", "name": "iShares Core Dividend Growth ETF", "current_price": 58000, "previous_price": 57700, "dividend_yield": 2.3, "expense_ratio": 0.08, "aum": 22000, "volume": 950000, "sector": "Diversified", "region": "US", "return_1d": 0.52, "return_1w": 1.4, "return_1m": 3.9, "return_1y": 14.5},
            {"ticker": "DGRW", "name": "WisdomTree US Quality Dividend Growth ETF", "current_price": 72000, "previous_price": 71600, "dividend_yield": 1.9, "expense_ratio": 0.28, "aum": 8500, "volume": 420000, "sector": "Diversified", "region": "US", "return_1d": 0.56, "return_1w": 1.5, "return_1m": 4.1, "return_1y": 16.2},
            {"ticker": "FDL", "name": "First Trust Morningstar Dividend Leaders ETF", "current_price": 38000, "previous_price": 37800, "dividend_yield": 4.1, "expense_ratio": 0.45, "aum": 3200, "volume": 285000, "sector": "Diversified", "region": "US", "return_1d": 0.53, "return_1w": 1.2, "return_1m": 3.3, "return_1y": 10.9},

            # High Dividend Sector ETFs
            {"ticker": "VNQ", "name": "Vanguard Real Estate ETF", "current_price": 95000, "previous_price": 94500, "dividend_yield": 4.2, "expense_ratio": 0.12, "aum": 35000, "volume": 1500000, "sector": "Real Estate", "region": "US", "return_1d": 0.53, "return_1w": 1.0, "return_1m": 2.8, "return_1y": 8.5},
            {"ticker": "SRET", "name": "Global X SuperDividend REIT ETF", "current_price": 8500, "previous_price": 8450, "dividend_yield": 8.5, "expense_ratio": 0.58, "aum": 850, "volume": 180000, "sector": "Real Estate", "region": "Global", "return_1d": 0.59, "return_1w": 1.1, "return_1m": 2.5, "return_1y": 7.2},
            {"ticker": "PFF", "name": "iShares Preferred and Income Securities ETF", "current_price": 38000, "previous_price": 37900, "dividend_yield": 6.2, "expense_ratio": 0.45, "aum": 15500, "volume": 3800000, "sector": "Financials", "region": "US", "return_1d": 0.26, "return_1w": 0.6, "return_1m": 1.8, "return_1y": 9.8},
            {"ticker": "KBWD", "name": "Invesco KBW High Dividend Yield Financial ETF", "current_price": 22000, "previous_price": 21850, "dividend_yield": 6.8, "expense_ratio": 0.35, "aum": 950, "volume": 125000, "sector": "Financials", "region": "US", "return_1d": 0.69, "return_1w": 1.4, "return_1m": 3.6, "return_1y": 12.5},
            {"ticker": "SPHD", "name": "Invesco S&P 500 High Dividend Low Volatility ETF", "current_price": 48000, "previous_price": 47750, "dividend_yield": 4.5, "expense_ratio": 0.30, "aum": 2800, "volume": 490000, "sector": "Diversified", "region": "US", "return_1d": 0.52, "return_1w": 1.1, "return_1m": 2.9, "return_1y": 10.2},
            {"ticker": "DHS", "name": "WisdomTree US High Dividend ETF", "current_price": 82000, "previous_price": 81600, "dividend_yield": 4.8, "expense_ratio": 0.38, "aum": 1500, "volume": 145000, "sector": "Diversified", "region": "US", "return_1d": 0.49, "return_1w": 1.0, "return_1m": 3.0, "return_1y": 11.3},
            {"ticker": "FVD", "name": "First Trust Value Line Dividend ETF", "current_price": 43000, "previous_price": 42800, "dividend_yield": 3.2, "expense_ratio": 0.70, "aum": 980, "volume": 95000, "sector": "Diversified", "region": "US", "return_1d": 0.47, "return_1w": 1.1, "return_1m": 3.1, "return_1y": 11.8},

            # International Dividend ETFs
            {"ticker": "VIGI", "name": "Vanguard International Dividend Appreciation ETF", "current_price": 82000, "previous_price": 81700, "dividend_yield": 2.8, "expense_ratio": 0.15, "aum": 6500, "volume": 320000, "sector": "Diversified", "region": "International", "return_1d": 0.37, "return_1w": 0.9, "return_1m": 2.3, "return_1y": 9.5},
            {"ticker": "IDV", "name": "iShares International Select Dividend ETF", "current_price": 32000, "previous_price": 31850, "dividend_yield": 6.5, "expense_ratio": 0.49, "aum": 2500, "volume": 280000, "sector": "Diversified", "region": "International", "return_1d": 0.47, "return_1w": 1.0, "return_1m": 2.5, "return_1y": 8.2},
            {"ticker": "DTH", "name": "WisdomTree International High Dividend ETF", "current_price": 48000, "previous_price": 47800, "dividend_yield": 5.2, "expense_ratio": 0.58, "aum": 850, "volume": 125000, "sector": "Diversified", "region": "International", "return_1d": 0.42, "return_1w": 0.9, "return_1m": 2.2, "return_1y": 7.8},
            {"ticker": "DEM", "name": "WisdomTree Emerging Markets High Dividend ETF", "current_price": 42000, "previous_price": 41800, "dividend_yield": 5.8, "expense_ratio": 0.63, "aum": 780, "volume": 98000, "sector": "Diversified", "region": "Emerging", "return_1d": 0.48, "return_1w": 1.1, "return_1m": 2.8, "return_1y": 9.2},
            {"ticker": "SDVY", "name": "First Trust SMID Cap Rising Dividend Achievers ETF", "current_price": 31000, "previous_price": 30850, "dividend_yield": 2.4, "expense_ratio": 0.60, "aum": 650, "volume": 85000, "sector": "Diversified", "region": "US", "return_1d": 0.49, "return_1w": 1.3, "return_1m": 3.5, "return_1y": 12.8},
            {"ticker": "VEA", "name": "Vanguard FTSE Developed Markets ETF", "current_price": 55000, "previous_price": 54700, "dividend_yield": 3.1, "expense_ratio": 0.05, "aum": 120000, "volume": 4500000, "sector": "Diversified", "region": "International", "return_1d": 0.55, "return_1w": 1.3, "return_1m": 2.9, "return_1y": 8.7},
            {"ticker": "VWO", "name": "Vanguard FTSE Emerging Markets ETF", "current_price": 48000, "previous_price": 47750, "dividend_yield": 3.5, "expense_ratio": 0.08, "aum": 85000, "volume": 8500000, "sector": "Diversified", "region": "Emerging", "return_1d": 0.52, "return_1w": 1.2, "return_1m": 3.2, "return_1y": 10.5},

            # Additional Dividend ETFs
            {"ticker": "DIV", "name": "Global X SuperDividend US ETF", "current_price": 23000, "previous_price": 22900, "dividend_yield": 6.8, "expense_ratio": 0.45, "aum": 1200, "volume": 195000, "sector": "Income", "region": "US", "return_1d": 0.44, "return_1w": 0.9, "return_1m": 2.3, "return_1y": 8.5},
            {"ticker": "RDVY", "name": "First Trust Rising Dividend Achievers ETF", "current_price": 52000, "previous_price": 51750, "dividend_yield": 2.1, "expense_ratio": 0.50, "aum": 6500, "volume": 780000, "sector": "Diversified", "region": "US", "return_1d": 0.48, "return_1w": 1.3, "return_1m": 3.7, "return_1y": 14.2},
            {"ticker": "IQDF", "name": "FlexShares International Quality Dividend ETF", "current_price": 38000, "previous_price": 37850, "dividend_yield": 3.8, "expense_ratio": 0.47, "aum": 950, "volume": 68000, "sector": "Diversified", "region": "International", "return_1d": 0.40, "return_1w": 0.8, "return_1m": 2.4, "return_1y": 9.8},
            {"ticker": "HNDL", "name": "Strategy Shares Nasdaq 7HANDL Index ETF", "current_price": 26000, "previous_price": 25900, "dividend_yield": 7.2, "expense_ratio": 0.95, "aum": 520, "volume": 125000, "sector": "Income", "region": "US", "return_1d": 0.39, "return_1w": 0.7, "return_1m": 1.9, "return_1y": 7.8},
            {"ticker": "DEW", "name": "WisdomTree Global High Dividend ETF", "current_price": 58000, "previous_price": 57800, "dividend_yield": 5.5, "expense_ratio": 0.58, "aum": 850, "volume": 98000, "sector": "Diversified", "region": "Global", "return_1d": 0.35, "return_1w": 0.9, "return_1m": 2.3, "return_1y": 8.9},
            {"ticker": "DLN", "name": "WisdomTree US LargeCap Dividend ETF", "current_price": 135000, "previous_price": 134500, "dividend_yield": 2.5, "expense_ratio": 0.28, "aum": 2800, "volume": 125000, "sector": "Diversified", "region": "US", "return_1d": 0.37, "return_1w": 1.1, "return_1m": 3.3, "return_1y": 13.5},
            {"ticker": "DON", "name": "WisdomTree US MidCap Dividend ETF", "current_price": 48000, "previous_price": 47800, "dividend_yield": 2.8, "expense_ratio": 0.38, "aum": 1200, "volume": 95000, "sector": "Diversified", "region": "US", "return_1d": 0.42, "return_1w": 1.2, "return_1m": 3.5, "return_1y": 12.8},
            {"ticker": "DES", "name": "WisdomTree US SmallCap Dividend ETF", "current_price": 38000, "previous_price": 37850, "dividend_yield": 3.5, "expense_ratio": 0.38, "aum": 850, "volume": 78000, "sector": "Diversified", "region": "US", "return_1d": 0.40, "return_1w": 1.3, "return_1m": 3.8, "return_1y": 11.5},
            {"ticker": "FTCS", "name": "First Trust Capital Strength ETF", "current_price": 88000, "previous_price": 87600, "dividend_yield": 1.8, "expense_ratio": 0.60, "aum": 2500, "volume": 185000, "sector": "Diversified", "region": "US", "return_1d": 0.46, "return_1w": 1.4, "return_1m": 4.0, "return_1y": 15.8},
            {"ticker": "FDVV", "name": "Fidelity High Dividend ETF", "current_price": 42000, "previous_price": 41850, "dividend_yield": 3.2, "expense_ratio": 0.29, "aum": 1800, "volume": 125000, "sector": "Diversified", "region": "US", "return_1d": 0.36, "return_1w": 1.0, "return_1m": 3.1, "return_1y": 12.3},
            {"ticker": "SDOG", "name": "ALPS Sector Dividend Dogs ETF", "current_price": 58000, "previous_price": 57750, "dividend_yield": 4.5, "expense_ratio": 0.40, "aum": 980, "volume": 95000, "sector": "Diversified", "region": "US", "return_1d": 0.43, "return_1w": 1.1, "return_1m": 3.0, "return_1y": 10.8},
            {"ticker": "DIVB", "name": "iShares Core Dividend ETF", "current_price": 32000, "previous_price": 31900, "dividend_yield": 3.8, "expense_ratio": 0.10, "aum": 750, "volume": 68000, "sector": "Diversified", "region": "US", "return_1d": 0.31, "return_1w": 0.9, "return_1m": 2.8, "return_1y": 11.8},
            {"ticker": "PEY", "name": "Invesco High Yield Equity Dividend Achievers ETF", "current_price": 24000, "previous_price": 23900, "dividend_yield": 4.8, "expense_ratio": 0.52, "aum": 1250, "volume": 125000, "sector": "Diversified", "region": "US", "return_1d": 0.42, "return_1w": 1.0, "return_1m": 2.9, "return_1y": 10.5},
            {"ticker": "PID", "name": "Invesco International Dividend Achievers ETF", "current_price": 19000, "previous_price": 18900, "dividend_yield": 5.2, "expense_ratio": 0.54, "aum": 680, "volume": 85000, "sector": "Diversified", "region": "International", "return_1d": 0.53, "return_1w": 1.1, "return_1m": 2.7, "return_1y": 9.2},
            {"ticker": "IDHD", "name": "Invesco S&P International Developed High Dividend Low Volatility ETF", "current_price": 28000, "previous_price": 27900, "dividend_yield": 5.5, "expense_ratio": 0.30, "aum": 520, "volume": 58000, "sector": "Diversified", "region": "International", "return_1d": 0.36, "return_1w": 0.8, "return_1m": 2.3, "return_1y": 8.5},
        ]

        # ETF 데이터 추가
        etfs = []
        for etf_data in sample_etfs:
            etf = ETF(**etf_data)
            db.add(etf)
            etfs.append(etf)

        db.commit()

        # ETF ID 갱신
        for etf in etfs:
            db.refresh(etf)

        print(f"{len(etfs)}개의 ETF 데이터 생성 완료")

        # 샘플 포트폴리오 데이터 (처음 5개 ETF만 보유)
        sample_portfolios = [
            {"etf_id": etfs[0].id, "shares": 10, "avg_price": 82000, "total_invested": 820000},
            {"etf_id": etfs[1].id, "shares": 15, "avg_price": 60000, "total_invested": 900000},
            {"etf_id": etfs[2].id, "shares": 50, "avg_price": 20500, "total_invested": 1025000},
            {"etf_id": etfs[3].id, "shares": 8, "avg_price": 128000, "total_invested": 1024000},
            {"etf_id": etfs[4].id, "shares": 20, "avg_price": 44000, "total_invested": 880000},
        ]

        for portfolio_data in sample_portfolios:
            portfolio = Portfolio(**portfolio_data)
            db.add(portfolio)

        db.commit()
        print(f"{len(sample_portfolios)}개의 포트폴리오 데이터 생성 완료")

        # 샘플 배당 일정 데이터
        today = date.today()
        sample_dividends = []

        for i, etf in enumerate(etfs[:5]):
            # 각 ETF당 2-3개의 배당 일정 생성
            dividend_dates = [
                today + timedelta(days=10 + i * 7),
                today + timedelta(days=40 + i * 7),
                today + timedelta(days=70 + i * 7),
            ]

            for ex_date in dividend_dates:
                payment_date = ex_date + timedelta(days=14)
                dividend = Dividend(
                    etf_id=etf.id,
                    ex_dividend_date=ex_date,
                    payment_date=payment_date,
                    dividend_per_share=etf.current_price * etf.dividend_yield / 100 / 12,
                    frequency="monthly" if etf.dividend_yield > 5 else "quarterly",
                )
                sample_dividends.append(dividend)
                db.add(dividend)

        db.commit()
        print(f"{len(sample_dividends)}개의 배당 일정 데이터 생성 완료")

        print("\n샘플 데이터 초기화 완료!")

    except Exception as e:
        print(f"에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
