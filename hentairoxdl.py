#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by "HYOUG"

from argparse import ArgumentParser
from os import makedirs
from os.path import exists, join
from random import choice
from bs4 import BeautifulSoup
from requests import Session
from tqdm import tqdm

user_agent = {"User-Agent": choice(open("user-agents.txt", "r").read().split("\n"))}
metadata = {
    "parodies": [],
    "characters": [],
    "tags": [],
    "artists": [],
    "groups": [],
    "languages": [],
    "category": [],
}
IMAGE_EXTENSIONS = ["jpg", "png", "gif"]
FORBIDDEN_CHARS = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]


def dl_gallery(gallery_url: str, output:str, model:str, pages:list, log:bool, info:bool) -> None:
    """
    Download the given Hentai Rox Gallery

    Parameters
    ----------
    gallery_url : str
        The targeted gallery URL
    output : str
        [description]
    filename_model : str
        [description]
    index : str
        [description]
    log : bool
        [description]   
    info : bool
        [description] 
    """
    
    gallery_id = [i for i in gallery_url.split("/") if i != ""][-1]
    s = Session()
    


    def display_log(event:str) -> None:
        if log:
            print(event)


    display_log(f"Generating output folder...")
    if not exists(output):
        makedirs(output)

    display_log("Fetching gallery metadata...")
    response = s.get(gallery_url, headers=user_agent)
    soup = BeautifulSoup(response.content, "html.parser")

    gallery_title = soup.find("h1").string
    metadata_tags = soup.find_all("span", {"class": "item_name"})
    for metadata_tag in metadata_tags:
        metadata_type = metadata_tag.parent["href"]
        if metadata_type.startswith("/parody"):
            metadata["parodies"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/character"):
            metadata["characters"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/tag"):
            metadata["tags"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/artist"):
            metadata["artists"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/group"):
            metadata["groups"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/language"):
            metadata["languages"].append(metadata_tag.contents[0])
        elif metadata_type.startswith("/category"):
            metadata["category"].append(metadata_tag.contents[0])
        else:
            display_log(f"Unknown metadata tag : {metadata_type}")

    page_num_node = soup.find("li", {"class": "pages"})
    pages_num = int(page_num_node.string.split(" ")[0])
    display_log(f"Getting URL pattern...")
    first_img = soup.find("img", {"class": "lazy preloader"})
    pattern = "/".join(first_img["data-src"].split("/")[:-1]) + "/"

    if info:
        display_log("Writing gallery metadata onto #info.txt...")
        f = open(f"{output}/#info.txt", "w", encoding="utf-8")
        f.write(f"Gallery name: {gallery_title}\n")
        f.write(f"URL: {gallery_url}\n")
        f.write(f"Pages: {pages_num}\n\n")
        f.write(f"Metadata:\n")
        for item in metadata.items():
            f.write(f"* {item[0]}: {', '.join(item[1])}\n")
        f.close()

    p_start = list(range(1, pages_num+1)).index(list(range(1, pages_num+1))[pages[0]])
    p_stop = list(range(1, pages_num+1)).index(list(range(1, pages_num+1))[pages[1]])

    bar = tqdm(
        iterable=range(p_start, p_stop),
        initial=0,
        total=p_stop-p_start,
        desc="Downloading :",
        bar_format="{desc} |{bar}| ({n_fmt}/{total_fmt})",
        ncols=60,
        ascii=".▌█")

    for i in bar:
        for ext in IMAGE_EXTENSIONS:
            response = s.get(f"{pattern}/{i}.{ext}")
            if response.status_code == 200:
                formatfound = True
                im_ext = ext
                break
            formatfound = False
        if formatfound:
            model_vars = {
                "{gallery_title}": gallery_title,
                "{gallery_id}": gallery_id,
                "{page_num}": str(i),
                "{pages_num}": str(pages_num)}
            filename = model
            for (var_name, var_value) in model_vars.items():
                filename = filename.replace(var_name, var_value)
            f = open(join(output, f"{filename}.{im_ext}"), "wb")
            f.write(response.content)
            f.close()


def main():
    parser = ArgumentParser()
    parser.add_argument("gallery_url",
                        help="The URL from the targeted gallery page")
    parser.add_argument("-o", "--output",
                        metavar="PATH",
                        default="./downloads",
                        help="Path for the output for the downloaded content")
    parser.add_argument("-m", "--model",
                        metavar="MODEL",
                        default="{gallery_id}_{page_num}",
                        help="Filename model given to the downloaded pictures")
    parser.add_argument("-p", "--pages",
                        metavar=("START_IDX", "STOP_IDX"),
                        default=[0, -1],
                        nargs=2,
                        type=int,
                        help="Specific page indexes to download")
    parser.add_argument("-l", "--log",
                        default=False,
                        help="Display every step of the downloading process",
                        action="store_true")
    parser.add_argument("-i", "--info",
                        default=False,
                        help="Save gallery info (title, author, metadata, etc.) in a file (#info.txt)",
                        action="store_true")
    args = parser.parse_args()
    dl_gallery(args.gallery_url, args.output, args.model, args.pages, args.log, args.info)


if __name__ == "__main__":
    main()
