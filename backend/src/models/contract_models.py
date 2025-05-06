from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ContractType(enum.Enum):
    AMM = "AMM"
    MULTISIG = "Multisig"
    LENDING = "Lending"
    STAKING = "Staking"
    OTHER = "Other"

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(Enum(ContractType), nullable=False, default=ContractType.OTHER)
    source_code = Column(Text, nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)