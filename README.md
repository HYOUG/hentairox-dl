# HentaiRoxDL
A simple command line python script to download galleries from [**HentaiRox**](https://hentairox.com/) using the `requests`, `BeautifulSoup`, `tqdm` and `colorama` modules.

💾 Installation
============
```bash
git clone https://github.com/HYOUG/HentaiRoxDL.git
cd hentairoxdl
```
or, `Code button` > `Download ZIP`

🔌 Requirements
============
```bash
requests==2.26.0
colorama==0.4.4
tqdm==4.62.1
beautifulsoup4==4.10.0
```

⚙️ Usage
============
```bash
python hentairoxdl.py [-h] [-o PATH] [-f FILENAME_MODEL] [-p START_INDEX STOP_INDEX] [-a ARCHIVE_NAME] [-t WORKERS_NUM] [-m] GALLERY_URL [GALLERY_URL ...]
```

Argument | Description | Default value(s) | Example
------------ | ------------- | ------------- | -------------
`GALLERY_URL` | Targeted gallery page URL. | ∅ | https://hentairox.com/gallery/362424/
-h, --help | Show the help message and exit. | ∅ | -h
-o, --output `PATH`| Specifies the path of the folder which the downloaded images will be saved in. | "./downloads" | -o C:\Users\johndoe\Downloads
-f, --filename `FILENAME_MODEL`| Formats the name of the downloaded images with context variables. Available variables: `gallery_name`, `gallery_id`, `pages_num`, `page_nums` | "{page_num}_{gallery_id}" | -m no.{page_num}
-p, --pages `START_INDEX` `STOP_INDEX` | Specifies the portion of the gallery to download. | [0, -1] | -p 5 -10
-a, --archive `ARCHIVE_NAME` | Archives downloaded pictures in a zip file and specifies the name of it. | None | -a archived_gallery
-t, --threads `THREADS_NUM` | Specifies the number of threads that the program uses to download the gallery. | 1 | -t 4 
-m, --metadata | Save the gallery's metadata in a file (metadata.txt). | False | -m

⚠️ Disclaimer
============
- I do not encourage anybody to use HentaiRoxDL in an unfair way (mirroring, harvesting, dumping, etc.).
- I do not assume responsibility for any sanction due to the use of HentaiRoxDL.

📜 License
============
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
