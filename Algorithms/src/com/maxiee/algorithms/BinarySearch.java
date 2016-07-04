package com.maxiee.algorithms;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by maxiee on 15-7-6.
 */
public class BinarySearch {

    private final static String TINY_T = "./tinyT.txt";
    private final static String TINY_W = "./tinyW.txt";

    public static int rank_correct(int key, int[] a) {
        int lo = 0;
        int hi = a.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < key) { lo = mid + 1;}
            else if (a[mid] > key) {hi = mid - 1;}
            else return mid;
        }
        return -1;
    }

    private static int[] fileToIntArray(String path) throws IOException {
        FileReader fr = new FileReader(path);
        BufferedReader br = new BufferedReader(fr);
        String line = "";
        ArrayList<Integer> ret = new ArrayList<>();
        while((line = br.readLine()) != null) {
            int value = Integer.valueOf(line);
            ret.add(value);
        }
        System.out.println("转为数组...");
        System.out.println(ret.toString());
        int[] retArray = new int[ret.size()];
        for (int i=0; i<ret.size(); i++) {
            retArray[i] = ret.get(i);
        }
        return retArray;
    }

    public static void main(String[] args) {
        try {
            int[] tinyW = fileToIntArray(TINY_W); // 要寻找的数字
            int[] tinyT = fileToIntArray(TINY_T); // 从这个数组中搜索
            System.out.println("数组排序...");
            Arrays.sort(tinyT); // 二分查找必须先排序
            System.out.println("开始二值查找...");
            for (int value: tinyW) {
                int result = rank_correct(value, tinyT); // rank 就是二分查找的函数
                System.out.println("当前值:" + String.valueOf(value) + ", 正确位置位于:" + String.valueOf(result));
                result = rank_my(value, tinyT);
                System.out.println("当前值:" + String.valueOf(value) + ", 算法位置位于:" + String.valueOf(result));
            }
        } catch (IOException e) {e.printStackTrace();}
    }

    // 每次要练算法的时候, 就把这个函数清空, 重新编写.
    private static int rank_my(int k, int[] a) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] < k) lo = mid + 1;
            else if (a[mid] > k) hi = mid -1;
            else return mid;
        }
        return -1;
    }

}
