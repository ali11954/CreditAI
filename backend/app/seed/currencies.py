from typing import List, Dict, Any

COMMON_CURRENCIES: List[Dict[str, Any]] = [
    {"code": "SAR", "name": "Saudi Riyal", "name_ar": "ريال سعودي", "symbol": "﷼", "is_base": True, "exchange_rate": 1.0},
    {"code": "AED", "name": "UAE Dirham", "name_ar": "درهم إماراتي", "symbol": "د.إ", "is_base": False, "exchange_rate": 0.97},
    {"code": "KWD", "name": "Kuwaiti Dinar", "name_ar": "دينار كويتي", "symbol": "د.ك", "is_base": False, "exchange_rate": 0.091},
    {"code": "QAR", "name": "Qatari Riyal", "name_ar": "ريال قطري", "symbol": "﷼", "is_base": False, "exchange_rate": 0.97},
    {"code": "BHD", "name": "Bahraini Dinar", "name_ar": "دينار بحريني", "symbol": "د.ب", "is_base": False, "exchange_rate": 0.99},
    {"code": "OMR", "name": "Omani Rial", "name_ar": "ريال عماني", "symbol": "﷼", "is_base": False, "exchange_rate": 0.97},
    {"code": "EGP", "name": "Egyptian Pound", "name_ar": "جنيه مصري", "symbol": "£", "is_base": False, "exchange_rate": 13.0},
    {"code": "JOD", "name": "Jordanian Dinar", "name_ar": "دينار أردني", "symbol": "د.ا", "is_base": False, "exchange_rate": 0.71},
    {"code": "LBP", "name": "Lebanese Pound", "name_ar": "ليرة لبنانية", "symbol": "£", "is_base": False, "exchange_rate": 1500.0},
    {"code": "IQD", "name": "Iraqi Dinar", "name_ar": "دينار عراقي", "symbol": "ع.د", "is_base": False, "exchange_rate": 1300.0},
    {"code": "USD", "name": "US Dollar", "name_ar": "دولار أمريكي", "symbol": "$", "is_base": False, "exchange_rate": 3.75},
    {"code": "EUR", "name": "Euro", "name_ar": "يورو", "symbol": "€", "is_base": False, "exchange_rate": 4.1},
    {"code": "GBP", "name": "British Pound", "name_ar": "جنيه إسترليني", "symbol": "£", "is_base": False, "exchange_rate": 4.75},
]
