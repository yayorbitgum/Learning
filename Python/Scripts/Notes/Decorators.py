# https://stackoverflow.com/questions/739654/how-to-make-function-decorators-and-chain-them-together
#
#
# So why use them? There are thousands of possibilities.
# A classic use is extending a function behavior from an external library that you can't modify,
# or for debugging (You don't want to modify the function because the debug is temporary).

# ------------------------------------------------------------------------------
# A decorator is just a function that expects ANOTHER function as parameter.
def decorator(a_function_to_decorate):

    # Inside, the decorator defines a function on the fly: The wrapper.
    # This function is going to be wrapped around the original function
    # so it can execute code before and after it.

    def the_wrapper():
        # Put code here that you want to be executed BEFORE the original function.
        print('Before the function runs.')
        # Call the function here. (use parenthesis)
        a_function_to_decorate()
        # Put code here that want you executed after.
        print('After the function runs.')

    # At this point, "a_function_to_decorate" hasn't been executed.
    # The wrapper contains the function and the code to wrap it in.
    # So we return the wrapper (without parenthesis, not calling it here).
    return the_wrapper


# ------------------------------------------------------------------------------
# Now imagine you create a function you never want to touch again.
def standalone():
    print("I am a standalone function. Don't modify me OR ELSE!!")


# You can decorate it to extend its behavior instead of needing to modify it.
standalone_decorated = decorator(standalone)
standalone_decorated()

# You probably want that every time you call standalone(),
# it calls standalone_decorated() instead.
standalone = decorator(standalone)
standalone()

# THAT is what decorators do.


# ------------------------------------------------------------------------------
@decorator
def another_standalone():
    print("Don't touch me WITCH!")


another_standalone()
# It's the pythonic approach to https://en.wikipedia.org/wiki/Decorator_pattern.
# "allows behavior to be added to an individual object, dynamically, without
# affecting the behavior of other objects from the same class."


# The decorator pattern is often useful for adhering to the
# Single Responsibility Principle, as it allows functionality to be divided
# between classes with unique areas of concern.


# ------------------------------------------------------------------------------
# You can accumulate multiple decorators too.
def bread(funk):
    def wrapper():
        print("</''''''\>")
        funk()
        print("<\______/>")
    return wrapper


def ingredients(funk):
    def wrapper():
        print("#tomatoes#")
        funk()
        print("~salad~")
    return wrapper


@bread
@ingredients
def sandwich(food='--salmon--'):
    print(food)


sandwich()


# ------------------------------------------------------------------------------
# You can decorate methods (in classes) too!
# Just be sure to pass (self) into the wrapper too.


# ------------------------------------------------------------------------------
# NOTES!
#
# - Decorators slow down the function call.
# - You cannot un-decorate a function. It will always be decorated from there.
#
# - Since they wrap functions, they can be hard to debug.
#   - Import functools to get functools.wraps().
#   - This gives us debugging help:
#       - Copies the name, module, and docstring of the decorated function, to its wrapper.