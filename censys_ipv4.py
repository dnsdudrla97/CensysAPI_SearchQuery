import sys
import censys.ipv4
try:
    c = censys.ipv4.CensysIPv4(api_id="9f6b9bf9-7c15-46f9-b0c5-714d7cffa1de", api_secret="Us73Ab0yCMHO8iXZ1b8zRoODJ11QL8V5")

    
    # report("쿼리문", field, 버킷 수)
    report = c.report(""" "welcome to" AND tags.raw: "http" """, field="80.http.get.headers.server.raw", buckets=5)
    print(report)


    # the view method lets you see the full JSON for an IP address
    # c.view('8.8.8.8')

    # the search method lets you search the index using indexed fields, full text, and 
    # combined predicates
    # for result in c.search("80.http.get.headers.server: Apache AND location.country: Korea", max_records=5):
    #     print (result)

    # # you can optionally specify which fields you want to come back for search results
    # IPV4_FIELDS = ['ip',
    #         'updated_at',
    #         '80.http.get.title',
    #         '443.https.get.title',
    #         '443.https.tls.certificate.parsed.subject_dn',
    #         '443.https.tls.certificate.parsed.names',
    #         '443.https.tls.certificate.parsed.subject.common_name',
    #         '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
    #         '25.smtp.starttls.tls.certificate.parsed.names',
    #         '25.smtp.starttls.tls.certificate.parsed.subject_dn',
    #         '110.pop3.starttls.tls.certificate.parsed.names',
    #         '110.pop3.starttls.tls.certificate.parsed.subject_dn']

    # data = list(c.search("80.http.get.headers.server: Apache AND location.country: Korea", 
    #                             IPV4_FIELDS, max_records=5))		 
    # print (data)
except censys.base.CensysUnauthorizedException:
    sys.stderr.write('[+] Censys account details wrong. \n')
    exit(1)

except censys.base.CensysRateLimitExceededException:
    sys.stderr.write('[+] Limit exceeded.')
    exit(1)

except censys.ipv4.CensysException:
    sys.stderr.write('[+] CensysException.')
    exit(1)
    

    