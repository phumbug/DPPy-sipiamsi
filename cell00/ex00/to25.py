user_input = input("Enter a number less than 26 : ")
number = int(user_input)


if number > 25:
    print("Error")

else:
 while number <= 25:
    print(f" Inside the loop my variable is {number}")
    number += 1

