package com.maxiee.algorithms;

import java.util.Iterator;

/**
 * Created by maxiee on 15-7-7.
 */
public class Bag<Item> implements Iterable<Item>
{
    private Node first;

    private class Node
    {

        Item item;
        Node next;
    }

    public void add(Item item)
    {
        Node oldfirst = first;
        first = new Node();
        first.item = item;
        first.next = oldfirst;
    }

    @Override
    public Iterator<Item> iterator() {
        return new ListIterator();
    }

    private class ListIterator implements Iterator<Item>
    {
        private Node current = first;

        @Override
        public boolean hasNext() {
            return current != null;
        }

        @Override
        public Item next() {
            Item item = current.item;
            current = current.next;
            return item;
        }

        @Override
        public void remove() {

        }
    }

}
