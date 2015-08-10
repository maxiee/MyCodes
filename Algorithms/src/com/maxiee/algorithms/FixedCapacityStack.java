package com.maxiee.algorithms;

import java.util.Iterator;

/**
 * Created by maxiee on 15-7-7.
 */
public class FixedCapacityStack<Item> implements Iterable<Item>{
    private Item[] a;
    private int N;

    public FixedCapacityStack(int cap) {
        // a = new Item[cap]; this is disallowed
        a = (Item[]) new Object[cap];
    }

    public boolean isEmpty() {return N==0;}

    public int size() {return N;}

    public void push(Item item) {
        if (N == a.length) {
            System.out.println("堆栈满, 进行扩展...");
            resize(2*a.length);
        }
        a[N++] = item;
    }

    public Item pop() {
        Item item = a[--N];
        a[N] = null; // avoid loitering
        // 当当前容量为a总长度1/4时将a缩小一半
        if (N>0 && N==a.length/4) resize(a.length/2);
        return item;
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

    private void resize(int max) {
        Item[] temp = (Item[]) new Object[max];
        for (int i=0; i<N; i++) {
            temp[i] = a[i];
        }
        a = temp;
    }

    @Override
    public Iterator<Item> iterator() {
        return new ReverseArrayIterator();
    }

    private class ReverseArrayIterator implements Iterator<Item> {

        private int i = N;

        @Override
        public boolean hasNext() {
            return i>0;
        }

        @Override
        public Item next() {
            return a[--i];
        }

        @Override
        public void remove() {

        }

    }

    public static void main(String[] args) {
        FixedCapacityStack<String> s;
        s = new FixedCapacityStack<>(1);
        String text = "to be or not to - be - - that - - - is";
        String[] split = text.split("\\s+");
        for (String word: split) {
            if(!word.equals("-")) {
                s.push(word);
                for (String j: s) {
                    System.out.println(j);
                }
            } else if (!s.isEmpty()) {
                s.pop();
                System.out.println(s.toString());
            }
        }
    }
}
