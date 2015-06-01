#include <iostream>

using namespace std;

double avg(double x, double y);

int main() {
    double ctemp, ftemp;

    cout << "Input a Celsius temp and press ENTER:";
    cin >> ctemp;
    ftemp = (ctemp * 1.8) + 32;
    cout << "Fahrenheit temp is: " << ftemp << endl;

    for (int i=0; i <= 20; i++) {
        cout << i << " ";
    }

    cout << endl << avg(99, 0) << endl;

    return 0;
}

double avg(double x, double y) {
    return (x + y) / 2;
}