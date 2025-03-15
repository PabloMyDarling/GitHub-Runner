# GitHub-Runner
This is a tool to run [Python3](https://www.python.org) and HTML-CSS-JS projects directly from GitHub.

## How it works
This is a CLI (Command Line Interface) tool, which means it should be run from your preferred terminal, whether it be kitty, Alacritty, Windows Terminal, etc.  

To actually run this tool, you need to use the following command:  
```
python3 ghr.py {language} {repository-owner}/{repository-name}/{repository-branch} {script-to-run}
```
Of course, you need to replace the curly brackets according to what's written in them. For example, you can try to run [my reaction speed test](https://github.com/PabloMyDarling/Reaction-Speed-Test) like this:
```
python3 ghr.py python3 PabloMyDarling/Reaction-Speed-Test/main main.py
```

***Learn more about this tool in the [documentation](https://github.com/PabloMyDarling/GitHub-Runner/wiki)!***
