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
pfx_password = b'namtrik'

from cryptography.hazmat.primitives.serialization import pkcs12

from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
with open(pfx_cert, "rb") as f:
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), pfx_password)
    
    print(certificate.not_valid_after)

    session = Session()

    try:
        os.mkdir("certs")
    except FileExistsError:
        pass
    with open("certs/public.pem", "wb") as f:
        f.write(certificate.public_bytes(encoding=Encoding.PEM))

    with open("certs/private.pem", "wb") as f:
        f.write(private_key.private_bytes(encoding=Encoding.PEM,
                                          format=PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=NoEncryption()))
                                          
    signature = Signature("certs/private.pem", "certs/public.pem")

    session.auth = HTTPBasicAuth(user, password)
    transport = Transport(session=session)
    client = Client(wsdl_url, transport=transport, wsse=[signature])

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