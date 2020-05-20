from censys.ipv4 import *
from censys.base import *
import pickle
import argparse
import time
import sys
import re
import os

# API = "API"
# SECRET = "SECRET"
# c = censys.ipv4.CensysIPv4(api_id=API, api_secret=SECRET)

# Report method Query
# c.report(""" "welcome to" AND tags.raw: "http" """, field="80.http.get.headers.server.raw", buckets=5)


# View method IP ALLL -> JSON FIlE
# ip = c.view('8.8.8.8')
# print(type(ip))


# search method -> Index filed, all text, combine
# for result in c.search("80.http.get.headers.server: Apache AND location.country: Japan", max_records=10):
#     print(result)

# custome filed 80, 443, 25, 110
# IPV4_FIELDS = ['ip',
# 		 'updated_at',
# 		 '80.http.get.title',
# 		 '443.https.get.title',
# 		 '443.https.tls.certificate.parsed.subject_dn',
# 		 '443.https.tls.certificate.parsed.names',
# 		 '443.https.tls.certificate.parsed.subject.common_name',
# 		 '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
# 		 '25.smtp.starttls.tls.certificate.parsed.names',
# 		 '25.smtp.starttls.tls.certificate.parsed.subject_dn',
# 		 '110.pop3.starttls.tls.certificate.parsed.names',
# 		 '110.pop3.starttls.tls.certificate.parsed.subject_dn']

filter_fields = ['location.country', 'location.country_code', 'location.city', 'ip',
                 'protocols', 'autonomous_system.name',
                 'autonomous_system.asn',
                 '443.https.tls.certificate.parsed.subject.organization',
                 '443.https.tls.certificate.parsed.subject.common_name',
                 '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names',
                 '993.imaps.tls.tls.certificate.parsed.subject.common_name',
                 '993.imaps.tls.tls.certificate.parsed.subject.organization',
                 '80.http.get.title',
                 '80.http.get.headers.server',
                 '80.http.get.body',
                 'metadata.os', 'tags']



# def searchQuery(server, country, maxrecords):
# 	queryOptions(server, country, maxrecords)
# 	data = list(c.search(f"80.http.get.headers.server: {server} AND location.country: {country}", IPV4_FIELDS, max_records=maxrecords))
# 	queryFilter(data)

# def queryOptions(server, country, maxrecords):
# 	print("server: {}".format(server))
# 	print("country: {}".format(country))
# 	print("maxrecords {}".format(maxrecords))
# 	print(f"80.http.get.headers.server:{server} AND location.country:{country} max_records={maxrecords}")

# def queryFilter(data):
# 	print("{:<15}{:^30}{:>30}".format('IP', 'UPDATE', 'TITLE'))
# 	for d in data:
# 		print("{ip:<30} {update:^30}".format(ip=d['ip'], update=d['updated_at']))
# 		# print(f'{ip:10} ==> {update:10}')
# query_string
def build_query_string(args):
	if len(args.arguments) == 0:
		s = '*'		
	else:
		s = "(" + args.arguments[0] + ")"
	if args.tags:
		if ',' in args.tags:
			tags_l = args.tags.split(',')
			tags_q = " AND tags:" + " AND tags:".join(tags_l)
		else:
			tags_q = " AND tags: %s" % args.tags
		s += tags_q
		# print(s)
	if args.asn:
		s += " AND autonomous_system.asn: %s" % args.asn
	if args.country:
		s += " AND location.country_code:%s" % args.country
	if args.http_server:
		s += " AND 80.http.get.headers.server:%s" % args.http_server
	
	if args.html_title:
		if " " in args.html_title:
			title = "\"%s\"" % args.html_title
		else:
			title = args.html_title
		s += " AND 80.http.get.title:%s" % title
	print(s)
	if args.html_body:
		if " " in args.html_body:
			body = "\"%s\"" % args.html_body
		else:
			body = args.html_body
		s += " AND 80.http.get.body:%s" % body
	return s

# res = complete dict from IPv4 search with generic info


