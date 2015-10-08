__author__ = 'maxiee'
import Sort.utils as utils

class Base:
    data = []
    aux = []

    def __init__(self, data):
        self.data = data

    def sort(self):
        pass

    def less(self, i, j):
        return self.data[i] < self.data[j]

    def more(self, i, j):
        return self.data[i] > self.data[j]

    def exch(self, i, j):
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp

    def show(self):
        print(self.data)

    def is_sorted(self):
        for I in range(len(self.data) - 1):
            if self.less(I + 1, I):
                return False
        return True

#选择排序
class SelectSort(Base):
    def sort(self):
        #填写算法
        return self.data

#插入排序
class InsertSort(Base):
    def sort(self):
        #填写算法
        return self.data

#希尔排序
class Shell(Base):
    def sort(self):
        #填写算法
        return self.data

#归并排序
class Merge(Base):
    def __init__(self, data):
        super().__init__(data)
        self.aux = list(data)

    def sort(self):
        self.sort_sub(0, len(self.data) - 1)
        return self.data

    #递归排序
    def sort_sub(self, lo, hi):
        #填写算法
        pass

    #归并方法
    def merge(self, lo, mid, hi):
        #填写算法
        pass

#快排
class Quick(Base):
    def sort(self):
        self.sort_sub(0, len(self.data) -1)
        return self.data

    #递归排序
    def sort_sub(self, lo, hi):
        #填写算法
        if hi <= lo:
            return
        j = self.partition(lo, hi)
        self.sort_sub(lo, j-1)
        self.sort_sub(j+1, hi)

    #分区
    def partition(self, lo, hi):
        #填写算法
        i = lo
        j = hi + 1
        v = self.data[lo]
        while True:
            i += 1
            while self.data[i] < v:
                i += 1
                if i == hi:
                    break
            j -= 1
            while self.data[j] > v:
                j -= 1
                if j == lo:
                    break
            if i >= j:
                break
            self.exch(i, j)
        self.exch(lo, j)
        return j


def sort_and_test(name, cls, l):
    c = cls(list(l))
    c.sort()
    print(name, c.is_sorted())

if __name__ == "__main__":
    length = 1000
    l = utils.gen_string_list(length)
    # sort_and_test("选择排序", SelectSort, l)
    # sort_and_test("插入排序", InsertSort, l)
    # sort_and_test("希尔排序", Shell, l)
    # sort_and_test("自顶向下归并", Merge, l)
    sort_and_test("快速排序", Quick, l)