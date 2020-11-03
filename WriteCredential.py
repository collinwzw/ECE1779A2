### Copy your Credentials here and run this file 

file='./.aws/credentials'
with open(file, 'w') as filetowrite:
    myCredential = """[default]
aws_access_key_id=ASIAUYP7WLAHGHFE2BXZ
aws_secret_access_key=aaEY6b2qJet69FTOeciVAvbjQ4KMi9g022AKoqnl
aws_session_token=FwoGZXIvYXdzEGEaDCla5PyckD9TI5dMDiLIAa+WwT80ffsvy78+LhACpcmOgLoK88f+SLBgOFvSLnY75MIOzFpi/m6c+gPPEMxxqgcHwXlPxnE7rKI7b/6Dpwc4OWVY7czSOB7VU7y07Kd3o4hkE3XGCUcRXeCUwtkcVQ0kl900DNY+gYk8bwQqrp5Orco2Yj4tUE4EUh8qeNc/2g9Q+uTmYqf5Kil6y1ehAIDQdIPX3c6m5uCHY4z9VWRQLu0xWwCVGvohA3KasNV8GHmiBG2ttIk8Avtvtg76IrOU8Q3kDQiAKOjIgP0FMi2MdEs3vKLRqe1cIdAAA9m2UIyJEdn0wcA6CKviPD9cgV+ZEsnrbPHz3GaLIvc=
    
    """

    filetowrite.write(myCredential)
    
    
    
    
#### Write in some default settings, don't change anything here 
file='./.aws/config'
with open(file, 'w') as filetowrite:
    myCredential = """[default]
                      region = us-east-1
                      output = json
                      [profile prod]
                      region = us-east-1
                      output = json"""
    filetowrite.write(myCredential)
    
