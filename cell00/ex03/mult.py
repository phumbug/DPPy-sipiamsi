num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

result = num1 * num2
print("{num1} * {num2} = {result}".format(num1=num1, num2=num2, result=result))

if result > 0:
    print("The result is positive.")
elif result < 0:
    print("The result is negative.")
else:
    print("The result is zero.")