package com.maxiee.algorithms.UnionFind;

import com.maxiee.algorithms.utils.Reader;

import java.io.IOException;

public class UF
{
    private static final String tinyUF = "/home/maxiee/MyCodes/Algorithms/src/com/maxiee/algorithms/UnionFind/tinyUF.txt";
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
    { return find(p) == find(q); }
    
    public int find (int p)
    { return id[p]; }
    
    public void union (int p, int q)
    { 
        int pID = find(p);
        int qID = find(q);
        
        if (pID == qID) return;
        
        for (int i=0; i<id.length; i++)
            if (id[i] == pID) id[i] = qID;
        count--;
    }
    
    public static void main (String[] args)
    {
        try {
            Reader r = new Reader();
            r.setPath(mediumUf);
            int N = r.readInt();
            UF uf = new UF(N);
            Reader.IntPair ip;
            while ((ip = r.readIntPair()) != null) {
                int p = ip.first;
                int q = ip.second;
                if (uf.connected(p, q)) continue;
                uf.union(p, q);
                System.out.println(p + " " + q);
            }
            System.out.println(uf.count() + " components");
        } catch (IOException e) { e.printStackTrace();}
    }
}