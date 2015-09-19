__author__ = 'maxiee'


def readInts():
    nums = []
    while True:
        try:
            line = input()
            nums.append(int(line))
        except EOFError as err:
            break
    return nums


if __name__ == "__main__":
    print(readInts())
