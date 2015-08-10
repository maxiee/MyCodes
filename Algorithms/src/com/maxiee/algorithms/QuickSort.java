package com.maxiee.algorithms;

/**
 * Created by maxiee on 15-7-21.
 */
public class QuickSort {
    //    public static void qsort(int[] a, int low, int high) {
    //    private static int partition(int[] a, int low, int high) {

    public static void qsort(int[] a, int low, int high) {
        if (low<high) {
            int pivot = partition(a, low, high);
            qsort(a, 0, pivot - 1);
            qsort(a, pivot + 1, high);
        }
    }

    private static int partition(int[] a, int low, int high) {
        int pivot = a[low];
        while (low < high) {
            while (low<high && a[high] >= pivot) high--;
            a[low] = a[high];
            while (low<high && a[low] <= pivot) low++;
            a[high] = a[low];
        }
        a[low] = pivot;
        return low;
    }

    public static void main(String[] argcs) {
        int a[] = {49,38,65,97,76,13,27,49,78,34,12,64,5,4,62,99,98,54,56,17,18,23,34,15,35,25,53,51};
        qsort(a, 0, a.length - 1);
        System.out.println("排序结果：");
        for (Integer i : a) {
            System.out.print(i);
            System.out.print(" ");
        }
    }
}

