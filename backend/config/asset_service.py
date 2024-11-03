from prisma import Prisma
from typing import List
from quart import Quart
import asyncio
import logging

app = Quart(__name__)

# Initialize Prisma client for shared use
prisma = Prisma()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_serving
async def connect_to_db():
    """Connect to the database before handling requests."""
    await prisma.connect()
    logger.info("DB connected")

@app.after_serving
async def disconnect_db():
    """Disconnect from the database when the app is shutting down."""
    if prisma.is_connected():
        await prisma.disconnect()
        logger.info("DB disconnected")

# Fetch asset name based on type and symbol
async def get_asset_name(asset_type: str, symbol: str) -> str:
    try:
        asset = await prisma.asset.find_first(
            where={
                "id": symbol,
                "type": asset_type
            }
        )
        return asset.name if asset else "Unknown Asset"
    except Exception as e:
        logger.error(f"Error fetching asset name for {symbol} ({asset_type}): {e}")
        return "Error"

# Retrieve symbols by asset type (stocks, bonds, cryptos)
async def get_asset_symbols(asset_type: str) -> List[str]:
    try:
        assets = await prisma.asset.find_many(
            where={"type": asset_type},
            select={"id": True}
        )
        return [asset.id for asset in assets]
    except Exception as e:
        logger.error(f"Error fetching asset symbols for type {asset_type}: {e}")
        return []

# Convenience functions for specific asset types
async def get_stock_symbols() -> List[str]:
    return await get_asset_symbols("stock")

async def get_bond_symbols() -> List[str]:
    return await get_asset_symbols("bond")

async def get_crypto_symbols() -> List[str]:
    return await get_asset_symbols("crypto")

# New function to get distinct asset types
async def get_asset_types() -> List[str]:
    """Retrieve distinct asset types from the database."""
    try:
        assets = await prisma.asset.find_many(
            distinct=["type"],
            select={"type": True}
        )
        return [asset.type for asset in assets]
    except Exception as e:
        logger.error(f"Error fetching asset types: {e}")
        return []
