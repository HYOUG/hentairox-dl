# HentaiRoxDL
A simple python script that download a given gallery using the `requests_cache`, `BeautifulSoup` and `tqdm` modules.

## 💾 Installation
```bash
git clone https://github.com/HYOUG/HentaiRoxDL.git
cd hentairoxdl
```
or, `Code button` > `Download ZIP`

## 🔌 Requirements
```bash
tqdm==4.62.1
beautifulsoup4==4.9.3
requests_cache==0.7.4
```

## ⚙️ Usage 
```bash
python hentairoxdl.py [-h] [-o PATH] [-m FILENAME_MODEL] [-p START_INDEX STOP_INDEX] [-l] [-i] GALLERY_URL
```

Argument | Description | Default value | Example
------------ | ------------- | ------------- | -------------
GALLERY_URL* | The URL from the targeted gallery page |  | https://hentairox.com/gallery/380508/
-h, --help | Show the help message and exit |  | -h
-o, --output PATH| Path for the output for the downloaded content | ./downloads | -o C:\Users\johndoe\Downloads
-m, --model FILENAME_MODEL| Filename model given to the downloaded pictures | {gallery_id}_{page_num} | -m {gallery_title} : ({page_num})
-p, --pages START_INDEX STOP_INDEX | Specific page indexes to download | 0 -1 | -p 0 101
-l, --log | Display every step of the downloading process | False | -l
-i, --info | Save gallery info (title, author, metadata, etc.) in a file (#info.txt) | False | -i

Arguments with a `*` are mandatory.

## ⚠️ Disclaimer
- I do not encourage anybody to use HentaiRoxDL in an unfair way (mirroring, harvesting, dumping, etc.).
- I do not assume responsibility for any sanction due to the use of HentaiRoxDL.

## 👍 Special Thanks
Thanks to [Peter Bowen AKA pzb](https://github.com/pzb) for the user-agent list.

## 📜 License 
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
