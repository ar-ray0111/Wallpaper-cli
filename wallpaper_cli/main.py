import sys
from typing import List
import aiohttp
import asyncio
import aiofiles
import os
import json

home_directory = os.path.expanduser("~")
RATE_LIMIT = 45
REQUEST_WAIT = 60 / RATE_LIMIT


async def get_urls(tags: str) -> list:
    wall_list = []
    url = f"https://wallhaven.cc/api/v1/search?q={tags}&sorting=random"
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    json_res = await response.json()
                    for i in json_res["data"]:
                        wall_list.append(i["path"])
                except json.JSONDecodeError as e:
                    print(f"Error with json data {e}")
                    print(f"Content: { await response.text()}")
    return wall_list


async def download_wall(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if res.status == 200:
                filename = os.path.join(f"{home_directory}/walls/", url.split("/")[-1])
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(await res.read())
                print(f"Downloaded: {filename}")
            else:
                print(f"failed to download {url}: status code: {res.status}")


async def download_walls(wall_urls: list) -> None:
    if not os.path.exists(f"{home_directory}/walls"):
        os.makedirs(f"{home_directory}/walls")

    tasks = []
    for i, url in enumerate(wall_urls):
        tasks.append(download_wall(url))
        if (i + 1) % RATE_LIMIT == 0:
            print(f"Rate limit reached, sleeping for {REQUEST_WAIT}")
            await asyncio.sleep(REQUEST_WAIT)

    await asyncio.gather(*tasks)


async def main(tag: List[str]):
    tags = " ".join(tag)

    wall_urls = await get_urls(tags)
    await download_walls(wall_urls)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python main.py <tags>")
        sys.exit()
    else:
        tags = sys.argv[1:]
        asyncio.run(main(tags))
