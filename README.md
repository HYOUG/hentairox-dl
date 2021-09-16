# HentaiRoxDL
A simple command line python script to download galleries from [**HentaiRox**](https://hentairox.com/) using the `requests`, `BeautifulSoup` and `tqdm` modules.

## 💾 Installation
```bash
git clone https://github.com/HYOUG/HentaiRoxDL.git
cd hentairoxdl
```
or, `Code button` > `Download ZIP`

## 🔌 Requirements
```bash
tqdm==4.62.1
requests==2.26.0
colorama==0.4.4
beautifulsoup4==4.10.0
```

## ⚙️ Usage 
```bash
python hentairoxdl.py [-h] [-o PATH] [-m FILENAME_MODEL] [-p START_INDEX STOP_INDEX] [-z ZIPFILE_NAME] [-l] [-i] GALLERY_URL [GALLERY_URL ...]
```

Argument | Description | Default value | Example
------------ | ------------- | ------------- | -------------
GALLERY_URL | Targeted gallery page URL |  | https://hentairox.com/gallery/362424/
-h, --help | Show the help message and exit |  | -h
-o, --output `PATH`| Specifies the path of the folder in which the downloaded images are saved | ./downloads | -o C:\Users\johndoe\Downloads
-f, --filename `FILENAME_MODEL`| Format the name of the downloaded images with context variables. Available variables: gallery_name, gallery_id, pages_num, page_num. | {page_num}_{gallery_id} | -m no.{page_num}
-p, --pages `START_INDEX` `STOP_INDEX` | Specifies the portion of the gallery to download | 0 -1 | -p 0 101
-a, --archive `ARCHIVE_NAME` | Archive downloaded pictures in a zip file and specifies the name of it | None | -a archived_gallery
-t, --threads `THREADS_NUM` | Specifies the number of threads that the program uses to download the gallery | 1 | -t 4 
-m, --metadata | Backup the metadata from the gallery in a file #metadata.txt | False | -i

## ⚠️ Disclaimer
- I do not encourage anybody to use HentaiRoxDL in an unfair way (mirroring, harvesting, dumping, etc.).
- I do not assume responsibility for any sanction due to the use of HentaiRoxDL.

## 📜 License 
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
