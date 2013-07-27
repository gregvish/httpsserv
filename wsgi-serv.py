#!/usr/bin/python
import web
from ClientCert import gen, reg

urls = (
    '/', 'index',
    '/gen', 'gen',
    '/reg', 'reg',
)
app = web.application(urls, globals())

class index(object):        
    def GET(self):
        return 'Hello! %s %s %s' % (web.ctx.env['REMOTE_ADDR'], 
                                    web.ctx.env['VERIFIED'],
                                    web.ctx.env['DN'])

def main():
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

if __name__ == "__main__":
    main()
