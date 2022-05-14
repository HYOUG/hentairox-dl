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
$ python hentairoxdl.py --help
usage: HentairoxDL.py [-h] [-o PATH] [-f FILENAME] [-p PAGE_RANGES]
                      [-a ARCHIVE_NAME] [-m] [-v] [-nc] [-q]
                      GALLERY_URL

Download content from an Hentairox gallery

positional arguments:
  GALLERY_URL           The URL from the targeted gallery page

options:
  -h, --help                 Dhow this help message and exit
  -o, --output PATH          Set the output path
  -f, --filename FILENAME    Set the downloaded pictures filename template
  -p, --pages PAGE_RANGES    Set the page indexes range to download
  -a, --archive ARCHIVE_NAME Archive the downloaded pictures
  -m, --metadata             Save the gallery metadata into a text file
  -v, --verbose              Increase output verbosity
  -nc, --no-color            Disable color display
  -q, --quiet                Quiet (no output)

Made with <3 by HYOUG

```

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
- [ ] Detailed usage help

📜 License
============
[MIT](https://choosealicense.com/licenses/mit/) (2021) License protected project.
