package com.maxiee.algorithms;

import java.util.Arrays;

/**
 * Created by maxiee on 15-7-7.
 */
public class FixedCapacityStackOfStrings {
    private String[] a;
    private int N;

    public FixedCapacityStackOfStrings(int cap) {
        a = new String[cap];
    }

    public boolean isEmpty() {return N == 0;}

    public int size() {return N;}

    public void push(String item) {
        a[N++] = item;
    }

    public String pop() {
        return a[--N];
    }

    @Override
    public String toString() {
        String ret = "";
        ret += "a=[";
        for (int i=0; i<N; i++) {
            ret += String.valueOf(a[i]) + ",";
        }
        ret += "]";
        return ret;
    }

    public static void main(String[] args) {
        FixedCapacityStackOfStrings s;
        s = new FixedCapacityStackOfStrings(100);
        String text = "to be or not to - be - - that - - - is";
        String[] split = text.split("\\s+");
        for (String word: split) {
            if(!word.equals("-")) {
                s.push(word);
            } else if (!s.isEmpty()) {
                s.pop();
                System.out.println(s.toString());
            }
        }
    }
}
