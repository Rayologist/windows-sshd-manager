from typing import Dict, Optional
from .base import BaseWhoisExtractor
from pytz import country_names as pytz_country_name


class IPWhoisExtractor(BaseWhoisExtractor):
    def get_country_name(self, country_code: str) -> str:
        return pytz_country_name.get(country_code, "Invalid")

    def extract(self, res_dict: Dict[str, Optional[str]]) -> Dict[str, str]:
        ip = res_dict.get("query")
        country_code = res_dict.get("asn_country_code")
        country = self.get_country_name(country_code)
        return {
            "ip_address": ip,
            "country": country,
        }
