from pydantic import BaseModel
from typing import List, Dict, Optional


class FinancialRecord(BaseModel):
    label: str
    value: Optional[float]


class CompanyData(BaseModel):
    income_statement: Optional[List[Dict[str, Optional[str]]]] = None
    balance_sheet: Optional[List[Dict[str, Optional[str]]]] = None
    cash_flow: Optional[List[Dict[str, Optional[str]]]] = None
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None
    about: Optional[str] = None


class NewsItem(BaseModel):
    title: str
    summary: str
    sentiment: str
    published: str
    link: str
