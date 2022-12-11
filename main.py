import os
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from zeep.plugins import HistoryPlugin
from lxml import etree
import xml.etree.ElementTree as ET
from zeep.exceptions import Fault
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from zeep.wsse import utils
from datetime import datetime, timedelta
from zeep.wsse.utils import WSU
from zeep.wsse.signature import BinarySignature

wsdl_url = 'https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl'
user = "520825"
password = "COHd6zaIf*08"

pfx_cert = 'certificate.pfx'
pfx_password = "namtrik".encode('utf8')# b'namtrik'

class BinarySignatureTimestamp(BinarySignature):
    
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
    private_key, certificate = pkcs12.load_key_and_certificates(f.read(), pfx_password, default_backend())[:2]
    
    print(certificate.not_valid_after)

    session = Session()

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
    history = HistoryPlugin()
    
    client = Client(wsdl_url, transport=transport, wsse=BinarySignatureTimestamp(pk, cert, str(pfx_password)), plugins=[history])
    client.settings.raw_response = True

    client.set_ns_prefix(None, "http://infocomercial.cifin.asobancaria.com")
    
    request_data = {
        'codigoInformacion': '1855',
        'motivoConsulta': '24',
        'numeroIdentificacion': '37685317',
        'tipoIdentificacion': '1'
    }

    request_parameter = {
        'parametrosConsulta': request_data
    }

    try:
        response = client.service.consultaXml(**request_parameter)
        for hist in [history.last_sent, history.last_received]:
            print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
        root = ET.fromstring(response.text)
        error_text = next(root.iter("faultstring")).text
    except Exception as e:
        error_text = str(e)

    if error_text:
        raise Fault(error_text)