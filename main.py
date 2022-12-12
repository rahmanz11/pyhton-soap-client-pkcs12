import json
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from zeep.wsse import utils
from datetime import datetime, timedelta
from zeep.wsse.utils import WSU
from zeep.wsse.signature import Signature

wsdl_url = 'https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl'
user = "***"
password = "****"

pfx_cert = 'certificate.pfx'
pfx_password = '****'

class SignatureTimestamp(Signature):
    
    def apply(self, envelope, headers):

        security = utils.get_security_header(envelope)
        
        created = datetime.utcnow()
        expired = created + timedelta(seconds=180 * 60)

        timestamp_token = WSU.Timestamp()

        timestamp_elements = [
            WSU.Created(created.strftime("%Y-%m-%dT%H:%M:%SZ")), 
            WSU.Expires(expired.strftime("%Y-%m-%dT%H:%M:%SZ"))
            ]
        
        timestamp_token.extend(timestamp_elements)
        
        security.append(timestamp_token)

        super().apply(envelope, headers)

        return envelope, headers

    def verify(self, envelope):
        pass

with open(pfx_cert, "rb") as f:

    private_key, certificate = pkcs12.load_key_and_certificates(f.read(), pfx_password.encode('utf8'), default_backend())[:2]
    
    session = Session()
    session.auth = HTTPBasicAuth(user, password)
    transport = Transport(session=session)

    pk = "private.pem"
    cert = "public.pem"

    with open(cert, "wb") as f:
        f.write(certificate.public_bytes(encoding=Encoding.PEM))
        f.close()

    with open(pk, "wb") as f:
        f.write(private_key.private_bytes(encoding=Encoding.PEM,
                                          format=PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=NoEncryption()))
        f.close()

    signature = SignatureTimestamp(pk, cert, pfx_password)
    client = Client(wsdl_url, transport=transport, wsse=signature)
    
    request_file = open('input.json')
    request_data = json.load(request_file)
    request_file.close()
    with client.settings(raw_response=True):
        response = client.service.consultaXml(**request_data)
        with open("output.xml", "w") as f:
            f.write(response.text)