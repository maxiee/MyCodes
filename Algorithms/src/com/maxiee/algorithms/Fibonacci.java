package com.maxiee.algorithms;

import java.util.ArrayList;

/**
 * Created by maxiee on 15-7-6.
 */
public class Fibonacci {

    private static ArrayList<Double> fibCache = new ArrayList<>();

    public static double F(int N) {
        if (N <= fibCache.size() - 1) {
            return fibCache.get(N);
        }
        if (N == 0) return 0;
        if (N == 1) return 1;
        return F(N-1) + F(N-2);
    }

    public static void main(String[] args) {
        for (int N=0; N<200; N++) {
            double result = F(N);
            fibCache.add(result);
            System.out.println(String.valueOf(N) + " " + String.valueOf(result));
        }
    }
}
