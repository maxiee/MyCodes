#include<stdio.h>

int main(int argc, char *argv[])
{
    int numbers[4] = {0};
    char name[4] = {'a'};

    printf("numbers: %d %d %d %d\n",
            numbers[0], numbers[1], numbers[2], numbers[3]);
    
    printf("name each: %c %c %c %c\n",
            name[0], name[1], name[2], name[3]);

    printf("name: %s\n", name);

    numbers[0] = 1;
    numbers[1] = 2;
    numbers[2] = 3;
    numbers[3] = 4;

    name[0] = 'Z';
    name[1] = 'e';
    name[2] = 'd';
    name[3] = '\0';

    printf("numbers: %d %d %d %d\n",
            numbers[0], numbers[1], numbers[2], numbers[3]);

    printf("name each: %c %c %c %c\n",
            name[0], name[1], name[2], name[3]);

    char *another = "zed";
    printf("another: %s\n", another);

    printf("another each: %c %c %c %c\n",
            another[0], another[1], another[2], another[3]);
    
    return 0;
}
