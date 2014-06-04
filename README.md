Daily Feed Push
===============

Convert feed to mobi and push to your email/kindle daily.


Requirements
------------
Bash

Python

Calibre


Usage
-----
* Manully convert feed to mobi and send email

```./run.sh```

* Setup crontab

```./set_crontab.sh  # Modify this file to set the when and how often the cronjob should run```


Configs
-------
mail.conf: SMTP server config

recipes.txt: List of calibre recipes

recipients.txt: Email recipients

.recipe files: Calibre recipes

