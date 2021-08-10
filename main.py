#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by "HYOUG"

from requests import session
from bs4 import BeautifulSoup
from os import mkdir


def check_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def dl_gallery(target_url: str) -> None:
    """
    Download the given Hentai Rox Gallery

    Parameters
    ----------
    target_url : str
        The targeted gallery URL
    """
    gallery_id = list(filter(check_int, target_url.split("/")))[0]

    with session() as s:
        print("Getting number of pages...")
        response = s.get(target_url)
        soup = BeautifulSoup(response.content, "html.parser")
        page_node = soup.find("li", {"class": "pages"})
        page_num = int(page_node.contents[0].split(" ")[0])
        
        print(f"Getting URL pattern...")
        page_url = f"{target_url}/1".replace("gallery", "view")
        response = s.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")
        pattern = "/".join(soup.find(id="gimg")["src"].split("/")[:-1])
        
        print(f"Generating new folder : .downloads/{gallery_id}/")
        mkdir(f"./downloads/{gallery_id}")

        for i in range(1, page_num+1):
            print(f"Downloading page n°{i} /{page_num}...")
            response = s.get(f"{pattern}/{gallery_id}_{i}.jpg")
            im = open(f"./downloads/{gallery_id}/{i}.jpg", "wb")
            im.write(response.content)
            im.close()

    print("Done !")


def main():
    target_url = input("Enter gallery URL : ")
    dl_gallery(target_url)


if __name__ == "__main__":
    main()