package com.maxiee.algorithms.UnionFind;

import com.maxiee.algorithms.utils.Reader;

import java.io.IOException;

public class UF
{
    private static final String tinyUF = "/Users/maxiee/MyCodes/Algorithms/tinyUF.txt";
    private static final String mediumUf = "/home/maxiee/MyCodes/Algorithms/src/com/maxiee/algorithms/UnionFind/mediumUF.txt";
    private int[] id;  // componet id
    private int count; // number of componets
    
    public UF(int N)
    {
        // create componets
        count = N;
        id = new int[N];
        for (int i=0; i<N; i++)
            id[i] = i;
    }
    
    public int count()
    { return count; }
    
    public boolean connected(int p, int q)
    { return find_quick_find(p) == find_quick_find(q); }
    
    public int find_quick_find(int p)
    { return id[p]; }
    
    public void union_quick_find(int p, int q)
    { 
        int pID = find_quick_find(p);  // 1次
        int qID = find_quick_find(q);  // 1次
        
        if (pID == qID) return;
        
        for (int i=0; i<id.length; i++) // 循环 N 次
            if (id[i] == pID) id[i] = qID;  // 比较 1 次,如果等再赋值 1 次
        count--;
    }
    
    public static void main (String[] args)
    {
        try {
            Reader r = new Reader();
            r.setPath(tinyUF);
            int N = r.readInt();
            UF uf = new UF(N);
            Reader.IntPair ip;
            while ((ip = r.readIntPair()) != null) {
                int p = ip.first;
                int q = ip.second;
                if (uf.connected(p, q)) continue;
                uf.union_quick_find(p, q);
                System.out.println(p + " " + q);
            }
            System.out.println(uf.count() + " components");
        } catch (IOException e) { e.printStackTrace();}
    }
}