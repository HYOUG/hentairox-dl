#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script by HYOUG

from argparse import ArgumentParser
from classes.Downloader import Downloader
from utils.page_parser import *


def main():
    parser = ArgumentParser(prog="HentairoxDL.py",
                            description="Download content from an Hentairox gallery",
                            epilog="Made with <3 by HYOUG")
    parser.add_argument("gallery_url",
                        help="The URL from the targeted gallery page",
                        metavar="GALLERY_URL")
    parser.add_argument("-o", "--output",
                        default="./downloads/{gallery_name}/",
                        help="Set the output path",
                        metavar="PATH",
                        dest="output")
    parser.add_argument("-f", "--filename",
                        default="{gallery_id}_{page_num}",
                        help="Set the downloaded pictures filename template",
                        metavar="FILENAME",
                        dest="filename")
    parser.add_argument("-p", "--pages",
                        default=":",
                        help="Set the pages indexes range to download",
                        metavar="PAGE_RANGES",
                        dest="pages")
    parser.add_argument("-a", "--archive",
                        default=None,
                        help="Archive the downloaded pictures",
                        metavar="ARCHIVE_NAME",
                        dest="archive_name")
    parser.add_argument("-m", "--metadata",
                        action="store_true",
                        default=False,
                        help="Save the gallery's metadata into a text file")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        default=False,
                        help="Increase output verbosity")
    parser.add_argument("-nc", "--no-color",
                        action="store_false",
                        default=True,
                        help="Disable color display",
                        dest="color_enabled")
    parser.add_argument("-q", "--quiet",
                        action="store_true",
                        default=False,
                        help="Quiet (no output)")

    args = parser.parse_args()
    dl = Downloader(args.color_enabled, args.verbose, args.quiet)
    dl.dl_gallery(args.gallery_url, args.output, args.filename, args.pages, args.archive_name, args.metadata)


if __name__ == "__main__":
    main()
