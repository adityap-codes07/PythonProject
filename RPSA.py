def game(score):
    with open('High_score.txt') as f:
        val=f.read()
        if val=='':
            highsc=0
        else:
            highsc=int(val)
    if highsc==0:
        print(f"It's a new high score:{score}")
        with open('High_score.txt','w') as f:
            f.write(str(score))
    elif highsc==score:
        print(f'You reached previous high score:{score}')
    elif highsc>score:
        print(f"Oops! You didn't reach the previous high score:{highsc}")
    else:
        print(f'Congrats! you broke previous high score:{highsc}')
        with open('High_score.txt','w') as f:
            f.write(str(score))

import random
print('*****************************************************************************\nWelcome to virtual stone,paper and scissors.')
print('Rules of the game are as follows:\n1.In stone and paper - paper wins\n2.In paper and scissors - scissors wins\n3.In scissors and stone-stone wins')
print('4.For stone press 1,paper press 2 and scissors press 3\n5.Press enter to terminate the game')
lis=['Stone','Paper','Scissors']
win=0
loss=0
while 1==1:
    move=input("Your's move: ").strip()
    comp=lis[random.randint(0,2)]
    if move !='':
        print(f"Computer's move: {comp}")
    if move=='':
        break
    elif int(move)==1 and comp=='Stone':
        print('Oops! it was a draw')
    elif int(move)==1 and comp=='Paper':
        print('You lost')
        loss+=1
    elif int(move)==1 and comp=='Scissors':
        print('You win')
        win+=1

    elif int(move)==2 and comp=='Paper':
        print('Oops! it was a draw')
    elif int(move)==2 and comp=='Scissors':
        print('You lost')
        loss+=1
    elif int(move)==2 and comp=='Stone':
        print('You win')
        win+=1

    elif int(move)==3 and comp=='Scissors':
        print('Oops! it was a draw')
    elif int(move)==3 and comp=='Stone':
        print('You lost')
        loss+=1
    elif int(move)==3 and comp=='Paper':
        print('You win')
        win+=1
    else:
        print('Invalid input')
    print()

print('Your score: ',win)
print('Computer score: ',loss)
if win>loss:
    print('Hence,You win')
elif win<loss:
    print('Hence,You loss')
else:
    print("Oops! it's a draw")
game(win)
print('Thank you for playing this game')
print('*****************************************************************************')
