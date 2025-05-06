from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.contract_models import Contract, ContractType
from src.database import async_session
from src.blockchain.tron_client import TronClient
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contracts")

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/{address}", response_model=Dict)
async def get_contract(address: str, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Processing request for contract: {address}")
        contract = await db.execute(select(Contract).filter_by(address=address))
        contract = contract.scalar_one_or_none()
        
        if contract:
            logger.info(f"Contract found in database: {address}")
            return {
                "address": contract.address,
                "type": contract.type.value,
                "source_code": contract.source_code,
                "created_at": contract.created_at,
                "last_analyzed": contract.last_analyzed
            }
        
        tron_client = TronClient()
        data = await tron_client.get_contract(address)
        
        if "error" in data:
            logger.error(f"Error fetching contract from TRON: {data['error']}")
            raise HTTPException(status_code=400, detail=data["error"])
        
        contract = Contract(
            address=data["address"],
            type=ContractType[data["type"]],
            source_code=data["source_code"]
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        
        logger.info(f"Contract saved successfully: {address}")
        return {
            "address": contract.address,
            "type": contract.type.value,
            "source_code": contract.source_code,
            "created_at": contract.created_at,
            "last_analyzed": contract.last_analyzed
        }
    except Exception as e:
        logger.error(f"Internal server error for contract {address}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")