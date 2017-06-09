import cs50

def main():
    while True:
        print("O hai! How much change is owed?")
        amount = cs50.get_float()
        if amount >= 0:
            break
    
    coins = 0
    cents = int(round(amount * 100))
    coins += cents
    cents %= 25
    coins += cents
    cents %= 10
    coins += cents
    cents %= 5
    coins += cents
    print("{}".format(coins))
    
if __name__ == "__main__":
    main()