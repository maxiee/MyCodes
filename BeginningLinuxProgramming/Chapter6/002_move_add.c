#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<curses.h>

int main()
{
    const char witch_one[] = " First Witch ";
    const char witch_two[] = " Second Witch ";
    const char *scan_ptr;

    initscr();
    move(5, 15);
    attron(A_BOLD);
    printw("%s", "Macbeth");
    attroff(A_BOLD);
    refresh();
    sleep(1);

    move(8, 15);
    attron(A_STANDOUT);
    printw("%s", "Thunder and Lightning");
    attroff(A_STANDOUT);
    refresh();
    sleep(1);

    move(10, 10);
    printw("%s", "When shall we there meet again");
    move(11, 23);
    printw("%s", "In thunder, lightning, or in rain ?");
    move(13, 10);
    printw("%s", "When the hurlyburly's done.");
    move(14, 23);
    printw("%s", "When the battle's lost and won.");
    refresh();
    sleep(1);

    attron(A_DIM);
    scan_ptr = witch_one + strlen(witch_one) - 1;
    while(scan_ptr != witch_one) {
        move(10, 10);
        insch(* scan_ptr--);
        sleep(1);
        refresh();
    }
    scan_ptr = witch_two +strlen(witch_two) - 1;
    while(scan_ptr != witch_two) {
        move(13, 10);
        insch(*scan_ptr--);
        sleep(1);
        refresh();
    }
    attroff(A_DIM);
    refresh();
    sleep(1);
}
