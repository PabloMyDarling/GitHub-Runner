from requests import get, RequestException
from sys import argv, platform
from colorama import Fore, Style
from os import mkdir, chdir, path, makedirs
from urllib.parse import urlparse, unquote
from runpy import run_path
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler
from webbrowser import open_new_tab
from shutil import rmtree
from keyboard import add_hotkey

def get_files(username: str, reponame: str, put_path: str = "", branch: str = "main", URL: str = ""):
    file_urls = []
    folder_names = []
    url = URL or f"https://api.github.com/repos/{username}/{reponame}/contents{put_path}?ref={branch}"

    try:
        response = get(url)
        response.raise_for_status()
        contents = response.json()
    except RequestException as e:
        print(f"{Fore.RED}ERROR:{Fore.RESET} {e}")
        return
    
    for item in contents:
        if item['type'] == 'file' and item['name'] != 'README.md': file_urls.append(item['download_url'])
        else: folder_names.append(item['path'])

    local_dir = path.join(files_dirname, put_path)
    makedirs(local_dir, exist_ok=True)

    for file_url in file_urls:
        filename = unquote(urlparse(file_url).path.split("/")[-1])
        local_path = path.join(local_dir, filename)

        print(f"{Fore.CYAN}Getting{Fore.RESET} {Fore.YELLOW}'{file_url}'{Fore.RESET}...")
        try:
            with open(local_path, "wb") as file: file.write(get(file_url).content)
            print(f"{Fore.GREEN}Received!{Fore.RESET}")
        except OSError as e:
            print(f"{Fore.RED}Error writing file '{filename}': {e}{Fore.RESET}")

    for folder_path in folder_names:
        folder_name = path.relpath(folder_path, start=put_path)
        print(f"{Fore.MAGENTA}Working on directory:{Fore.RESET} {folder_name}")

        get_files(username, reponame, folder_path, branch,
                  f"https://api.github.com/repos/{username}/{reponame}/contents/{folder_path}?ref={branch}")

files_dirname = ""
ghr_path = path.join(path.expanduser("~"), "Documents", "ghr")

def MAIN():
    global files_dirname, ghr_path, lang
    try:
        try:
            lang = argv[1]
            repo = argv[2].split("/", 3)
            if lang != "html-css-js" and lang != "ghr": main_file = argv[3]
        except IndexError:
            print(f"{Style.BRIGHT}{Fore.RED}ERROR:{Fore.RESET}{Style.RESET_ALL} not enough arguments")
            exit()

        if argv[1] == "ghr" and argv[2] == "setup":
            print("\033c", end="")
            print(f"{Fore.BLUE}Creating{Fore.RESET} {Fore.YELLOW}'ghr'{Fore.BLUE} in {Fore.YELLOW}Documents{Fore.RESET}...")
            try: mkdir(ghr_path)
            except FileExistsError: print(f"{Fore.CYAN}The ghr folder has already been created!{Fore.RESET}")
            print(f"{Fore.GREEN}Done!{Fore.RESET}")
            exit()

        if lang == "html-css-js":
            try:
                argv[3]
                print(f"{Fore.YELLOW}{Style.BRIGHT}WARN:{Fore.RESET}{Style.BRIGHT} main file not required for html-css-js")
            except IndexError: pass
        response = get(f"https://api.github.com/repos/{repo[0]}/{repo[1]}/contents?ref={repo[2]}")

        if not response.status_code == 200:
            print(f"{Style.BRIGHT}{Fore.RED}ERROR:{Fore.RESET}{Style.RESET_ALL} failed to reach repo")
            exit()

        try:
            if platform == "linux" or platform == "linux2" or platform == "darwin":
                mkdir(path.join(ghr_path, ".files")); files_dirname = path.join(ghr_path, ".files")
            else:
                mkdir(path.join(ghr_path, "files"))
                from win32api import SetFileAttributes
                SetFileAttributes(path.join(ghr_path, "files"), 2)
                files_dirname = path.join(ghr_path, "files")
        except FileExistsError:
            if platform == "linux" or platform == "linux2" or platform == "darwin": files_dirname = path.join(ghr_path, ".files")
            else: files_dirname = path.join(ghr_path, "files")

        assert files_dirname != "", "ERROR: files_dirname is empty!"
        get_files(repo[0], repo[1], branch=repo[2])
        print("\033c")
        if lang != "html-css-js": print(f"{Fore.GREEN}Receiving successful! The following output will be according to your code.{Fore.RESET}")
        else: print(f"{Fore.GREEN}Receiving successful! You can press <Ctrl-Alt-C> anywhere to abort the process.{Fore.RESET}")
        print(f"{Fore.BLUE}-------------------------------------------------------------------------------{Fore.RESET}")

        chdir(files_dirname)
        if lang == "python3":
            print(f"main_file path: {main_file}")
            run_path(path.join(files_dirname, main_file))
        elif lang == "html-css-js":
            with TCPServer(("", 0), SimpleHTTPRequestHandler) as httpd:
                chdir(files_dirname)
                open_new_tab(f"http://localhost:{httpd.server_address[1]}")
                add_hotkey("ctrl+alt+x", httpd.shutdown)
                httpd.serve_forever()
        chdir(path.dirname(__file__))
        rmtree(files_dirname)
    except KeyboardInterrupt:
        print(f"\033c{Fore.RED}{Style.BRIGHT}Aborted.{Fore.RESET}{Style.NORMAL}")
        chdir( path.dirname(files_dirname) )
        rmtree(files_dirname)

if __name__ == "__main__": MAIN()

