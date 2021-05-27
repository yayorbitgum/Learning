#include <iostream>

int main()
{
    int number = 25;
    // A pointer to an int, a reference. Pointers are made with "*".
    int* pointer;
    // This stores the address of "number". Get the address with "&".
    pointer = &number;

    // Print address.
    std::cout << pointer << std::endl;

    return 0;
}
