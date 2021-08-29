# HentaiRoxDL
A simple python script that download a given gallery using the `requests`, `BeautifulSoup` and `tqdm` modules.

## 💾 Installation
```bash
git clone https://github.com/HYOUG/HentaiRoxDL.git
```
or, `Code button` > `Download ZIP`

## 🔌 Requirements
```bash
requests==2.26.0
tqdm==4.62.1
beautifulsoup4==4.9.3
```

## ⚙️ Usage 
```bash
python hentairoxdl.py [-h] [-o PATH] [-m MODEL] [-p START_IDX STOP_IDX] [-l] [-i] gallery_url
```

Argument | Value(s) | Description | Default value | Example
------------ | ------------- | ------------- | ------------- | -------------
gallery_url | URL | The URL from the targeted gallery page | / | https://hentairox.com/gallery/380508/
-h, --help | / | Show this help message and exit | / | /
-o, --output | Path | Path for the output for the downloaded content | ./downloads | C:\Users\johndoe\Downloads
-m, --model | Filename Model | Filename model given to the downloaded pictures | {gallery_id}_{page_num} | {gallery_title} : ({page_num})
-p, --pages | StartIndex, StopIndex | Specific page indexes to download | [0, -1] | 0 101
-l, --log | / | Display every step of the downloading process | False | /
-i, --info | / | Save gallery info (title, author, metadata, etc.) in a file (#info.txt) | False | /

## ⚠️ Disclaimer
- I do not encourage anybody to use HentaiRoxDL in an unfair way (mirroring, harvesting, dumping, etc.).
- I do not assume responsibility for any sanction due to the use of HentaiRoxDL.

## 👍 Special Thanks
Thanks to [Peter Bowen aka pzb](https://github.com/pzb) for the user-agent list.

## 📜 License 
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
