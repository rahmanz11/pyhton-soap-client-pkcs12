import os
from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import xsd, Client, Settings
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from zeep.plugins import HistoryPlugin
from lxml import etree
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from zeep.wsse import utils
from datetime import datetime, timedelta
from zeep.wsse.utils import WSU
from zeep.wsse.signature import Signature

wsdl_url = 'InformacionComercialWS.wsdl' #https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl
user = "520825"
password = "COHd6zaIf*08"

pfx_cert = 'certificate.pfx'
pfx_password = 'namtrik'

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
    history = HistoryPlugin()

    pk = "certs/private.pem"
    cert = "certs/public.pem"
    try:
        os.mkdir("certs")
    except FileExistsError:
        pass
    with open(cert, "wb") as f:
        f.write(certificate.public_bytes(encoding=Encoding.PEM))
        f.close()

    with open(pk, "wb") as f:
        f.write(private_key.private_bytes(encoding=Encoding.PEM,
                                          format=PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=NoEncryption()))
        f.close()
    
    signature = SignatureTimestamp(pk, cert, pfx_password)
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client(wsdl_url, transport=transport, wsse=signature, plugins=[history], settings=settings)    
    client.set_ns_prefix("inf", "http://infocomercial.cifin.asobancaria.com")
    client.set_ns_prefix("dto", "http://dto.infocomercial.cifin.asobancaria.com")
    client.set_ns_prefix("xsd", "http://www.w3.org/2001/XMLSchema")
    client.set_ns_prefix("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    client.set_ns_prefix('soapenc', 'http://schemas.xmlsoap.org/soap/encoding/')

    dto_factory = client.type_factory('dto')
    parameters = dto_factory.ParametrosConsultaDTO(codigoInformacion='1855', motivoConsulta='24', numeroIdentificacion='37685317', tipoIdentificacion='1')

    with client.settings(raw_response=True): 
        response = client.service.consultaXml(parametrosConsulta = parameters)
    print (response.text)

    for hist in [history.last_sent, history.last_received]:
        print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=False))