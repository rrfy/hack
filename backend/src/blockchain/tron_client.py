import logging
import re
import requests
from src.config import TRONGRID_API_KEY, TRON_FULL_NODE
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TronClient:
    def __init__(self):
        self.api_key = TRONGRID_API_KEY
        self.base_url = TRON_FULL_NODE.rstrip('/')

    def is_valid_address(self, address: str) -> bool:
        """Проверка валидности TRON-адреса."""
        try:
            if not isinstance(address, str):
                return False
            if len(address) != 34 or not address.startswith('T'):
                return False
            base58_pattern = r'^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]+$'
            return bool(re.match(base58_pattern, address))
        except Exception as e:
            logger.error(f"Address validation error for {address}: {str(e)}")
            return False

    async def get_contract(self, address: str) -> Dict:
        try:
            logger.info(f"Fetching contract: {address}")
            if not self.is_valid_address(address):
                logger.error(f"Invalid TRON address: {address}")
                return {"error": "Invalid TRON address"}

            # Запрос к TronGrid API
            url = f"{self.base_url}/wallet/getcontract"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "TRON-PRO-API-KEY": self.api_key
            } if self.api_key else {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "value": address,
                "visible": True
            }

            logger.info(f"Sending POST request to {url} with payload: {payload}")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if not data or "Error" in data:
                logger.error(f"Contract not found: {address}, API response: {data.get('Error', 'No data')}")
                return {"error": "Contract not found"}

            # Извлечение байткода
            code = data.get("bytecode", "")
            if isinstance(code, bytes):
                code = code.hex()
            elif not isinstance(code, str):
                logger.warning(f"Unexpected bytecode type: {type(code)}")
                code = str(code)

            contract_type = "OTHER"
            if code and "swap" in code.lower():
                contract_type = "AMM"
            elif code and "multisig" in code.lower():
                contract_type = "MULTISIG"

            result = {
                "address": address,
                "source_code": code,
                "type": contract_type,
                "name": data.get("name", "")
            }
            logger.info(f"Contract fetched successfully: {address}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch contract {address}: {str(e)}")
            return {"error": f"Failed to fetch contract: {str(e)}"}
        except Exception as e:
            logger.error(f"Failed to fetch contract {address}: {str(e)}")
            return {"error": f"Failed to fetch contract: {str(e)}"}