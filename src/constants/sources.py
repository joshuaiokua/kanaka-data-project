"""
constants/sources.py

Constants for various sources (e.g. file paths, URLs).
"""

### --- CONSTANTS --- ###
# OHA Data Book
_OHA_BASE = "https://www.ohadatabook.com/"
_OHA_DB_BASE = f"{_OHA_BASE}CHAP%200"

### --- DATA SOURCE MAPS --- ###
OHA_DATA_BOOK = {
    "population": f"{_OHA_DB_BASE}1%20Population.23.xlsx",
    "housing": f"{_OHA_DB_BASE}2%20Housing.23.xlsx",
    "labor_and_employment": f"{_OHA_DB_BASE}3%20Labor%20and%20Employment.23.xlsx",
    "income": f"{_OHA_DB_BASE}4%20Income.23.xlsx",
    "land_water_air": f"{_OHA_DB_BASE}5%20Land%20Water%20Air.23.xlsx",
    "education": f"{_OHA_DB_BASE}6%20Education.23.xlsx",
    "health": f"{_OHA_DB_BASE}7%20Health.23.xlsx",
    "human_services": f"{_OHA_DB_BASE}8%20Human%20Services.23.xlsx",
    "crime": f"{_OHA_DB_BASE}9%20Crime.23.xlsx",
    "legacy_data": f"{_OHA_DB_BASE}10%20Legacy%20Data.23.xlsx",
}
