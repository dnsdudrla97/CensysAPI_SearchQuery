# hello/main.py
# argparse 모듈 임포트
import argparse


def hello(name):
    print("Hello, {}".format(name))


def main():
    parser = argparse.ArgumentParser()
    # name argument 추가
    parser.add_argument('name')
    args = parser.parse_args()

    name = args.name
    hello(name)


if __name__ == "__main__":
    main()