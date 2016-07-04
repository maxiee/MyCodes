package com.maxiee.algorithms;

/**
 * Created by maxiee on 16/7/4.
 */
public class SelectSort {

    public static void exch(int[] a, int b, int c) {
        int tmp = a[b];
        a[b] = a[c];
        a[c] = tmp;
    }

    public static void sort(int[] a, int low, int high) {
        for (int i = low; i < high; i++) {
            int min = i;
            for (int j = i +1 ; j <= high; j++) {
                if (a[j] < a[min]) min = j;
            }
//            System.out.print(String.format("i=%d, min=%d\n", i, min));
            exch(a, i, min);
        }
    }

    public static void main(String[] argcs) {
        int a[] = {49,38,65,97,76,13,27,49,78,34,12,64,5,4,62,99,98,54,56,17,18,23,34,15,35,25,53,51};
        sort(a, 0, a.length - 1);
        System.out.println("排序结果：");
        for (int i : a) {
            System.out.print(i);
            System.out.print(" ");
        }
    }
}
