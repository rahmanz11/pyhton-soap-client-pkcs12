from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from OpenSSL import crypto

user = "520825"
password = "COHd6zaIf*08"

session = Session()
cert_file = 'certificate.pfx'
# p12 = crypto.load_pkcs12(open("/path/to/cert.p12", 'rb').read(), password)
pkcs12 = crypto.load_pkcs12(open(cert_file, 'rb').read(), password)
cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())

with open(cert_file, 'wb') as f:
    f.write(cert)    
with open('key.pem', 'wb') as f:
    f.write(key)

session.cert = (cert_file, 'key.pem')

# signature = Signature(cert_file, cert_file)
session.auth = HTTPBasicAuth(user, password)
client = Client('https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl',
            transport=Transport(session=session)) #, wsse=[signature]

request_data = {
    'codigoInformacion': '1855',
    'motivoConsulta': '24',
    'numeroIdentificacion': '37685317',
    'tipoIdentificacion': '1'
}

request_parameter = {
    'parametrosConsulta': request_data
}

print(client.service.consultaXml(**request_parameter))