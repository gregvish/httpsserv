#/bin/bash
sudo kill `pgrep wsgi-serv` ; sleep 0.7 && sudo spawn-fcgi -u nobody -s /tmp/cgi_sock wsgi-serv.py
sudo kill `pgrep nginx` ; sudo /usr/local/nginx/sbin/nginx
