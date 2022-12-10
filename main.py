import os
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature


wsdl_url = 'https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl'
user = "520825"
password = "COHd6zaIf*08"

pfx_cert = 'D:\\utilities\\caoh91\\Certificados\\certificate.pfx'
pfx_password = "namtrik".encode('utf8')# b'namtrik'

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend

class CustomSignature(object):
    """Sign given SOAP envelope with WSSE sig using given key and cert."""
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
        for wsse in self.wsse_list:
            envelope, headers = wsse.apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):
        pass


with open(pfx_cert, "rb") as f:
    private_key, certificate = pkcs12.load_key_and_certificates(f.read(), pfx_password, default_backend())[:2]
    
    print(certificate.not_valid_after)

    session = Session()

    # cert_bytes = certificate.public_bytes(Encoding.DER)
    # pk_bytes = private_key.private_bytes(Encoding.DER, PrivateFormat.TraditionalOpenSSL, NoEncryption())
    
    pk = "certs/private.pem"
    cert = "certs/public.pem"
    try:
        os.mkdir("certs")
    except FileExistsError:
        pass
    with open(cert, "wb") as f:
        f.write(certificate.public_bytes(encoding=Encoding.PEM))

    with open(pk, "wb") as f:
        f.write(private_key.private_bytes(encoding=Encoding.PEM,
                                          format=PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=NoEncryption()))
                                          
    signature = Signature(pk, cert)

    session.auth = HTTPBasicAuth(user, password)
    transport = Transport(session=session)
    client = Client(wsdl_url, transport=transport, wsse=CustomSignature([signature]))

    request_data = {
        'codigoInformacion': '1855',
        'motivoConsulta': '24',
        'numeroIdentificacion': '37685317',
        'tipoIdentificacion': '1',
        'primerApellido': None
    }

    request_parameter = {
        'parametrosConsulta': request_data
    }

    import xml.etree.ElementTree as ET
    from zeep.exceptions import Fault

    response = client.service.consultaXml(**request_parameter)
    try:
        root = ET.fromstring(response.text)
        error_text = next(root.iter("faultstring")).text
    except:
        error_text = "" 

    if error_text:
        raise Fault(error_text)