import asyncio

import methods


async def test():
    await methods.cheque_gpt_formatter()

if __name__ == "__main__":
    asyncio.run(test())