def print_short(res):
	max_title_len = 50
	title_head = 'Title: '
	cut = '[...]'
	http_title = res.get('80.http.get.title', 'N/A')
	as_name = res.get('autonomous_system.name', 'N/A')
	as_num = res.get('autonomous_system.asn', '')
	loc = '{} / {}'.format(res.get('location.country_code',
                                   'N/A'), res.get('location.city', 'N/A'))
	os = res.get('metadata.os', 'N/A')
	tags = res.get('tags', '')
	ip = res.get('ip', 'N/A')


	# print(max_title_len, title_head, cut, http_title,
    #   as_name, as_num, loc, os, tags, ip)

	http_title = http_title.replace('\n', '\\n')
	http_title = http_title.replace('\r', '\\r')

    # do some destructive encoding to UTF-8
	# http_title = http_title.encode('UTF-8', errors='ignore')
	# tags = b', '.join([t.encode('UTF-8', errors='ignore') for t in tags])
	# as_name = as_name.encode('UTF-8', errors='ignore')
	# os = os.encode('UTF-8', errors='ignore')
	# loc = loc.decode('ASCII', errors='ignore')

    # shortun title if too long
	# print(len(http_title))
	# print(max_title_len-len(title_head)-len(cut)-1)
	if len(http_title) > (max_title_len-len(title_head)-1):
		http_title = str(http_title[:max_title_len-len(title_head)-len(cut)-1]) + cut

	print(ip.ljust(16) +
			((title_head + '%s') % http_title).ljust(max_title_len) +
			('AS: %s (%s)' % (as_name, as_num)).ljust(40) +
			('Loc: %s' % loc).ljust(30) +
			('OS: %s' % os).ljust(15) +
			('Tags: %s' % tags))



# def main():
# 	parser = argparse.ArgumentParser()
#     # name argument 추가
# 	parser.add_argument('server')
# 	parser.add_argument('country')
# 	parser.add_argument('maxrecords', type=int)
# 	args = parser.parse_args()

# 	searchQuery(server = args.server,
# 		country = args.country,
# 		maxrecords = args.maxrecords
# 	)

# 	# queryOptions(server, country, maxrecords)

help_desc = '''
Censys query via command line
-- Younsle
'''


def conf_get_censys_api(args):
	conf_file = "%s/.censys_API.p" % os.environ.get('HOME')
	api = dict()

    # command-line API key get precedence other methods
	if args.api_id and args.api_secret:
		api['id'] = args.api_id
		api['secret'] = args.api_secret
		pickle.dump(api, open(conf_file, "wb"))
		return api
	

    # if conf file exists, load it
	print(os.path.isfile(conf_file))
	
	with open(conf_file,"rb") as f:
		car_obj_2 = pickle.load(f)
	print(car_obj_2)
	
	if os.path.isfile(conf_file):
		try:
			api = pickle.load(open(conf_file, "rb"))
		except:
			print ("Pickle file corrupted.")
			sys.exit(-1)
		if not api.get('id') or not api.get('secret'):
			print ("Pickle file structure mismatch.")
			sys.exit(-2)
		return api

    # if environment variable exists, store it in file
	if 'CENSYS_API_ID' in os.environ and 'CENSYS_API_SECRET' in os.environ:
		api['id'] = os.environ.get('CENSYS_API_ID')
		api['secret'] = os.environ.get('CENSYS_API_SECRET')
		pickle.dump(api, open(conf_file, "wb"))
		return api


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=help_desc, formatter_class=argparse.RawTextHelpFormatter)

	# query filter shortcuts
	parser.add_argument('-a', '--asn', default=None,
	                    help='Filter with ASN (ex: 25408 for Westcall-SPB AS)')
	parser.add_argument('-c', '--country', default=None,
	                    help='Filter with country')
	parser.add_argument('-S', '--http-server', default=None, help='Server header')
	parser.add_argument('-t', '--html-title', default=None,
	                    help='Filter on html page title')
	parser.add_argument('-b', '--html-body', default=None,
	                    help='Filter on html body content')
	parser.add_argument('-T', '--tags', default=None,
	                    help='Filter on specific tags. E.g: -T tag1,tag2,... (use keyword \'list\' to list usual tags')

	parser.add_argument('--api_id', default=None,
	                    help='Censys API ID (optional if no env defined)')
	parser.add_argument('--api_secret', default=None,
	                    help='Censys API SECRET (optional if no env defined)')
	parser.add_argument('arguments', metavar='arguments',
	                    nargs='*', help='Censys query')
	args = parser.parse_args()

	# handle API key/secret
	api = conf_get_censys_api(args)
	# print(api)

	# build up query
	q = CensysIPv4(api_id=api['id'], api_secret=api['secret'])
	
	s = build_query_string(args)
	

	r = q.search(s, fields=filter_fields)
	for e in r:
		print_short(e)
