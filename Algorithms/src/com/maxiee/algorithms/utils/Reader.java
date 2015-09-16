package com.maxiee.algorithms.utils;

import java.io.*;

/**
 * Created by maxiee on 15-9-15.
 */
public class Reader {

    private BufferedReader br;

    public void setPath(String path) throws IOException{
        FileReader fb = new FileReader(path);
        br = new BufferedReader(fb);
    }

    public int readInt() throws IOException{
        String line = br.readLine();
        return Integer.valueOf(line);
    }

    public IntPair readIntPair() throws IOException {
        String line = br.readLine();
        if (line == null) return null;
        String[] spt =  line.split(" ");

        IntPair ip = new IntPair();
        ip.first = Integer.valueOf(spt[0]);
        ip.second = Integer.valueOf(spt[1]);
        return ip;
    }

    public class IntPair {
        public int first;
        public int second;
    }
}
