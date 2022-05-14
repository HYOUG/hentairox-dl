hentairoxdl
============
A simple CLI to download galleries from [**HentaiRox**](https://hentairox.com/) written in Python.

💾 Installation
============
```console
# Clone the repository
$ git clone https://github.com/HYOUG/hentairoxdl.git

# Change the working directory to hentairoxdl
$ cd hentairoxdl

# Install the requirements
$ python3 -m pip install -r requirements.txt
```

🔌 Requirements
============
```bash
beautifulsoup4==4.11.1
colorama==0.4.4
pathvalidate==2.5.0
requests==2.26.0
tqdm==4.62.3
```

⚙️ Usage
============
```console
# Download a gallery
$ python3 hentairoxdl.py [OPTIONS] GALLERY_URL
```

**GALLERY_URL**  
The HentaiRox gallery to download.

**-h, --help**  
Show this help message and exit.

**-o, --output `PATH`**  
Specify the path for the downloaded pictures.  
Default PATH="./downloads/{gallery_name}/"  
E.g: -o ./saved/{gallery_id}-{gallery\_name}

**-f, --filename `FILENAME`**  
Specify the filename model given to the downloaded pictures.  
Default FILENAME="{gallery_id}\_{page_num}"  
E.g: -f number\_{page_num}

**-p, --pages `PAGE_RANGES`**  
Specify the page indexes range to download.  
Default PAGES_RANGES=":"  
E.g: -p 0:100/5

**-a, --archive `ARCHIVE_NAME`**  
Archive the downloaded pictures in a .zip file with the given name.  
E.g: -a personal_archive

**-m, --metadata**  
Save the gallery's metadata into a file (metadata.txt).

**-nc, --no-color**  
Disable color display.

**-v, --verbose**  
Increase output verbosity.

**-q, --quiet**  
Run the download without output.

> Avaible templates : `{gallery_id}`, `{gallery_name}`, `{pages_num}`, `{page_num}`.  
> The `{page_num}` value is only working for the `FILENAME` argument. 

⚠️ Disclaimer
============
- I do not endorse unsing hentairoxdl in an unfair way (mirroring, harvesting, etc.).
- I do not assume responsibility for any sanction due to the use of hentairoxdl.
- Due to the lack of moderation on hentairox.com, some users may find disturbing content on the website.

📋 TODO
============
- [ ] Precise exception handling   
- [ ] DOCSTRINGS  
- [ ] Advanced template features

📜 License
============
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
