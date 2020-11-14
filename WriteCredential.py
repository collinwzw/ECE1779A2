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
aws_access_key_id=ASIAUYP7WLAHKWHXNWD6
aws_secret_access_key=9i8b4W+5sz2CGA1jvlD+pBkyi2hIlcJy4K9Q+tm6
aws_session_token=FwoGZXIvYXdzEDsaDBLR5+RCh6utPiOsYSLIAZXUWpIRjuEEcpJFw0UWcUui8UK3u1E4xSld6F1N1yqXe0BtrzHS/KYs4KEaDAwaNsGIgkoMBD+gdGIty42f/PnNv6wwSeSb0uzxpce6RScWo+CJmU9asMmXwOpfki3AnXHUFzkugrM3G+qIyMBMYAGubzevKltnhogmljSzGngjAF7O4dU1vlC7FhTLITeUBmULx6oQBAm84t9Sr3EOoNTNxjtPXkP7fphSvvB++0FTakfJj13uagOwd0CgUieqgrXAY/P9WnKxKK25sP0FMi0jREfmJnXiG4154iANBoY7lP9Uin5oUHnYPCsK4QGYZjjQDE+JLFB+DEBacug=


    filetowrite.write(myCredential)
    
    
    
