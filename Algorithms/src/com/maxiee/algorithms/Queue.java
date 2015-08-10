package com.maxiee.algorithms;

/**
 * Created by maxiee on 15-7-7.
 */
public class Queue<Item>
{
    private Node first;
    private Node last;
    private int N;

    private class Node
    {
        Item item;
        Node next;
    }

    public boolean isEmpty() {return first == null;}

    public int size() {return N;}

    public void enqueue(Item item)
    {
        Node oldlast = last;
        last = new Node();
        last.item = item;
        last.next = null;
        if (isEmpty()) first = last;
        else oldlast.next = last;
        N++;
    }

    public Item dequeue()
    {
        Item item = first.item;
        first = first.next;
        // 若仅剩 1 个 Node, first 和 last 都指向它
        // first 通过 next 变成 null 了, 可 last 还指向它
        // 因此需要手动 null
        if (isEmpty()) last=null;
        N--;
        return item;
    }

    @Override
    public String toString() {
        if (first == null) return "";
        Node node = first;
        String result = "data=[";
        do {
            result += node.item.toString() + ", ";
            node = node.next;
        } while (node != null);
        result += "]";
        return result;
    }

    public static void main(String[] argcs)
    {
        Queue<String> queue = new Queue<>();
        for (int i=1; i<10; i++) {
            if (i%3 == 0) {
                queue.dequeue();
            } else {
                queue.enqueue(String.valueOf(i));
            }
            System.out.println(queue.toString());
        }
    }
}
