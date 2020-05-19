import censys.ipv4
import argparse


API = "API"
SECRET = "SECRET"
c = censys.ipv4.CensysIPv4(api_id=API, api_secret=SECRET)

# Report method Query
# c.report(""" "welcome to" AND tags.raw: "http" """, field="80.http.get.headers.server.raw", buckets=5)


# View method IP ALLL -> JSON FIlE
# ip = c.view('8.8.8.8')
# print(type(ip))


# search method -> Index filed, all text, combine
# for result in c.search("80.http.get.headers.server: Apache AND location.country: Japan", max_records=10):
#     print(result)

# custome filed
IPV4_FIELDS = ['ip',
		 'updated_at',
		 '80.http.get.title',
		 '443.https.get.title',
		 '443.https.tls.certificate.parsed.subject_dn',
		 '443.https.tls.certificate.parsed.names',
		 '443.https.tls.certificate.parsed.subject.common_name',
		 '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
		 '25.smtp.starttls.tls.certificate.parsed.names',
		 '25.smtp.starttls.tls.certificate.parsed.subject_dn',
		 '110.pop3.starttls.tls.certificate.parsed.names',
		 '110.pop3.starttls.tls.certificate.parsed.subject_dn']




def searchQuery(server, country, maxrecords):
	queryOptions(server, country, maxrecords)
	data = list(c.search(f"80.http.get.headers.server: {server} AND location.country: {country}", IPV4_FIELDS, max_records=maxrecords))
	queryFilter(data)

def queryOptions(server, country, maxrecords):
	print("server: {}".format(server))
	print("country: {}".format(country))
	print("maxrecords {}".format(maxrecords))
	print(f"80.http.get.headers.server:{server} AND location.country:{country} max_records={maxrecords}")

def queryFilter(data):
	print("{:<15}{:^30}{:>30}".format('IP', 'UPDATE', 'TITLE'))
	for d in data:
		print("{ip:<30} {update:^30}".format(ip=d['ip'], update=d['updated_at']))
		# print(f'{ip:10} ==> {update:10}')





def main():
	parser = argparse.ArgumentParser()
    # name argument 추가
	parser.add_argument('server')
	parser.add_argument('country')
	parser.add_argument('maxrecords', type=int)
	args = parser.parse_args()

	searchQuery(server = args.server,
		country = args.country,
		maxrecords = args.maxrecords
	)

	# queryOptions(server, country, maxrecords)


if __name__ == "__main__":
    main()
