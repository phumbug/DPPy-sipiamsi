import sys

try:
    current_age = int(input(""))
    my_age = current_age + 42
    print(my_age)
    
except ValueError:

    print("Please enter a valid integer.")
    sys.exit(1)