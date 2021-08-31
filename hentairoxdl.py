#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by "HYOUG"

from argparse import ArgumentParser
from os import makedirs, remove
from os.path import basename, exists, join
from random import choice
from zipfile import ZIP_DEFLATED, ZipFile

from bs4 import BeautifulSoup
from requests_cache import CachedSession
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


def dl_gallery(gallery_url:str, output:str, model:str, pages:list, zipfile: bool or str, log:bool, info:bool) -> None:
    """
    Download the given Hentai Rox Gallery

    Parameters
    ----------
    gallery_url : str
        [description]
    output : str
        [description]
    model : str
        [description]
    pages : list
        [description]
    zipfile : boolorstr
        [description]
    log : bool
        [description]
    info : bool
        [description]
    """
    
    gallery_id = [i for i in gallery_url.split("/") if i != ""][-1]
    s = CachedSession("cached_session", backend="memory")
    

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
        fp = join(output, "#info.txt")
        f = open(fp, "w", encoding="utf-8")
        f.write(f"Gallery name: {gallery_title}\n")
        f.write(f"URL: {gallery_url}\n")
        f.write(f"Pages: {pages_num}\n\n")
        f.write(f"Metadata:\n")
        for item in metadata.items():
            f.write(f"* {item[0]}: {', '.join(item[1])}\n")
        f.close()

    if zipfile is not None:
        zf = ZipFile(join(output, f"{zipfile}.zip"), "w", ZIP_DEFLATED)
        zf.write(fp, basename(fp))
        remove(fp)

    p_start = list(range(pages_num)).index(list(range(pages_num))[pages[0]])
    p_stop = list(range(pages_num)).index(list(range(pages_num))[pages[1]])

    bar = tqdm(
        iterable=range(p_start, p_stop),
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
                "{pages_num}": str((p_stop-1)-p_start)}
            filename = model
            for (var_name, var_value) in model_vars.items():
                filename = filename.replace(var_name, var_value)
            fp = join(output, f"{filename}.{im_ext}")
            f = open(fp, "wb")
            f.write(response.content)
            f.close()
            zf.write(fp, basename(fp))
            remove(fp)
    zf.close()


def main():
    parser = ArgumentParser()
    parser.add_argument("gallery_url",
                        help="The URL from the targeted gallery page",
                        metavar="GALLERY_URL")
    parser.add_argument("-o", "--output",
                        default="./downloads",
                        help="Path for the output for the downloaded content",
                        metavar="PATH")
    parser.add_argument("-m", "--model",
                        nargs="+",
                        default="{gallery_id}_{page_num}",
                        help="Filename model given to the downloaded pictures",
                        metavar="FILENAME_MODEL")
    parser.add_argument("-p", "--pages",
                        nargs=2,
                        default=[0, -1],
                        type=int,
                        help="Specific page indexes to download",
                        metavar=("START_INDEX", "STOP_INDEX"))
    parser.add_argument("-z", "--zipfile",
                        nargs="+",
                        default=None,
                        help="Archive the downloaded pictures in a zip file with the given name",
                        metavar="ZIPFILE_NAME")           
    parser.add_argument("-l", "--log",
                        action="store_true",
                        default=False,
                        help="Display every step of the downloading process")
    parser.add_argument("-i", "--info",
                        action="store_true",
                        default=False,
                        help="Save gallery info (title, author, metadata, etc.) in a file (#info.txt)")
    args = parser.parse_args()
    dl_gallery(args.gallery_url, args.output, ' '.join(args.model), args.pages, ' '.join(args.zipfile), args.log, args.info)


if __name__ == "__main__":
    main()
