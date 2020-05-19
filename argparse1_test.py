import argparse

# 1. argparse object create
# parser = argparse.ArgumentParser()

# 2. add_argument() string -> object
# parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (dafault: find the max)')
# parser.add_argument('domain', metavar='Domain')

# parse
# print(parser.parse_args(['--sum', '7', '-1', '42', "www.google.com"]))
# args = parser.parse_args()
# print(args)

def hello(data):
    print("Hello, {}".format(data))


def main():
    parser = argparse.ArgumentParser()
    # name argument 추가
    parser.add_argument('data')
    args = parser.parse_args()
    
    data = args.data
    hello(data)


if __name__ == "__main__":
    main()