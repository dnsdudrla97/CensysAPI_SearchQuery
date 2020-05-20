import argparse
# 설명란
help_desc='''
Censys query via command line
-- Younsle
'''
#

# 인자 <- 인스턴스 생성
# formatter_clss = 설명란 포맷 형식
parse = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)

# 인자 입력
# parse.add_argument('--tag', required=True, help='지원 태그 POP3, SMTP, HTTP, HTTPS')
parse.add_argument('-t','--tags', default=None, help='지원 태그 POP3, SMTP, HTTP, HTTPS')
parse.add_argument('-s','--server', default=None, help='서버 모델 입력')
parse.add_argument('-mr','--max', type=int, help='최대 레코드 수를 지정할 수 있습니다.')
parse.add_argument('argument', metavar='argument', nargs='*', help='Censys query')

# 입력 -> 인자 args 저장
args = parse.parse_args()

# API 핸들 키/비밀키

print(args.tag)
print(args.server)
print(args.max)