# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     365spider
   Description :
   Author :       dean
   date：          2020/7/24 17:55
-------------------------------------------------
   Change Activity:
                   17:55
-------------------------------------------------
"""
import asyncio
import platform
import os
import sys

now_path = os.getcwd()
root_path = now_path.split("scrapy_aio")[0] + "/scrapy_aio"
os.chdir(root_path)
sys.path.append(root_path)
from template import settings
from scrapy_aio.conf.settings import Settings
from scrapy_aio.core.crawler import Crawler
from scrapy_aio.http.request import Request
from scrapy_aio.spiders import Spider
from scrapy_aio.log_handler import LogHandler
from rich.progress import track, Progress

logger = log = LogHandler(__name__)

sysstr = platform.system()
if sysstr == "Windows":
    print("Call Windows tasks")
    import selectors

    selector = selectors.SelectSelector()  # New line
    loop = asyncio.SelectorEventLoop(selector)
elif sysstr == "Linux":
    print("Call Linux tasks")
    import uvloop

    loop = uvloop.new_event_loop()
else:
    loop = asyncio.get_event_loop()


class ComSpider(Spider):
    name = 'test'

    def start_requests(self):
        yield Request(url='http://youdao.com', dont_filter=True, callback=self.parse)

    async def parse(self, response):
        logger.warning(f"parse {response.meta}")
        logger.warning(f"parse {response.url}")
        meta = {
            "download_timeout": 60,
        }
        for i in range(100):
            yield Request(url=f"https://www.baidu.com/s?wd={i}", meta=meta, dont_filter=True,
                          callback=self.parse_content)

    async def parse_content(self, response):
        # while not progress.finished:
        progress.update(download_task, advance=1)
        logger.debug(response.url)

        yield {"result": response.url}


async def start():
    await crawler.crawl()
    await crawler.start()


if __name__ == '__main__':
    with Progress() as progress:
        download_task = progress.add_task("[red]Downloading...", total=100)
        s = Settings()
        s.setmodule(settings)
        crawler = Crawler(ComSpider, s, loop)
        loop.run_until_complete(start())
        loop.close()
