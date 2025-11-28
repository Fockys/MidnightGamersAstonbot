import random

def slotsGame():
    """
    Slots gambling game, 3 symbols are choosen and different win amounts depending on what the symbols are
    Args:
        none
    Returns:
        int prizeMultiplier : the amount to multiply the bet amount by in any case (this also corresponds to the different types of wins)
        str symbolsOutput : the selected 3 symbols returned to a user
    """
    symbols = ["melon","pear","peach","orange","lemon","cherries","grapes","crown","strawberry","blueberry","apple","banana","watermelon","pineapple","kiwi"]
    symbolEmoji = {
        "melon":"🍈",
        "pear":"🍐",
        "peach":"🍑",
        "orange":"🍊",
        "lemon":"🍋",
        "cherries":"🍒",
        "grapes":"🍇",
        "crown":"👑",
        "strawberry":"🍓",
        "blueberry":"🫐",
        "apple":"🍏",
        "banana":"🍌",
        "watermelon":"🍉",
        "pineapple":"🍍",
        "kiwi":"🥝"
    }
    numSymbols = len(symbols)
    #get 3 random symbols
    symbolsSelected = []
    for i in range(3):
        symbolsSelected.append(symbols[random.randint(0,numSymbols-1)])

    symbolsSelected = sorted(symbolsSelected)



    #get the longest repeating symbol and if the crown symbol is present
    longest = 0
    crown = False
    for i in range(len(symbolsSelected)):
        j=i
        if symbolsSelected[i] == "crown":
            crown = True
        while j< len(symbolsSelected) and symbolsSelected[j] == symbolsSelected[i]:
            j += 1
            longest = max(longest,j-i)


    

    #case 1: 3 matching symbols
    if longest == 3:
        if crown:
            prizeMultiplyer = 100 #note 100 corresponds to the jackpot
        else:
            prizeMultiplyer = 5
    #case 2: 2 matching symbols
    elif longest == 2:
        if crown:
            prizeMultiplyer = 3
        else:
            prizeMultiplyer = 2
    #other case: where no matching symbols
    else:
        if crown:
            prizeMultiplyer = 1
        else:
            prizeMultiplyer=0


    #returns the prize mutliplier and symbols selected
    returnSymbols = []
    for symbol in symbolsSelected:
        returnSymbols.append(symbolEmoji[symbol])
    return(prizeMultiplyer,''.join(returnSymbols))




    
if __name__ == "__main__":
    total = 0
    for i in range(100000):
        result = slotsGame()
        if result[0] == 100:
            print(result[1])
            print("jackpot")
        total += result[0]

    print(total)