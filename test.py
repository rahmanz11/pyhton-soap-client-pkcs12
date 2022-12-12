import requests

url="https://miportafoliouat.transunion.co/InformacionComercialWS/services/InformacionComercial?wsdl"
# headers = {'content-type': 'application/soap+xml', 'Authorization': 'Basic NTIwODI1OkNPSGQ2emFJZiowOA=='}
headers = {'SOAPAction': '""', 'Content-Type': 'text/xml; charset=utf-8', 'Authorization': 'Basic NTIwODI1OkNPSGQ2emFJZiowOA=='}
body = """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:inf="http://infocomercial.cifin.asobancaria.com" xmlns:dto="http://dto.infocomercial.cifin.asobancaria.com" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"><soap-env:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"><wsu:Timestamp xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="id-92c199c6-91d1-44d4-b826-3b82f1d2bd94"><wsu:Created>2022-12-12T09:38:28Z</wsu:Created><wsu:Expires>2022-12-12T12:38:28Z</wsu:Expires></wsu:Timestamp><Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
<SignedInfo>
<CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
<Reference URI="#id-5fb538df-379e-4782-b20f-14d5a226ad1d">
<Transforms>
<Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
</Transforms>
<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<DigestValue>fthWis8BL3RgWE59gER3AHoe9Yo=</DigestValue>
</Reference>
<Reference URI="#id-92c199c6-91d1-44d4-b826-3b82f1d2bd94">
<Transforms>
<Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
</Transforms>
<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<DigestValue>JZ0vr+dHh+Mr0B7QSz7vtAoi1FA=</DigestValue>
</Reference>
</SignedInfo>
<SignatureValue>hBXdgDFiH/8UIQTYgltypy+avH6W8/7T5dR3U1jqj3gN6pKXgfO7HjWAxhi4yuvc
fSLr+8rtbOczce5+R8A2khMpo7JvG/BXh4zyFhyDUTVNR0CWhClK9F3aMh/xQ3RR
d+JCPjtWHgCIVGBfR147yAatBHuLDxuoTcjItt2fB/nKff6yFXEZ0eXUzh5JGZ4o
Xm0Z1MT7j5MM1S+ufj1czias7E9+gWB4IqCJ0z1C9BLExDgeiZjI5MSTqgVYKzbF
cXcmueRzEbyDzHnx6jSKG7OnIwn2dt9fk4H7gJVYU/U9a8pMbYG4V1swFNrv56hM
dQNX7RL8ECRdGFMUGOzBrMgfJdSMhPpuTVLmDEOEuZXTa0a0N5ln2m5pJdUL5CCW
StQL37iENIq4qK+ebFcpq9k9mCkOFjWVqcRFHrhcv3jyEukO2UNlpDeNHb3OA+2w
RqyWSynHryr9Pf1kWxANxurw8biTE5kdFRHBGPExvzX2IsrxVyw2qtKvyvhxZgTg
Ssv2nH4nFBzrmTn+b8YOkLwDdrRXvCPmXsJwT08NlNiBk1D3QfA9IfsUxJfg64Kk
DND5WwTH2lBRr9It31OCF7rQnRJ0Uf98sA0+MbgS20WUI26+oMaaUw2vH2EipBdJ
A4CzKf1v2wxyJ3D++CgybsoxMjzoiwJHk/aRtb+Dqk0=</SignatureValue>
<KeyInfo>
<wsse:SecurityTokenReference><X509Data>
<X509IssuerSerial>
<X509IssuerName>CN=*.crediscore.co</X509IssuerName>
<X509SerialNumber>701958465195975363928029716549400644846424809112</X509SerialNumber>
</X509IssuerSerial>
<X509Certificate>MIIFFTCCAv2gAwIBAgIUevTn/d/XbTqbj0M6Q93+sRYx3pgwDQYJKoZIhvcNAQEL
BQAwGjEYMBYGA1UEAwwPKi5jcmVkaXNjb3JlLmNvMB4XDTIyMDUxODE1NTAzMFoX
DTIzMDUxODE1NTAzMFowGjEYMBYGA1UEAwwPKi5jcmVkaXNjb3JlLmNvMIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzcXCy8j6k16n9z+LLl1Yyu8MwxCj
DuOrWES37HVyuXiD53uEZaOXQFevx+MxWwM409+cfhZdiCdXTxa6wLkGSVvEORym
3W14a8/kmbV968/RTNVqQ1J7lgz6nh/wjDS9VDgKyJtYUex0BHmOX0hIXw9FUwpX
NKlxcvdr29CRvrbOX1lInFPhuQdHz8H5xxDpqPBWGuPret3K8x4q1apMgINmrqDd
MaBaTqV0mKIIyuPrC1APIpkhzZR/Vvn3NWvjm+NFp6GNx5BdT8XS88lAHO/Kqqji
lCVR2lLKCZ7pJsD8fJnEU50+a9yKc2uD6yC9rQlL31JSX14xCmPBy7JXCrDnBvxD
Z2OOHl2AMa6vMgKnxI+w4WFlDQNc6dL7joRH8UXQSQL6euV8vsh8rp4xmuJAR8In
dYoOv+XJm79PqqMHXQF18Ws51Tl7WhAtwkqnblxNCRTZ2sdbyq75t8cVo5e61glq
sxS3DZnP0Ir4h696AtNQIJJSWskJv+ded/kMVgaL1vECPiPnW/Xf9JFEOeWjUYJe
d+G+9DG4hUGYjbkmeuFGry+KQbU3u4XRzq62glLRC1SB4UQy8DKJLECPmaXQwfQy
jVjfXHJf5Y4BXv6Bu2fs4vx//aCrMQzt+BLrq57RZgtvNzP/0VvIWlHVtOzoG6ZU
F7fghBlhD/Q+dv0CAwEAAaNTMFEwHQYDVR0OBBYEFCmqokNlUI6Av/54p1MCIC8n
fdDPMB8GA1UdIwQYMBaAFCmqokNlUI6Av/54p1MCIC8nfdDPMA8GA1UdEwEB/wQF
MAMBAf8wDQYJKoZIhvcNAQELBQADggIBAAmvik7/83QNuvT7t9Rik+WltBa//5BE
8jcEEMnehVI5/lbQE2hn34OZ2OtBJxXEWJ6aa71cJo43IDJ0o5uv9i1tBO40mZNj
JKunJg19/2q4szJuXuCs4vRSmS6nV20s/MM8dv4bHSJdSmxeEsU7NTsWNtQOgXlQ
WWCz1m+b6OzzxJTwOQLbizMosvAjCRdt1MSGhU8UPXpZeQRHRLdHs8WaSk0j/fza
qqiOx7xN2/1aeZ+gnfa1CPCTq6DYCNyrInPzaDR3sV4f96VDTkZLBWFgCyL7IDJw
yI2bhuiUCWRBMXhIwtxPr1BXUZ+RHaSJkhBxSSLjRY5AXf7e0PIYs9gIjVmC4DJV
dd0KrJpTEFTs9e8o2B+m+z4n8uLFnafefZMyzcfRaQxJGoIF8dJpL2lT//1XOiD3
He5alf6uiyeOBmUOXBiitx4Nou6LrPNjFFc3dwXMJZ3Lh8SN80Pf6N7H3mpQFqrj
HrVDcUrOR3cDjObs6dTDv8pGjyNZ0KWstkcNQFEMKaz1fnf1Llu0WUZ8gyYwTi0A
DbyBLFzqT1u6gbmgVcW5hDy7RRHVYNyoUWH8vmbIqsveLkwHo1aqQemjZ8EUyjcx
KEZr7bZO6OzU9/ar1YMErsHd+kM+s3EmCNOtXsiyaxtnhuQBp4iRbw4aXFTsRr//
s7Wv+dyRKX3i</X509Certificate>
</X509Data>
</wsse:SecurityTokenReference></KeyInfo>
</Signature></wsse:Security></soap-env:Header><soap-env:Body xmlns:ns0="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" ns0:Id="id-5fb538df-379e-4782-b20f-14d5a226ad1d"><inf:consultaXml><parametrosConsulta><codigoInformacion>1855</codigoInformacion><motivoConsulta>24</motivoConsulta><numeroIdentificacion>37685317</numeroIdentificacion><primerApellido xsi:nil="true"/><tipoIdentificacion>1</tipoIdentificacion></parametrosConsulta></inf:consultaXml></soap-env:Body></soap-env:Envelope>"""
response = requests.post(url,data=body,headers=headers)
print (response.content)