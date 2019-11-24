# Nanny Salary

## Prerequisite
Python versions covered:
* `Python 3.6`
* `Python 3.7`

## Prepare
```
pipenv update
```

## Runtime
```
pipenv run python main.js
```

### Systemd service
```
[Unit]
Description=Nanny API Service
After=multi-user.target

[Service]
User=root
WorkingDirectory=/opt/python/nanny-api
Restart=always
Type=simple
ExecStart=/usr/local/bin/pipenv run python main.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
