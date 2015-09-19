package com.maxiee.algorithms.Assignments;

/**
 * Created by maxiee on 15/9/17.
 */
public class Percolation {
    private static final boolean BLOCKED = false;
    private static final boolean OPEN = true;

    private int mN;
    private boolean[] mGrid;

    public Percolation (int N) {
        mN = N;
        mGrid = new boolean[N*N];
        for (int i=0; i<N*N; i++) {
                mGrid[i] = BLOCKED;
        }
    }

    public void open(int i, int j) {
        mGrid[(i-1)*mN + (j-1)] = OPEN;
    }

    public boolean isOpen(int i, int j) {return mGrid[(i-1)*mN + (j-1)];}

    public boolean isFull(int i, int j) {return true;}

    public boolean percolates() {return true;}

    public static void main(String[] args) {}
}
