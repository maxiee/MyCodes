#include <iostream>

using namespace std;

void swap(int *a, int *b);
void printArray(int *v, int n);

int main() {
    int array[5] = {30, 10, 0, 50, 25};
    int i, j;
    int min_index;

    printArray(array, 5);

    for(i = 0; i < 4; i++) {
        min_index = i;
        for (j=i+1; j<5; j++) {
            if(array[j] < array[min_index]) {
                min_index = j;
            }
        }
        if (i != min_index) {
            swap(array[i], array[min_index]);
        }
        printArray(array, 5);
    }

    printArray(array, 5);

    return 0;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void printArray(int *v, int n){
    for (int i=0; i<n; i++) {
        cout << *v << " ";
        v++;
    }
    cout << endl;
}

