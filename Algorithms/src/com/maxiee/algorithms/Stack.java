package com.maxiee.algorithms;

import java.util.Iterator;

/**
 * Created by maxiee on 15-7-7.
 */
public class Stack<Item> implements Iterable<Item>
{
    private Node first;
    private int N;

    private class Node
    {
        Item item;
        Node next;
    }

    public boolean isEmpty() {return first==null;}

    public int size() {return N;}

    public void push(Item item) {
        Node oldFirst = first;
        first = new Node();
        first.item = item;
        first.next = oldFirst;
        N++;
    }

    public Item pop() {
        Item item = first.item;
        first = first.next;
        N--;
        return item;
    }

    @Override
    public Iterator<Item> iterator() {
        return new ReverseIterator();
    }

    private class ReverseIterator implements Iterator<Item>{

        private Node nodeIter = first;

        @Override
        public boolean hasNext() {
            return nodeIter.next != null;
        }

        @Override
        public Item next() {
            Item ret = nodeIter.item;
            nodeIter = nodeIter.next;
            return ret;
        }

        @Override
        public void remove() {

        }
    }

    public static void main(String[] args) {
        Stack<String> s;
        s = new Stack<>();
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
