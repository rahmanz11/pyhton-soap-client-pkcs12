# pyhton-soap-client

## Libraries to install
    pip install requests
    pip install zeep
    pip install zeep[xmlsec]
    pip install cryptography
    pip install python-dotenv

## Hack
    Python39\Lib\site-packages\zeep\wsse\signature.py:239
    from: security.insert(0, signature)
    to: security.insert(1, signature)

## Configuration
    .env file contains all necessary configuration
    resources folder contains all necessary files

## Input
    input data are available inside the project directory from resources/input.json

## Run
    From the project directory, execute the following command:
    python main.py

## Output
    output will be saved in output.xml in the project directory