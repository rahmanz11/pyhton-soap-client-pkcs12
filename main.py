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

wsdl_url = 'https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl'
user = "520825"
password = "COHd6zaIf*08"

pfx_cert = 'D:\\utilities\\caoh91\\Certificados\\certificate.pfx'
pfx_password = "namtrik".encode('utf8')# b'namtrik'

class BinarySignatureTimestamp(object):
    """Sign given SOAP envelope with WSSE sig using given key and cert."""
    def __init__(self, wsse_list):
        self.wsse_list = wsse_list

    def apply(self, envelope, headers):
    #     for wsse in self.wsse_list:
    #         envelope, headers = wsse.apply(envelope, headers)
    #     return envelope, headers
        security = utils.get_security_header(envelope)

        created = datetime.now()
        expired = created + timedelta(seconds=5 * 60)

        token = utils.WSSE.UsernameToken()
        token.extend([
            utils.WSSE.Nonce('43d74dda16a061874d9ff27f2b40e017'),
            utils.WSSE.Created(utils.get_timestamp(created)),
        ])

        timestamp = utils.WSU('Timestamp')
        timestamp.append(utils.WSU('Created', utils.get_timestamp(created)))
        timestamp.append(utils.WSU('Expires', utils.get_timestamp(expired)))

        security.append(timestamp)

        #  
        # headers['Content-Type'] = 'application/soap+xml;charset=UTF-8'

        # security = utils.get_security_header(envelope)

        # created = datetime.utcnow()
        # expired = created + timedelta(seconds=1 * 60)

        # timestamp = utils.WSU('Timestamp')
        # timestamp.append(utils.WSU('Created', created.replace(microsecond=0).isoformat()+'Z'))
        # timestamp.append(utils.WSU('Expires', expired.replace(microsecond=0).isoformat()+'Z'))

        # security.append(timestamp)

        # super().apply(envelope, headers)
        return envelope, headers
        
    # Override response verification and skip response verification for now...
    # Zeep does not supprt Signature verification with different certificate...
    # Ref. https://github.com/mvantellingen/python-zeep/pull/822/  "Add support for different signing and verification certificates #822"
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
    history = HistoryPlugin()
    client = Client(wsdl_url, transport=transport, wsse=BinarySignatureTimestamp([signature]), plugins=[history])
    client.settings.raw_response = True

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

    try:
        response = client.service.consultaXml(**request_parameter)
        root = ET.fromstring(response.text)
        error_text = next(root.iter("faultstring")).text
    except Exception as e:
        error_text = str(e)

    if error_text:
        raise Fault(error_text)
    
    for hist in [history.last_sent, history.last_received]:
        print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))