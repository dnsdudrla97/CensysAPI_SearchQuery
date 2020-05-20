from censys.ipv4 import *
from censys.base import *
import pickle
import argparse
import time
import sys
import os

# 필터링 데이터 구조
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

# 인자를 바탕으로 쿼리문을 제작합니다. 
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
	if args.html_body:
		if " " in args.html_body:
			body = "\"%s\"" % args.html_body
		else:
			body = args.html_body
		s += " AND 80.http.get.body:%s" % body
	return s

# res, ipv4 기반의 일반 정보를 검색 -> dict 형태
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

	http_title = http_title.replace('\n', '\\n')
	http_title = http_title.replace('\r', '\\r')

    # 타이틀이 길 경우 길이 제한
	if len(http_title) > (max_title_len-len(title_head)-1):
		http_title = str(http_title[:max_title_len-len(title_head)-len(cut)-1]) + cut

	print(ip.ljust(16) +
			((title_head + '%s') % http_title).ljust(max_title_len) +
			('AS: %s (%s)' % (as_name, as_num)).ljust(40) +
			('Loc: %s' % loc).ljust(30) +
			('OS: %s' % os).ljust(15) +
			('Tags: %s' % tags))

# help 설명문
help_desc = '''
Censys API를 활용한 OSINT
-- Younsle
'''

# API 설정 - 환경 변수 파일 생성
def conf_get_censys_api(args):
	conf_file = "%s/.censys_API.p" % os.environ.get('HOME')
	api = dict()

    # 인자가 있을 경우 해당 환경 변수 파일 생성 및 저장
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
			print ("피클 파일이 손상되었습니다.")
			sys.exit(-1)
		if not api.get('id') or not api.get('secret'):
			print ("피크 파일 구조가 불일치 합니다.")
			sys.exit(-2)
		return api

    # 환경 변수가 존재 하지 않을시 저장
	if 'CENSYS_API_ID' in os.environ and 'CENSYS_API_SECRET' in os.environ:
		api['id'] = os.environ.get('CENSYS_API_ID')
		api['secret'] = os.environ.get('CENSYS_API_SECRET')
		pickle.dump(api, open(conf_file, "wb"))
		return api

# 해당 소스가 현재 main 에서 동작하는지
if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=help_desc, formatter_class=argparse.RawTextHelpFormatter)

	# 단순 검색 인자 
	parser.add_argument('-a', '--asn', default=None,
	                    help='기관이,단체가 독립적으로 운영하는 네트워크 라우터를 입력해 주세요')
	parser.add_argument('-c', '--country', default=None,
	                    help='국가 코드를 입력해 주세요')
	parser.add_argument('-S', '--http-server', default=None, help='서버 <header> 정보를 입력해 주세요')
	parser.add_argument('-t', '--html-title', default=None,
	                    help='웹 페이지 <title> 정보를 입력해 주세요')
	parser.add_argument('-b', '--html-body', default=None,
	                    help='웹 페이지 <body> 정보를 입력해 주세요')
	parser.add_argument('-T', '--tags', default=None,
	                    help='검색 하고자 하는 tag를 입력해 주세요 (-T tag1,tag2,... ) (키워드 사용시 \'list\' 사용해야 정확히 나옵니다.')

	parser.add_argument('--api_id', default=None,
	                    help='환경변수로 정의 하지 않을시 입력해 주세요 (API_ID)')
	parser.add_argument('--api_secret', default=None,
	                    help='환경변수로 정의 하지 않을시 입력해 주세요 (API_SECRET)')
	parser.add_argument('arguments', metavar='arguments',
	                    nargs='*', help='쿼리 나열')
	args = parser.parse_args()

	# API 키, 비밀키를 처리 합니다.
	api = conf_get_censys_api(args)
	# print(api)

	# API 인증을 진행 합니다.
	q = CensysIPv4(api_id=api['id'], api_secret=api['secret'])
	# 인자를 받아와 분류 후 쿼리문을 만듭니다.
	s = build_query_string(args)
	
	# 정리한 쿼리를 바탕으로 search 함수를 사용하여 검색을 진행합니다. (필터 리스트 를 사용하여 찾고자 하는 정보를 분산시킵니다.)
	r = q.search(s, fields=filter_fields)
	for e in r:
		print_short(e)
