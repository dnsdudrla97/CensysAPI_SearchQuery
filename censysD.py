import sys
import requests
import censys.certificates

# API 
AID = "API"
SECRET = "SECRET"

# API Certificates
certificates = censys.certificates.CensysCertificates(AID, SECRET)

# search Query
fields = ["parsed.subject_dn", "parsed.fingerprint_sha256", "parsed.fingerprint_sha1"]

# search function 
for c in certificates.search("validation.nss.valid: true", fields=fields):
    print(c["parsed.subject_dn"])