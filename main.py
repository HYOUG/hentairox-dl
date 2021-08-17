#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by "HYOUG"

from requests import session
from bs4 import BeautifulSoup
from os import mkdir, listdir


IMAGE_EXTENSIONS = ["jpg", "png", "gif"]
FORBIDDEN_CHARS = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]


def dl_gallery(target_url: str) -> None:
    """
    Download the given Hentai Rox Gallery

    Parameters
    ----------
    target_url : str
        The targeted gallery URL
    """
    gallery_id = [i for i in target_url.split("/") if i != ""][-1]
    metadata = {
        "parodies": [],
        "characters": [],
        "tags": [],
        "artists": [],
        "groups": [],
        "languages": [],
        "category": [],
    }

    with session() as s:
        print("Fetching gallery metadata")
        response = s.get(target_url)
        soup = BeautifulSoup(response.content, "html.parser")
        gallery_name = soup.find("h1").string
        metadata_tags = soup.find_all("span", {"class": "item_name"})
        
        for metadata_item in metadata_tags:
            metadata_type = metadata_item.parent["href"]
            if metadata_type.startswith("/parody"):
                metadata["parodies"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/character"):
                metadata["characters"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/tag"):
                metadata["tags"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/artist"):
                metadata["artists"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/group"):
                metadata["groups"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/language"):
                metadata["languages"].append(metadata_item.contents[0])
            elif metadata_type.startswith("/category"):
                metadata["category"].append(metadata_item.contents[0])
            else:
                print(f"Unknown metadata tag : {metadata_type}")

        page_num_node = soup.find("li", {"class": "pages"})
        page_num = int(page_num_node.string.split(" ")[0])

        print(f"Getting URL pattern")
        page_url = f"{target_url}/1".replace("gallery", "view")
        response = s.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")
        pattern = "/".join(soup.find(id="gimg")["src"].split("/")[:-1])
        
        print(f"Generating new folder")
        try:
            folder_name = "".join([i for i in gallery_name if i not in FORBIDDEN_CHARS])
            if len(folder_name) > 255:
                folder_name = folder_name[:255]
            mkdir(f"./downloads/{folder_name}")
        except FileExistsError:
            print(f"The folder ./downloads/{folder_name}/ already exist")

        f = open(f"./downloads/{folder_name}/#info.txt", "w", encoding="utf-8")
        f.write(f"Name  : {gallery_name}\n")
        f.write(f"URL   : {target_url}\n")
        f.write(f"Pages : {page_num}\n\n")
        f.write(f"Metadata :\n")
        for item in metadata.items():
            f.write(f"* {item[0]}: {', '.join(item[1])}\n")
        f.close()

        downloaded_im = ["".join(i.split(".")[:-1]) for i in listdir(f"./downloads/{folder_name}/")]

        for i in range(1, page_num+1):
            if f"{gallery_id}_{i}" not in downloaded_im:
                print(f"Downloading page n° {i}/{page_num}")
                for ext in IMAGE_EXTENSIONS:
                    response = s.get(f"{pattern}/{i}.{ext}")
                    if response.status_code == 200:
                        formatfound = True
                        im_ext = ext
                        break
                    formatfound = False
                if formatfound:
                    f = open(f"./downloads/{folder_name}/{gallery_id}_{i}.{im_ext}", "wb")
                    f.write(response.content)
                    f.close()
            else:
                print(f"Skiping page n° {i}/{page_num}")

    print(f"Download finished, the output is located in the ./downloads/{folder_name}/ folder.")


def main():
    target_url = input("Enter gallery URL : ")
    dl_gallery(target_url)


if __name__ == "__main__":
    main()