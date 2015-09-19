__author__ = 'maxiee'
import Sort.utils as utils


class Base:
    data = []

    def __init__(self, data):
        self.data = data

    def sort(self):
        pass

    def less(self, i, j):
        # print("===========")
        # print(self.data[i])
        # print(self.data[j])
        # print(self.data[i] < self.data[j])
        # print("===========")
        return self.data[i] < self.data[j]

    def exch(self, i, j):
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp

    def show(self):
        print(self.data)

    def is_sorted(self):
        for i in range(len(self.data)-1):
            if self.less(self.data[i], self.data[i+1]):
                return False
        return True


class SelectSort(Base):
    def sort(self):
        N = len(self.data)
        for i in range(N):
            min = i
            for j in range(i+1, N):
                if self.less(j, min):
                    min = j
            self.exch(i, min)
        return self.data


class InsertSort(Base):
    def sort(self):
        N = len(self.data)
        for i in range(N):
            for j in range (i, 0, -1):
                if not self.less(j, j-1):
                    break
                self.exch(j, j-1)
        return self.data

if __name__ == "__main__":
    l = utils.gen_string_list(20)
    print('原数组为: ', l)
    selectSort = SelectSort(l)
    print('选择排序后:', selectSort.sort())
    insetSort = InsertSort(l)
    print('插入排序后:', insetSort.sort())