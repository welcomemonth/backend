# prisma.py
from prisma import Prisma

prisma = Prisma(auto_register=True)

async def connect():
    await prisma.connect()

async def disconnect():
    await prisma.disconnect()