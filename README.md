# pyhton-soap-client-pkcs12
## Libraries to install
    pip install requests
    pip install zeep
    pip install zeep[xmlsec]
    pip install cryptography
## Hack
    Python39\Lib\site-packages\zeep\wsse\signature.py:239
    from: security.insert(0, signature)
    to: security.insert(1, signature)