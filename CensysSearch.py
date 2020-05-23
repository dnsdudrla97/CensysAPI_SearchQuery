from censys.ipv4 import *
from censys.base import *
import pickle
import argparse
import sys
import os

# help 설명문
help_desc = '''
Censys API를 활용한 OSINT툴 개발 - 보안 프로젝트 -
-- @dnsdudrla97
'''

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
def make_query(query):
	if len(query.arguments) == 0:
		q = '*'		
	else:
		q = "(" + query.arguments[0] + ")"
	if query.tags:
		if ',' in query.tags:
			tags_split = query.tags.split(',')
			tags_q = " AND tags:" + " AND tags:".join(tags_split)
		else:
			tags_q = " AND tags: %s" % query.tags
		q += tags_q
		print(q)
	if query.asn:
		q += " AND autonomous_system.asn: %s" % query.asn
	if query.country:
		q += " AND location.country_code:%s" % query.country
	if query.http_server:
		q += " AND 80.http.get.headers.server:%s" % query.http_server	
	if query.html_title:
		if " " in query.html_title:
			title = "\"%s\"" % query.html_title
		else:
			title = query.html_title
		q += " AND 80.http.get.title:%s" % title	
	if query.html_body:
		if " " in query.html_body:
			body = "\"%s\"" % query.html_body
		else:
			body = query.html_body
		q += " AND 80.http.get.body:%s" % body
	return q

# res, ipv4 기반의 일반 정보를 검색 -> dict 형태
def SearchPrint(query):
	max_title_len = 50
	title_head = 'Title: '
	cut = '[...]'
	http_title = query.get('80.http.get.title', 'N/A')
	as_name = query.get('autonomous_system.name', 'N/A')
	as_num = query.get('autonomous_system.asn', '')
	location = '{} / {}'.format(query.get('location.country_code',
                                   'N/A'), query.get('location.city', 'N/A'))
	os = query.get('metadata.os', 'N/A')
	tags = query.get('tags', '')
	ip = query.get('ip', 'N/A')

	# 문자열 변경 '\n' -> '\\n'
	http_title = http_title.replace('\n', '\\n')
	http_title = http_title.replace('\r', '\\r')

    # 타이틀이 길 경우 길이 제한
	if len(http_title) > (max_title_len-len(title_head)-1):
		http_title = str(http_title[:max_title_len-len(title_head)-len(cut)-1]) + cut

	print(ip.ljust(16) +
			((title_head + '%s') % http_title).ljust(max_title_len) +
			('AS: %s (%s)' % (as_name, as_num)).ljust(40) +
			('Loc: %s' % location).ljust(30) +
			('OS: %s' % os).ljust(15) +
			('Tags: %s' % tags))

# API 설정 - 환경 변수 파일 생성
def censys_api(api_key):
	conf_file = "%s/.censys_API.p" % os.environ.get('HOME')
	api = dict()

    # 인자가 있을 경우 해당 환경 변수 파일 생성 및 저장
	if api_key.api_id and api_key.api_secret:
		api['id'] = api_key.api_id
		api['secret'] = api_key.api_secret
		pickle.dump(api, open(conf_file, "wb"))
		return api
	
    # conf_file 존재할시 로드
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

    # 환경 변수 파일에 API가 존재 하지 않을시 저장 후 반환
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
	api = censys_api(args)
	# print(api)

	# API 인증을 진행 합니다.
	Censys_Auth = CensysIPv4(api_id=api['id'], api_secret=api['secret'])
	# 인자를 받아와 분류 후 쿼리문을 만듭니다.
	Query_string = make_query(args)
    
	# 정리한 쿼리를 바탕으로 search 함수를 사용하여 검색을 진행합니다. (필터 리스트 를 사용하여 찾고자 하는 정보를 분산시킵니다.)
	result = Censys_Auth.search(Query_string, fields=filter_fields)
	for entity in result:
		SearchPrint(entity)
