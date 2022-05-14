from multiprocessing import cpu_count
from os import listdir, makedirs
from os.path import exists, join
from threading import Event, Lock, Thread
from time import perf_counter, sleep
from zipfile import ZIP_DEFLATED, ZipFile

from bs4 import BeautifulSoup
from utils.output_parser import parse_output
from utils.page_parser import parse_pages
from pathvalidate import sanitize_filepath
from requests import get
from requests.exceptions import RequestException
from tqdm import tqdm

from classes.Colors import Colors


class Downloader:
    
    def __init__(self, color_enabled:bool, verbose:bool, quiet:bool) -> None:
        """
        Create a `Downloader` object

        Parameters
        ----------
        color_enabled : bool
            _description_
        verbose : bool
            _description_
        quiet : bool
            _description_
        """
        self.color_enabled = color_enabled
        self.verbose = verbose
        self.quiet = quiet
        
        self.PBAR_LOCK = Lock()
        self.CANCEL_LOCK = Lock()
        self.ARCHIVE_LOCK = Lock()
        self.COLORS = Colors(self.color_enabled)
        self.IMAGE_EXTENSIONS = ["jpg", "png", "gif"]

        self.metadata = dict()
        self.gallery_proprties = dict()
        self.dl_cancelled = bool()
        self.archived = bool()
        self.filename = str()
        self.output = str()
        self.archive_name = str()
        self.base_url = str()
        self.parsed_output = str()
        
            
    def dl_pages(self, page_list:list) -> None:
        """
        Download HentaiRox gallery pages from from the base URL of the gallery and the given `page_list`

        Parameters
        ----------
        page_list : list
            _description_

        Raises
        ------
        SystemExit
            _description_
        """
        for page_num in page_list:
            formatfound = False
            for extension in self.IMAGE_EXTENSIONS:
                try:
                    response = get(f"{self.base_url}/{page_num+1}.{extension}", timeout=5)
                    response.raise_for_status()
                    formatfound = True
                    img_extension = extension
                    break
                except RequestException as e:
                    raise SystemExit(f"\n{self.COLORS.ERROR}{e}")
            if formatfound:
                self.gallery_proprties["page_num"] = str(page_num)
                parsed_filename = f"{self.filename.format(**self.gallery_proprties)}.{img_extension}"
                if not self.archived:
                    fp = join(self.parsed_output, parsed_filename)
                    fp = sanitize_filepath(fp)
                    f = open(fp, "wb")
                    f.write(response.content)
                    f.close()                   
                else:
                    with self.ARCHIVE_LOCK:
                        with self.archive.open(parsed_filename, "w") as img:
                            img.write(response.content)
            else:
                print(f"{self.COLORS.WARNING}The file format of the page num. {page_num} have not been found")

            with self.PBAR_LOCK:
                if not self.quiet:
                    self.progress_bar.update()
                    
            if not self.is_downloading.is_set():
                break
    
    
    def dl_gallery(self, gallery_url:str, output:str, filename:str, pages:str, archive_name: str | type[None],
                   metadata:bool) -> None:
        """
        Download an HentaiRox gallery from the given `gallery_url`

        Parameters
        ----------
        gallery_url : str
            _description_
        output : str
            _description_
        filename : str
            _description_
        pages : str
            _description_
        archive_name : str or type[None]
            _description_
        metadata : bool
            _description_

        Raises
        ------
        SystemExit
            _description_
        """       
        self.gallery_proprties["gallery_id"] = [i for i in gallery_url.split("/") if i != ""][-1]
        thread_list = []
        start_time = perf_counter()
        self.archived = archive_name is not None
        self.filename = filename
        self.output = output
        self.archive_name = archive_name
        self.is_downloading = Event()
        self.is_downloading.set()
        
        try:
            response = get(gallery_url, timeout=5)
            response.raise_for_status()
        except RequestException as e:
            raise SystemExit(f"\n{self.COLORS.ERROR}{e}")

        soup = BeautifulSoup(response.content, "html.parser")

        self.gallery_proprties["gallery_name"] = soup.find("h1").string                    
        metadata_tags = soup.find_all("span", {"class": "item_name"})
        
        for metadata_tag in metadata_tags:
            tag_type = list(filter(lambda el: el != "", metadata_tag.parent["href"].split("/")))[0]
            if not tag_type in list(self.metadata.keys()): 
                self.metadata[tag_type] = []
            if metadata_tag.string is None:
                metadata_tag = metadata_tag.contents[0]
            tag_value = metadata_tag.string.strip()
            self.metadata[tag_type].append(tag_value)

        page_num_node = soup.find("li", {"class": "pages"})
        self.gallery_proprties["pages_num"] = int(page_num_node.string.split(" ")[0])
        first_img = soup.find("img", {"class": "lazy preloader"})
        self.base_url = "/".join(first_img["data-src"].split("/")[:-1]) + "/"
        
        page_list = parse_pages(pages, self.gallery_proprties["pages_num"])
        page_len = len(page_list)
        threads_num = min(cpu_count(), page_len)
        
        if not self.quiet:
            print(f"\n{self.COLORS.TITLE}Gallery{self.COLORS.RESET}: {self.gallery_proprties['gallery_name']}")
            if self.verbose:
                print(f"{self.COLORS.SUBTITLE}Lenght{self.COLORS.RESET}: {self.gallery_proprties['pages_num']} pages")
                for (metadata_key, metadata_value) in self.metadata.items():
                    metadata_values = ", ".join(metadata_value[0:min(4, len(metadata_value))])
                    metadata_title = metadata_key.capitalize()
                    if len(metadata_value) > 10: metadata_values += ", ..."
                    print(f"{self.COLORS.SUBTITLE}{metadata_title}{self.COLORS.RESET}: {metadata_values}")
            print()

        self.parsed_output = parse_output(self.output, self.gallery_proprties)
        if not exists(self.parsed_output):
            makedirs(self.parsed_output)

        if self.archived:
            fp_archive = join(self.parsed_output, f"{archive_name}.zip")
            if f"{archive_name}.zip" not in listdir(self.parsed_output):
                self.archive = ZipFile(fp_archive, "w", ZIP_DEFLATED)
            else:
                self.archive = ZipFile(fp_archive, "a", ZIP_DEFLATED)

        if not self.quiet:
            bar_format = "Download |{bar:30}| [{n_fmt}/{total_fmt}] ({percentage:.0f}%)"
            if self.verbose:
                bar_format += " [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
            self.progress_bar = tqdm(iterable=range(page_len),
                                     total=page_len,
                                     bar_format=bar_format,
                                     ascii=".▌█",
                                     unit=" img")                

        for i in range(threads_num):
            thread_pages = page_list[i::threads_num]      
            thread = Thread(target=self.dl_pages, args=(thread_pages,), daemon=True)
            thread.start()
            thread_list.append(thread)
            
        try:
            while True:
                sleep(0.1)
                if not True in [t.is_alive() for t in thread_list]:
                    if not self.quiet:
                        with self.PBAR_LOCK:
                            self.progress_bar.close()   
                    break
        except KeyboardInterrupt:
            self.is_downloading.clear()
            for thread in thread_list: thread.join()
            if not self.quiet:
                with self.PBAR_LOCK:
                    self.progress_bar.close()   
            print(f"\n{self.COLORS.ERROR}Download cancelled{self.COLORS.RESET}")
            exit()               

        if metadata:
            metadata_text = str()
            metadata_text += f"Gallery: {self.gallery_proprties['gallery_name']}\n"
            metadata_text += f"URL: {gallery_url}\n"
            metadata_text += f"Pages: {self.gallery_proprties['pages_num']}\n\n"
            for (category, tag_list) in self.metadata.items():
                if len(tag_list) > 0:
                    metadata_text += f"{category.capitalize()}: {', '.join(tag_list)}\n"
            if not self.archived:
                metadata_filepath = join(self.parsed_output, "metadata.txt")
                with open(metadata_filepath, "w", encoding="utf-8") as metadata_file:
                    metadata_file.write(metadata_text)
            else:
                with self.archive.open("metadata.txt", "w") as metadata_file:
                    metadata_file.write(bytes(metadata_text, "utf-8"))
            self.archive.close()
                
        end_time = perf_counter()
        dl_time = round(end_time-start_time, 2)
        print(f"\n{self.COLORS.SUCCESS}Download finished in {dl_time} seconds")
