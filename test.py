x = 1
counting = True

def check_for_seven(inputint):
    if inputint == 7:
        print(f'{inputint} is equal to seven')
        return True

def check_for_ten(inputint):
    if inputint == 10:
        print('Leaving')
        return True

while counting:
    if check_for_seven(x):
        x = x + 1
        continue
    print(f'{x} is not seven')
    if check_for_ten(x):
        break
    x = x+1

print('finished')