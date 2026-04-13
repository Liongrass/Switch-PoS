import asyncio

from payments import listener
from screens import make_idlescreen
from display import init, touchme

async def main():
    init()
    await make_idlescreen()
    #await make_salesscreen()
    await asyncio.gather(listener(), touchme())
    #await asyncio.gather(touchme())

asyncio.run(main())