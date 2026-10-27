import sys

def main() :
    try :
        user_input = input()
        number = float(user_input)
        if number == 0 :
            print("number is equal to zero")
        else :
            print("This number is different from zero")
    except ValueError :
        print("Invalid input")

if __name__ == "__main__":
    main()