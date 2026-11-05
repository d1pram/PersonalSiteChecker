import asyncio
import logging

import aiohttp
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup


async def parse(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                html = await response.text()

                # soup = BeautifulSoup(html, "html.parser")

                document = BufferedInputFile(
                    html.encode("utf-8"),
                    filename="page.html",
                )

                return document
    except Exception as err:
        logging.error(err)
        return None