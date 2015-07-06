package com.maxiee.algorithms;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by maxiee on 15-7-6.
 */
public class BinarySearchBigSet {

    private final static String LARGE_T = "/home/maxiee/Code/algorithmsResources/largeT.txt";
    private final static String LARGE_W = "/home/maxiee/Code/algorithmsResources/largeW.txt";

    public static int rank(int key, int[] a) {
        int lo = 0;
        int hi = a.length - 1;
        while (lo <= hi) {
            System.out.print(".");
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
            int value = Integer.valueOf(line.trim());
            ret.add(value);
        }
        System.out.println("转为数组...");
        System.out.println("共有元素:" + String.valueOf(ret.size()));
        int[] retArray = new int[ret.size()];
        for (int i=0; i<ret.size(); i++) {
            retArray[i] = ret.get(i);
        }
        return retArray;
    }

    public static void main(String[] args) {
        try {
            int[] largeW = fileToIntArray(LARGE_W);
            int[] laegeT = fileToIntArray(LARGE_T);
            System.out.println("数组排序...");
            long startTime = System.currentTimeMillis();
            Arrays.sort(laegeT);
            long endTime = System.currentTimeMillis();
            System.out.println("排序用时:" + String.valueOf((endTime-startTime) / 1000.0f));
            System.out.println("开始二值查找...");
            for (int value: largeW) {
                startTime = System.currentTimeMillis();
                int result = rank(value, laegeT);
                endTime = System.currentTimeMillis();
                System.out.println(
                    "当前值:" + String.valueOf(value) +
                    ", 位于:" + String.valueOf(result) +
                    "用时:" + String.valueOf(endTime - startTime)
                );
            }
        } catch (IOException e) {e.printStackTrace();}
    }

}
