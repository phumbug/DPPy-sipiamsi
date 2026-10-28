i = 0
while i <= 10:
    print(f"Table de {i}: ", end="")
    j = 0
    while j <= 10:
        result = i * j
        if j < 10:
            print(f"{result}, ", end="")
        else:
            print(f"{result}, ", end="")
        j += 1
    print()
    i += 1