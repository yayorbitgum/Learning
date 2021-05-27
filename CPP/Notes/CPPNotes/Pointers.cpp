/* https://www.youtube.com/watch?v=W0aE-w61Cb8
 *
 * Uses of pointers:
 * - Refer to new memory reserved during execution.
 * - Refer and share large data structures without making copies of them.
 * - Specify relationships among data: Linked lists, trees, graphs, etc.
*/

#include <iostream>

int main()
{
    int x = 25;
    // A pointer to an int, a reference. Pointers are made with "*".
    int* pointer;
    // This stores the address of "x". Get the address of x with "&".
    pointer = &x;

    // Print address.
    std::cout << pointer << std::endl;
    // You can dereference a pointer so you get the value pointed at, rather than the address pointed at.
    // Print original value.
    std::cout << *pointer << std::endl;
    // In this case, "*pointer" essentially means "x".

    return 0;
}
