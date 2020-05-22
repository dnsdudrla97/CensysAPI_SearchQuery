import argparse
# ArgumentParser() - 인자값을 받을 수 있는 인스턴스를 생성한다. (parser)
parser = argparse.ArgumentParser(description='심플')
# add_argument() - --name을 통해 입력받을 인자값을 등록한다.
parser.add_argument('--name', help='이름을 입력해주세요')
# parse_args() - 입력받은 인작값을 data에 저장 
data = parser.parse_args()
# data 변수에서 name 값을 호출하게 되면 인자값을 문자열 상태로 받아 온다.
name = data.name
# 출력
print("Hello, {}".format(name))

