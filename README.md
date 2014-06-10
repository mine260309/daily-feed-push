#Daily Feed Push

Convert feed to mobi and push to your email/kindle daily.


##Requirements

##### Requirements for basic usage

- Bash
- Python
- Calibre

##### Requirements for webapp for subscriptions

- nginx
- python-paste
- uwsgi
- simplejson
- validate-email

##Usage

* Manully convert feed to mobi and send email

    ```
    ./run.sh
    ```

* Setup crontab

    ```
    ./set_crontab.sh  # Modify this file to set the when and how often the cronjob should run
    ```

* Setup webapp for subscriptions

    1. Setup nginx server, refer to `uwsgi-app/nginx.conf` for sample config;
    2. Start uwsgi backend manully:

        ```uwsgi --socket /tmp/daily-feed-push.sock --wsgi-file uwsgi-app/app.py --chmod-socket=666```

     or

        ```uwsgi uwsgi-app/uwsgi.ini```

    3. To manually add/delete subscriptions, just edit `config/recipients.txt`

##Configs

- mail.conf: SMTP server config
- recipes.txt: List of calibre recipes
- recipients.txt: Email recipients
- .recipe files: Calibre recipes

