from requests import get
from sys import argv, platform
from colorama import Fore, Style
from os import mkdir, listdir, chdir, remove, path, rmdir
from urllib.parse import urlparse, unquote
from runpy import run_path

# file functions
def rm(Path: str):
    if path.isdir(Path):
        for item in listdir(Path): rm( path.join(Path, item) )
        rmdir(Path)
        return
    remove(Path)

import os
import requests
from urllib.parse import unquote, urlparse
from colorama import Fore

def get_files(username: str, reponame: str, put_path: str = "", branch: str = "main", URL: str = ""):
    file_urls = []
    folder_names = []
    url = URL or f"https://api.github.com/repos/{username}/{reponame}/contents{put_path}?ref={branch}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        contents = response.json()
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching repository contents: {e}{Fore.RESET}")
        return
    
    for item in contents:
        if item['type'] == 'file':
            file_urls.append(item['download_url'])
        else:
            folder_names.append(item['path'])

    local_dir = os.path.join(os.path.dirname(__file__), files_dirname, put_path)
    os.makedirs(local_dir, exist_ok=True)

    for file_url in file_urls:
        filename = unquote(urlparse(file_url).path.split("/")[-1])
        local_path = os.path.join(local_dir, filename)

        print(f"{Fore.CYAN}Getting{Fore.RESET} {Fore.YELLOW}'{file_url}'{Fore.RESET}...")
        try:
            with open(local_path, "wb") as file:
                file.write(requests.get(file_url).content)
            print(f"{Fore.GREEN}Received: {filename}{Fore.RESET}")
        except OSError as e:
            print(f"{Fore.RED}Error writing file {filename}: {e}{Fore.RESET}")

    for folder_path in folder_names:
        folder_name = os.path.relpath(folder_path, start=put_path)
        print(f"{Fore.MAGENTA}Working on directory:{Fore.RESET} {folder_name}")

        get_files(username, reponame, folder_path, branch,
                  f"https://api.github.com/repos/{username}/{reponame}/contents/{folder_path}?ref={branch}")

#script
files_dirname = ""

try:
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

    try:
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            mkdir(".files"); files_dirname = ".files"
        else:
            mkdir("files")
            from win32api import SetFileAttributes
            SetFileAttributes( path.join(path.dirname(__file__), "files"), 2 )
            files_dirname = "files"
    except FileExistsError:
        if platform == "linux" or platform == "linux2" or platform == "darwin": files_dirname = ".files"
        else: files_dirname = "files"

    get_files(repo[0], repo[1], branch=repo[2])
    print("\033c")
    print(f"{Fore.GREEN}Receiving successful! The following output will be accoring to your code.{Fore.RESET}")
    print(f"{Fore.BLUE}-------------------------------------------------------------------------------{Fore.RESET}")

    chdir( path.join(path.dirname(__file__), files_dirname) )
    run_path(main_file)
    chdir( path.dirname(__file__) )
    rm( path.join(path.dirname(__file__), files_dirname) )
except KeyboardInterrupt:
    print(f"{Fore.RED}{Style.BRIGHT}Aborted.{Fore.RESET}{Style.NORMAL}")
    rm( path.join(path.dirname(__file__), files_dirname) )
except Exception as e:
    print(f"{Fore.RED}{Style.BRIGHT}ERROR: {Fore.RESET}{Style.NORMAL}{e}")
    rm( path.join(path.dirname(__file__), files_dirname) )

