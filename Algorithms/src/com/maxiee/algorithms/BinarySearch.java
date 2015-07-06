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

    private final static String TINY_T = "/home/maxiee/Code/algorithmsResources/tinyT.txt";
    private final static String TINY_W = "/home/maxiee/Code/algorithmsResources/tinyW.txt";

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
            int[] tinyW = fileToIntArray(TINY_W);
            int[] tinyT = fileToIntArray(TINY_T);
            System.out.println("数组排序...");
            Arrays.sort(tinyT);
            System.out.println("开始二值查找...");
            for (int value: tinyW) {
                int result = rank(value, tinyT);
                System.out.println("当前值:" + String.valueOf(value) + ", 位于:" + String.valueOf(result));
            }
        } catch (IOException e) {e.printStackTrace();}
    }

}
