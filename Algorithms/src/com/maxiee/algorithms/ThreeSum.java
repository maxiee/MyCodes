package com.maxiee.algorithms;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by maxiee on 15-7-9.
 */
public class ThreeSum {

    private static final String FILE = "/home/maxiee/Code/algorithmsResources/4Kints.txt";

    public static int count(int[] a)
    {
        int N = a.length;
        int cnt = 0;
        for (int i=0; i<N; i++)
            for (int j=i+1; j<N; j++)
                for (int k=j+1; k<N; k++)
                    if(a[i] + a[j] + a[k] == 0) // N(N-1)(N-2)/6
                        cnt++;
        return cnt;
    }

    public static int countFast(int[] a)
    {
        Arrays.sort(a);
        int N = a.length;
        int cnt = 0;
        for (int i=0; i<N; i++)
            for (int j=i+1; j<N; j++)
                if (BinarySearch.rank(-a[i]-a[j], a) >j)
                    cnt++;
        return cnt;
    }

    private static int[] fileToIntArray(String path) throws IOException
    {
        FileReader fr = new FileReader(path);
        BufferedReader br = new BufferedReader(fr);
        String line = "";
        ArrayList<Integer> ret = new ArrayList<>();
        while((line = br.readLine()) != null) {
            int value = Integer.valueOf(line.trim());
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

    public static void main(String[] args)
    {
        try {
            int[] ints = fileToIntArray(FILE);
            long start = System.currentTimeMillis();
            int count = count(ints);
            long end = System.currentTimeMillis();
            System.out.println(count);
            System.out.println("耗时:" + String.valueOf((end - start) / 1000.0));
            start = System.currentTimeMillis();
            count = countFast(ints);
            end = System.currentTimeMillis();
            System.out.println(count);
            System.out.println("耗时:" + String.valueOf((end - start) / 1000.0));
        } catch (IOException e) {e.printStackTrace();}
    }
}
