import os

TRONGRID_API_KEY = os.getenv("TRONGRID_API_KEY")
TRON_FULL_NODE = "https://api.trongrid.io"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://defi_user:password@localhost:5432/defi_analyzer")