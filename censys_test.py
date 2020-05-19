import sys
import os
import time
import censys.certificates
import censys.ipv4
import censys

API = "API"
SECRET = "SECRET"

#finding the subdomains related to given domain
def subdomain_find(domain,censys_id,censys_secret):
    try:
        censys_cert = censys.certificates.CensysCertificates(api_id=censys_id,api_secret=censys_secret)
        cert_query = 'parsed.names: %s' % domain
        cert_search_results = censys_cert.search(cert_query, fields=['parsed.names'], page=1)
 
        subdomains = [] #List of subdomains
        for s in cert_search_results:
            subdomains.extend(s['parsed.names'])
 
        return set(subdomains) #removes duplicate values
    except censys.base.CensysUnauthorizedException:
        sys.stderr.write('[+] Censys account details wrong. \n')
        exit(1)
    except censys.base.CensysRateLimitExceededException:
        sys.stderr.write('[+] Limit exceeded.')
        exit(1)

subdomain_find("google.com", API, SECRET)