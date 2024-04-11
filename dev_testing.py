import asyncio

from methods import *


async def test():
    a = "http://consumer.oofd.kz?i=3937088095&f=620300144467&s=11022.00&t=20231109T203226"
    b = "https://ofd.beeline.kz/t/?i=739826471308&f=010102493800&s=1000.0&t=20240111T192925"
    data = format_data(parse_cheque_site(a))
    for row in data["no_format_header"].split("\n"):
        data.update(search_in_text(row))

if __name__ == "__main__":
    asyncio.run(test())
