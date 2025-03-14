# Python-GitHub-Runner
This is a tool to run [Python3](https://www.python.org) (specifically [Python3](https://www.python.org)) projects from GitHub.

## How it works
This is a CLI (Command Prompt Interface) tool, which means it should be run from your preferred terminal, whether it be kitty, Alacritty, Windows Terminal, etc.  

To actually run this tool, you need to use the following command:  
```
python3 ghr.py {repository-owner}/{repository-name}/{repository-branch} {script-to-run}
```
Of course, you need to replace the curly brackets according to what's written in them. For example, you can try to run [my reaction speed test](https://github.com/PabloMyDarling/Reaction-Speed-Test) like this:
```
python3 ghr.py PabloMyDarling/Reaction-Speed-Test/main main.py
```
A simple breakdown of this command:  
  - **python3 ghr.py:** runs the script with [Python3](https://www.python.org). (yes, you need Python for this to work)
  - **PabloMyDarling/Reaction-Speed-Test/main:**
    - **PabloMyDarling:** the repository owner
    - **Reaction-Speed-Test:** the repository name
    - **main:** the repository branch to run
  - **main.py:** the file to run from the repository

## How to install
If you'd like to use this tool for yourself, you can do the following steps:  

1. Click on the ***Code*** button to show a menu.  
![Code Button](docs-assets/code-button.png)    
2. A menu should come up, click ***Download ZIP***.  
 
![Download ZIP](docs-assets/download-zip.png)  
3. Then, you'll receive a ZIP file. Extract it, and start using the script!  

***Planning on making this tool cross language...***
