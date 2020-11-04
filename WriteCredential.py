import boto3

client = boto3.client("sts")

response = client.get_session_token(
    DurationSeconds=36000,
    SerialNumber='string',
    TokenCode='string'
)


### Copy your Credentials here and run this file

file='/Users/qiweifu/.aws/credentials'
with open(file, 'w') as filetowrite:
    myCredential = """[default]
aws_access_key_id=ASIAUYP7WLAHMRFG65U2
aws_secret_access_key=6b9TnrhyN+v3c+DIOpHMxdwPpvWdAt+Vm2ADu4Xc
aws_session_token=FwoGZXIvYXdzEJD//////////wEaDBz2VmSt56EPhou2QCLIAeFHn1bkMAKIJtL17LpoxLlncQSqeXOTBYNB0fuxHj150/sSuAlSLvbOxq6kz6LsxA6W+0yOYMiHFxMdgClnDXOLxgBNOQjw7zB+dJBqFP3fjtogPgtwm6UjhcR4J/ke1UK4SGlwJcNoz1Ec9ZWSk2zDvkMpEBbk9D2cUFnE3AzVk0obFqcCj6zYBGxUrQ0Zd8F5w9mqZWRLd7u1U5QVPrSTHzavHmYZaAxzxyWR3gpFevxzdt/ctTuLdAqrnHEwPakNxg1CDQlUKJmEi/0FMi3vkUB9F9h/F4o29Kbqk32kgY2lnQILX5RSEpjPEGJpPXCTmyk30X6XDeR7VVM=
    """

    filetowrite.write(myCredential)
    
    
    
    
#### Write in some default settings, don't change anything here 
file='/Users/qiweifu/.aws/config'
with open(file, 'w') as filetowrite:
    myCredential = """[default]
                      region = us-east-1
                      output = json
                      [profile prod]
                      region = us-east-1
                      output = json"""
    filetowrite.write(myCredential)
    
