from requests import get
from sys import argv
from colorama import Fore, Style
from os import mkdir, chdir, remove, path, rmdir
from urllib.parse import urlparse
from win32api import SetFileAttributes
from runpy import run_path

try:
    repo = argv[1].split("/", 3)
    main_file = argv[2]
except IndexError:
   print(f"{Style.BRIGHT}{Fore.RED}ERROR:{Fore.RESET}{Style.RESET_ALL} not enough arguments")
   exit() 

response = get(f"https://api.github.com/repos/{repo[0]}/{repo[1]}/contents?ref={repo[2]}")

if not response.status_code == 200:
    print(f"{Style.BRIGHT}{Fore.RED}ERROR:{Fore.RESET}{Style.RESET_ALL} failed to reach repo")
    exit()

content = response.json()
file_urls = []
for item in content:
    if item['type'] == 'file': file_urls.append(item['download_url'])

try:
    mkdir("files")
    SetFileAttributes( path.join(path.dirname(__file__), "files"), 2 )
except FileExistsError: pass
files = []
for file_url in file_urls:
    with open( path.join(path.dirname(__file__), "files", urlparse(file_url).path.split("/")[-1]), "wb" ) as file:
        file.write( get(file_url).content )
        files.append(file.name)

chdir( path.join(path.dirname(__file__), "files") )
run_path(main_file)
chdir( path.dirname(__file__) )
for file in files: remove(file)
rmdir(path.join(path.dirname(__file__), "files"))

