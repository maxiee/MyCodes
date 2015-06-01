//
// Created by maxiee on 15-5-30.
//

#include <iostream>

using namespace std;

int const n = 5;
int stack[3][n] = {{1, 2, 3, 4, 5}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}};
int count = 0;


void move_rings(int n, int src, int dest, int other);
void print_stack();
int getTopNum(int numStack);
int getTopZero(int numStack);
void doMove(int src, int dest);

int main() {
    print_stack();
    move_rings(n, 0, 2, 1);
    return 0;
}

void move_rings(int n, int src, int dest, int other) {

//    cout << "move_rings(" << n << "," << src << "," << dest << "," << other << ")" << endl;

    if (n == 1) {
        doMove(src, dest);
    } else {
        move_rings(n - 1, src, other, dest);
        doMove(src, dest);
        move_rings(n - 1, other, dest, src);
    }
}

void print_stack() {
    cout << "***********第" << count << "轮**************" << endl;
    int line;
    for (line = 0; line < n; line++) {
        cout << stack[0][line] << "\t" << stack[1][line] << "\t" << stack[2][line] << endl;
    }
    count ++;
}

int getTopNum(int numStack) {
    int i;
    for (i=0; i<n; i++) {
        if (stack[numStack][i] != 0) {
            return i;
        }
    }
    return 3;
}

int getTopZero(int numStack) {
    int i;
    for (i=0; i<n-1; i++) {
        if (stack[numStack][i+1] != 0 && stack[numStack][i] == 0) {
            return i;
        }
    }
    return n-1;
}

void doMove(int src, int dest){
    int topSrc = getTopNum(src);
    int topDest = getTopZero(dest);
    int temp = stack[src][topSrc];
    stack[dest][topDest] = temp;
    stack[src][topSrc] = 0;
    print_stack();
}
