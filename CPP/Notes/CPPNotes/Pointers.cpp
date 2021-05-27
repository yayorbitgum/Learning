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
    // -------------------------------------------------------------------
    int x = 25;
    // A pointer to an int, a reference. Pointers are made with "*".
    int* pointer;
    // This stores the address of "x". Get the address of x with "&".
    pointer = &x;

    // Print address.
    std::cout << pointer << std::endl;
    // You can dereference a pointer so you get the value pointed at,
    // rather than the address pointed at.
    // Print original value.
    std::cout << *pointer << std::endl;
    // In this case, "*pointer" essentially means "x".

    // -------------------------------------------------------------------
    // We allocate new memory to store an int, and point to it with p.
    int* p = new int;
    // Then we could assign a value to that memory location with that pointer dereferenced.
    *p = 5;

    // But if we later assign p to a new value (thus new memory location), the old location
    // can't be accessed anymore, so it's just garbage! Memory leaks SUCK.
    // So before the next line, we should do "delete p" to delete that now unused memory.
    delete p;
    p = new int(10);

    std::cout << p;

    return 0;
}
