# Devops task #

Python3 script that gets a GIT repo, compiles it and pushes binaries to a GIT repo or sends an error email.

### Use
```
pip install virtualenv
```
```
virtualenv venv -p /usr/bin/python3
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python make.py build --config config.json
```

### Config (JSON)
```
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "alexisfloresortega@gmail.com",
    "password": "********",
    "email_from": "alexisfloresortega@gmail.com",
    "email_to": "alexisfloresortega@gmail.com",
    "subject": "SCRIPT ERROR"
  },
  "git_origin": {
    "git_repo": "https://github.com/alexiscata/git_task",
    "git_user": "alexiscata",
    "git_pass": "********",
    "repo_path": "./repository",    
    "build_file": "./build.sh"
  },
  "git_target": {
    "git_target": "https://{}:{}@github.com/alexisCata/target_task",
    "target_path": "./target_repository",
    "files": ["HelloWorld.class", "ByeWorld.class"]
  },
  "last_execution": null
}
```

### Help
```shell
python make.py build -h
```
```shell
python make.py -h
```

### Dependencies
    
[GitPython](https://github.com/gitpython-developers/GitPython)
    
[clinner](https://github.com/PeRDy/clinner)