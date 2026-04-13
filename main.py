import asyncio

from payments import listener
from TP2in9_test import init, pthread_irq

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(1)

async def main():
    init()
    await asyncio.gather(listener(), count(), pthread_irq())

if __name__ == "__main__":
    import time

asyncio.run(main())