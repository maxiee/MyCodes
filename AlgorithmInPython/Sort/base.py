__author__ = 'maxiee'
import Sort.utils as utils
import timeit


class Base:
    data = []
    aux = []

    def __init__(self, data):
        self.data = data

    def sort(self):
        pass

    def merge(self, lo, mid, hi):
        i = lo
        j = mid + 1
        # for k in range(lo, hi + 1):
        #     self.aux[k] = self.data[k]
        self.aux = list(self.data)
        for k in range(lo, hi + 1):
            if i > mid:
                self.data[k] = self.aux[j]
                j += 1
            elif j > hi:
                self.data[k] = self.aux[i]
                i += 1
            elif self.aux[j] < self.aux[i]:
                self.data[k] = self.aux[j]
                j += 1
            else:
                self.data[k] = self.aux[i]
                i += 1

    def less(self, i, j):
        # print("===========")
        # print(self.data[i])
        # print(self.data[j])
        # print(self.data[i] < self.data[j])
        # print("===========")
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


class SelectSort(Base):
    def sort(self):
        N = len(self.data)
        for i in range(N):
            min = i
            for j in range(i + 1, N):
                if self.less(j, min):
                    min = j
            self.exch(i, min)
        return self.data


class InsertSort(Base):
    def sort(self):
        N = len(self.data)
        for i in range(N):
            for j in range(i, 0, -1):  #j 最小只到1
                if self.more(j, j - 1):
                    break
                self.exch(j, j - 1)
        return self.data


class Shell(Base):
    def sort(self):
        N = len(self.data)
        h = 1
        while h < int(N / 3):
            h = 3 * h + 1
        while h >= 1:
            for i in range(h, N):
                for j in range(i, h - 1, -h):
                    if not self.less(j, j - h):
                        break
                    self.exch(j, j - h)
            h = int(h / 3)
        return self.data

class Merge(Base):
    def __init__(self, data):
        super().__init__(data)
        self.aux = list(data)

    def sort(self):
        self.sort_sub(0, len(self.data) - 1)
        return self.data

    def sort_sub(self, lo, hi):
        if hi <= lo:
            return
        mid = lo + int ((hi - lo) / 2)
        self.sort_sub(lo, mid)
        self.sort_sub(mid + 1, hi)
        self.merge(lo, mid, hi)

class Quick(Base):
    def sort(self):
        self.sort_sub(0, len(self.data) -1)
        return self.data

    def sort_sub(self, lo, hi):
        if hi <= lo:
            return
        j = self.partition(lo, hi)
        self.sort_sub(lo, j-1)
        self.sort_sub(j+1, hi)

    def partition(self, lo, hi):
        i = lo
        j = hi + 1
        v = lo
        while True:
            i += 1
            while self.less(i, v):
                i += 1
                if i == hi:
                    break
            j -= 1
            while self.more(j, v):
                j -= 1
                if j == lo:
                    break
            if i >= j:
                break
            self.exch(i, j)
        self.exch(lo, j)
        return j


if __name__ == "__main__":
    for i in range(1):
        length = 1000
        # 创建对象
        l = utils.gen_string_list(length)
        s = SelectSort(list(l))
        n = InsertSort(list(l))
        shell = Shell(list(l))
        m = Merge(list(l))
        q = Quick(list(l))
        # 创建定时器
        t1 = timeit.Timer('s.sort()', "from __main__ import s, l")
        t2 = timeit.Timer('n.sort()', "from __main__ import n, l")
        t3 = timeit.Timer('shell.sort()', "from __main__ import shell, l")
        t4 = timeit.Timer('m.sort()', "from __main__ import m, l")
        t5 = timeit.Timer('q.sort()', "from __main__ import q, l")
        print("=========第%d轮==========" % i)
        print("随机数组长度为 %d" % length)
        print("选择排序时间:" + str(t1.timeit(1)), ",排序正确:" + str(s.is_sorted()))
        print("插入排序时间:" + str(t2.timeit(1)), ",排序正确:" + str(n.is_sorted()))
        print("希尔排序时间:" + str(t3.timeit(1)), ",排序正确:" + str(shell.is_sorted()))
        print("自顶向下归并:" + str(t4.timeit(1)), ",排序正确:" + str(m.is_sorted()))
        print("快速排序事件:" + str(t5.timeit(1)), ",排序正确:" + str(q.is_sorted()))
        print("-------------------------")
