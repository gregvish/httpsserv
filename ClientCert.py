import web
import base64
import subprocess
from tempfile import NamedTemporaryFile

urls = (
    '/gen', 'gen',
    '/reg', 'reg',
)
app = web.application(urls, globals())

FORM = '''
<html>
<body>
    <form action="/reg">
        <keygen name="pubkey" challenge="test1234">
        <input type="text" name="name" value="test1">
        <input type="submit" name="createcert" value="Generate">
    </form>
</body>
</html>
'''

SPKAC_TEMPLATE = '''SPKAC=%s
CN=%s
emailAddress=test@test.com
0.OU=Company client certificate
organizationName=Company
countryName=US
stateOrProvinceName=State
localityName=US
'''

CA_DIR = '../nobodycerts/trustedca'
OPENSSL = '/usr/bin/openssl'
OPENSSL_CA_SIGN_TEMPLATE = 'ca -config ./openssl.cnf -days 365 -batch -spkac %s -out %s'

class gen(object):        
    def GET(self):
        web.header('Content-Type', 'text/html')
        return FORM

class reg(object):        
    def GET(self):
        pubkey = str(web.input()['pubkey']).decode('base64')
        name = str(web.input()['name'])
        spkac = SPKAC_TEMPLATE % (base64.b64encode(pubkey), name)
        spkac_file = NamedTemporaryFile()
        spkac_file.write(spkac)
        spkac_file.flush()
        openssl_args = OPENSSL_CA_SIGN_TEMPLATE % (spkac_file.name, spkac_file.name + '.s')
        subprocess.check_output([OPENSSL] + openssl_args.split(' '), 
                                cwd = CA_DIR,
                                stderr = subprocess.STDOUT)
        cert = open(spkac_file.name + '.s', 'rb').read()
        web.header('Accept-Ranges', 'bytes')
        web.header('Content-Type', 'application/x-x509-user-cert')
        web.header('Content-Length', str(len(cert)))
        return cert

