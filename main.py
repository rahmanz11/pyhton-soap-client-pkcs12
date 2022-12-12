import json
import os
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
from dotenv import dotenv_values

# Load .env file
config = dotenv_values('.env')

wsdl_url = config['WSDL']
user = config['USER']
password = config['PASSWORD']
pfx_cert = config['CERTFILE']
pfx_password = config['CERTPASS']

pk = config['PRIVATEKEY']
cert = config['PUBLICKEY']

input = config['INPUT']
output = config['OUTPUT']

'''
This class will be used to sign the soap 
by the certificate and add the signature 
and timestamp to the security header
'''
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

# First open the certificate.pfx file
with open(pfx_cert, "rb") as f:
    # Extract the private key and public key from the certificate
    private_key, certificate = pkcs12.load_key_and_certificates(f.read(), pfx_password.encode('utf8'), default_backend())[:2]
    
    session = Session()
    session.auth = HTTPBasicAuth(user, password)
    transport = Transport(session=session)

    # Write the public key to the file
    with open(cert, "wb") as f:
        f.write(certificate.public_bytes(encoding=Encoding.PEM))
        f.close()

    # Write the private key to the file
    with open(pk, "wb") as f:
        f.write(private_key.private_bytes(encoding=Encoding.PEM,
                                          format=PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=NoEncryption()))
        f.close()

    # Sign the soap request with the keys extracted from the certificate
    signature = SignatureTimestamp(pk, cert, pfx_password)

    try:
        # Build the SOAP Client
        client = Client(wsdl_url, transport=transport, wsse=signature)
        
        # Open the input file
        request_file = open(input)
        # Load request data from input file
        request_data = json.load(request_file)
        request_file.close()
        
        # Consume the webservice
        with client.settings(raw_response=True):
            
            response = client.service.consultaXml(**request_data)
                
            # First remove the output file if it exists
            try:
                os.remove(output)
            except OSError:
                pass
            
            # Write the new output to the file
            with open(output, "w") as f:
                f.write(response.text)
    except Exception as e:
        print(e)