def is_even(n):
    return n%2

def validate(n):
    print(f"Is {n} even?")
    if (not is_even(n)):
        print(f"Yes, {n} is Even")
    else:
        print(f"No, {n} is NOT Even")
    
    print()
    
def main():
    n = 9
    validate(n)

    # What about below input?
    n = "9"
    validate(n)

    n = "is 9 is even?"
    validate(n)

    n = "is nine is even?"
    validate(n)
    

        
if __name__ == "__main__":
    main()
