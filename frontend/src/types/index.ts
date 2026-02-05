export interface Holding {
  name: string
  weight: number
}

export interface ETF {
  id: number
  ticker: string
  name: string
  current_price: number
  previous_price: number
  dividend_yield: number
  expense_ratio: number
  aum: number
  volume: number
  sector: string
  region: string
  return_1d: number
  return_1w: number
  return_1m: number
  return_1y: number
  investment_strategy?: string
  top_holdings?: Holding[]
  created_at: string
  updated_at: string
}

export interface ETFRanking {
  ticker: string
  name: string
  return_value: number
  dividend_yield?: number
}

export interface Portfolio {
  id: number
  etf_id: number
  shares: number
  avg_price: number
  total_invested: number
}

export interface PortfolioWithETF extends Portfolio {
  ticker: string
  name: string
  current_price: number
  dividend_yield: number
}

export interface PortfolioSummary {
  total_invested: number
  total_value: number
  total_profit: number
  profit_rate: number
  unrealized_profit: number
  monthly_dividend: number
}

export interface Dividend {
  id: number
  etf_id: number
  ex_dividend_date: string
  payment_date: string
  dividend_per_share: number
  frequency: string
}

export interface DividendCalendarItem {
  id: number
  ticker: string
  name: string
  ex_dividend_date: string
  payment_date: string
  dividend_per_share: number
  frequency: string
  dividend_yield?: number
}

export interface SectorAllocation {
  [sector: string]: number
}

export interface RegionAllocation {
  [region: string]: number
}
