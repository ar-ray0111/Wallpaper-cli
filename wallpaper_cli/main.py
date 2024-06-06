import sys
import requests
import json
import os


def get_urls(tags: str) -> list:
    wall_list = []
    url = f"https://wallhaven.cc/api/v1/search?q={tags}&sorting=random"
    print(url)
    res = requests.get(url)

    if res.status_code == 200:
        try:
            json_res = res.json()
            for i in json_res['data']:
                wall_list.append(i['path'])

        except json.JSONDecodeError as e:
            print("JSONDecoder", e)
            print("Content:", res.content)
    return wall_list


def download_walls(wall_urls: list) -> None:
    if not os.path.exists("./walls"):
        os.makedirs("./walls")
    for url in wall_urls:
        res = requests.get(url)

        if res.status_code == 200:
            filename = os.path.join("./walls", url.split('/')[-1])
            with open(filename, "wb") as f:
                f.write(res.content)
                print(f"Downloaded: {filename}")

        else:
            print("Failed")


def main():
    tags = sys.argv[1:]

    tags = ",".join(tags)
    print(tags, type(tags))

    wallpaper_list = get_urls(tags)

    download_walls(wallpaper_list)


if __name__ == "__main__":
    main()
