import ssl
from godaddypy import Client, Account

ssl._create_default_https_context = ssl._create_unverified_context

my_acct = Account(api_key='XXXX', api_secret='XXXX')
client = Client(my_acct)

domainList = [
    'XYZ.com', 
    'YQV.org'
]


# Example DKIM Generate
# openssl genrsa -out domain.pem 2048
# openssl rsa -in domain.pem -out domain.pub -pubout
# Read pub key from automatically and send to variable

def addNewRecord():
    for domain in domainList:
        # Default A Record
        defaultValue = 'X.X.X.X'
        req = client.add_record(domain, {'data': defaultValue, 'name': '@', 'ttl': 600, 'type': 'A'})
        print(req)

        # Mail A Record
        recordValue = 'X.X.X.X'
        req = client.add_record(domain, {'data': recordValue, 'name': 'mail', 'ttl': 600, 'type': 'A'})
        print(req)

        # SPF Record
        spfValue = 'v=spf1 a mx a:' + domain + ' ~all'
        req = client.add_record(domain, {'data': spfValue, 'name': 'spf1', 'ttl': 600, 'type': 'TXT'})
        print(req)

        # DMARC Record
        dmarcValue = 'v=DMARC1; p=reject; rua=mailto:admin@' + domain
        req = client.add_record(domain, {'data': dmarcValue, 'name': '_dmarc', 'ttl': 600, 'type': 'TXT'})
        print(req)

        #DKIM Record
        with open('/dkim_pub_key_path/' + domain + '.pub', 'r') as file:
            data = file.read().replace('\n', '')
            data = data.replace('-----BEGIN PUBLIC KEY-----', '')
            dkimValue = 'v=DKIM1; k=rsa; p=' + data.replace('-----END PUBLIC KEY-----', '')

        req = client.add_record(domain, {'data': dkimValue, 'name': 'dkim._domainkey', 'ttl': 600, 'type': 'TXT'})
        print(req)

        # STAR Record
        req = client.add_record(domain, {'data': '@', 'name': '*', 'ttl': 600, 'type': 'CNAME'})
        print(req)


addNewRecord()
