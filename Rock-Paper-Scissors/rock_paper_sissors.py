import random, re
R = 'rock'
P = 'paper'
S = 'sissors'
PASSWORD = 0
LEVEL = 1
USUALPLAY =2
WINNUM = 3
MATCH = {R:P,P:S,S:R}

def play(lastPlay=None,playerLv=0):
    if lastPlay == None:
        play = random.choice((R,P,S))
    else:
        firstPlay = connect(lastPlay)
        secondPlay = connect(firstPlay)
        thirdPlay = connect(secondPlay)
        plays = (firstPlay,secondPlay,thirdPlay)
        autualPlay = int(playerLv) + 1
        while autualPlay >= len(plays):
            autualPlay -= 1
        play = plays[autualPlay]
    return play,plays

def connect(play):
    return MATCH[play]

def main():
    playersData = readFile('data')
    for player in playersData.keys():
        if playersData[player][LEVEL] == '':
            playersData[player][LEVEL] = 0
        if playersData[player][USUALPLAY] == '':
            playersData[player][USUALPLAY] = R
    while True:
        player = raw_input('please enter your username:')
        if player not in playersData.keys():
            print 'you are a new player, please enter your password'
            psw = raw_input('>')
            print ' please wait...'
            addPlayer(player,psw)
            print 'added player ' + player
            print 'please log in again, your password is ' + psw
            break
        psw = ''
        while psw != playersData[player][PASSWORD]:
            psw = raw_input('please enter password(enter exit to exit):')
            if psw == 'exit':
                break
        if psw == playersData[player][PASSWORD]:
            rungame(playersData[player],player)

def addPlayer(username,password):
    f = open('.\playerData.txt','a')
    f.write('\n\n'+username+'\n'+password)
    f.close()

def rungame(data,player):
    print 'hello, '+ player + ', welcome to the rock paper sissors game'
    print '--don t mind sissors'
    print 'as the rule said, i must deal before you'
    print 'now lets start'
    winNo = 0
    loseNo = 0
    playData = []
    levelData = []
    roundNo = 0
    level = data[LEVEL]
    #very first round
    computerPlay = data[USUALPLAY]
    print 'im ready'
    playerPlay = raw_input('(rock,paper,sissors):')
    playData.append(playerPlay)
    result = justice(computerPlay, playerPlay)
    print 'computer ' + computerPlay + ', player ' + playerPlay
    print result
    if result == 'computer win':
        winNo += 1
    elif result == 'player win':
        loseNo += 1
    while True:
        lastPlay = playerPlay
        computerPlay,plays = play(lastPlay,level)
        print 'im ready'
        playerPlay = raw_input('(rock,paper,sissors,exit):')
        if playerPlay == 'exit':
            level = analysize(levelData)
            usualPlay = analysize(playData)
            dataConfig(player,level,usualPlay)
            print 'ok, see you next time, ' + player + '.'
            break
        playData.append(playerPlay)
        result = justice(computerPlay, playerPlay)
        print 'computer ' + computerPlay + ', player ' + playerPlay
        print result
        if result == 'computer win':
            winNo += 1
        elif result == 'player win':
            loseNo += 1
        levelData.append(plays.index(playerPlay))
        roundNo += 1
        if roundNo >= 5:
            print 'please wait , saving...'
            level = analysize(levelData)
            usualPlay = analysize(playData)
            dataConfig(player,level,usualPlay)
            roundNo = 0

def analysize(data):
    dic = {}
    lst = []
    for d in data:
        n = data.count(d)
        dic[n] = d
        lst.append(n)
    lst.sort()
    out = []
    for i in lst:
        out.append(dic[i])
    return out[0]
#    lst = []
#    biggest = 0
#    for i in diclst:
#        if i[1] > biggest:
#            biggest = i[1]
#        else:

def readFile(mode):
    if mode == 'data':
        f = open('.\playerData.txt')
        txt = f.read()
        lst = txt.split('\n\n')
        dataLst = []
        playerData = {}
        for p in lst:
            dataLst.append(p.split('\n'))
        for data in dataLst:
            other = data[1:]
            while len(other) < 3:
                other.append('')
#                if len(other) == 2:
#                    other.append('0')
#                elif len(other) == 3:
#                    other.append(random.choice((R,P,S)))
            playerData[data[0]] = other
        f.close()
        return playerData

def dataConfig(username,lv,uslPlay):
#    import re
#    fp3 = open(".\playerData.txt", "r+")
#    for s in fp3.readlines():
#        s = s.replace(prelv,lv)
#        s = s.replace(preuslPlay,uslPlay)
#        fp3.write(s)
#    fp3.close()
#    strOne = []
#    strTwo = ''
#    for i in playerData:
    data = readFile('data')
    data[username][LEVEL] = lv
    data[username][USUALPLAY] = uslPlay
    s = []
    for user in data.keys():
        s1 = user + '\n' + str(data[user][PASSWORD]) + '\n' + str(data[user][LEVEL]) + '\n' + str(data[user][USUALPLAY]) + '\n\n'
        s.append(s1)
    s[-1] = s[-1].replace('\n\n','')
    f = open('.\playerData.txt','w')
    s = ''.join(s)
    f.write(s)
    f.close()

def justice(pc,user):
    if pc == user:
        return 'tie'
    elif pc == MATCH[user]:
        return 'computer win'
    elif user == MATCH[pc]:
        return 'player win'

if __name__ == '__main__':
    main()
