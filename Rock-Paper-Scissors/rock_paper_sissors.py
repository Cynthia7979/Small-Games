import random
import time
R = 'rock'
P = 'paper'
S = 'scissors'
PASSWORD = 0
LEVEL = 1
usual_play = 2
WIN_NUM = 3
MATCH = {R: P, P: S, S: R}


def play(last_play=None, player_lv=0):
    if last_play is None:
        play_ = random.choice((R, P, S))
        plays = ()
    else:
        first_play = connect(last_play)
        second_play = connect(first_play)
        third_play = connect(second_play)
        plays = (first_play, second_play, third_play)
        actual_play = int(player_lv) + 1
        while actual_play >= len(plays):
            actual_play -= 1
        play_ = plays[actual_play]
    return play_, plays


def connect(play_):
    return MATCH[play_]


def main():
    players_data = read_file('data')
    for player in players_data.keys():
        if players_data[player][LEVEL] == '':
            players_data[player][LEVEL] = 0
        if players_data[player][usual_play] == '':
            players_data[player][usual_play] = R
    while True:
        player = raw_input('please enter your username:')
        if player not in players_data.keys():
            print('you are a new player, please enter your password')
            psw = raw_input('>')
            print(' please wait...')
            add_player(player,psw)
            print('added player ' + player)
            print('please log in again, your password is ' + psw)
            break
        psw = ''
        while psw != players_data[player][PASSWORD]:
            psw = raw_input('please enter password(enter exit to exit):')
            if psw == 'exit':
                break
        if psw == players_data[player][PASSWORD]:
            rungame(players_data[player],player)


def add_player(username,password):
    f = open('.\playerData.txt','a')
    f.write('\n\n'+username+'\n'+password)
    f.close()


def rungame(data, player):
    print('hello, ' + player + ', welcome to the rock paper scissors game')
    print('as the rule said, i must deal before you')
    print('now lets start')
    win_no = 0
    lose_no = 0
    play_data = []
    level_data = []
    round_no = 0
    level = data[LEVEL]
    # very first round
    computer_play = data[2]
    print('im ready')
    player_play = raw_input('(rock,paper,sissors):')
    play_data.append(player_play)
    result = justice(computer_play, player_play)
    print('computer ' + computer_play + ', player ' + player_play)
    print(result)
    if result == 'computer win':
        win_no += 1
    elif result == 'player win':
        lose_no += 1
    while True:
        last_play = player_play
        computer_play,plays = play(last_play, level)
        print('im ready')
        player_play = raw_input('(rock,paper,sissors,exit):')
        if player_play == 'exit':
            level = analyze(level_data)
            usual_play = analyze(play_data)
            data_config(player, level, usual_play)
            print('ok, see you next time, ' + player + '.')
            break
        play_data.append(player_play)
        result = justice(computer_play, player_play)
        print('computer ' + computer_play + ', player ' + player_play)
        print(result)
        if result == 'computer win':
            win_no += 1
        elif result == 'player win':
            lose_no += 1
        level_data.append(plays.index(player_play))
        round_no += 1
        if round_no >= 5:
            print('please wait , saving...')
            level = analyze(level_data)
            usual_play = analyze(play_data)
            data_config(player, level, usual_play)
            round_no = 0
            time.sleep(10)


def analyze(data):
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


def read_file(mode):
    if mode == 'data':
        f = open('.\playerData.txt')
        txt = f.read()
        lst = txt.split('\n\n')
        data_lst = []
        player_data = {}
        for p in lst:
            data_lst.append(p.split('\n'))
        for data in data_lst:
            other = data[1:]
            while len(other) < 3:
                other.append('')
            player_data[data[0]] = other
        f.close()
        return player_data


def data_config(username, lv, usl_play):
    data = read_file('data')
    data[username][LEVEL] = lv
    data[username][usual_play] = usl_play
    s = []
    for user in data.keys():
        s1 = user + '\n' + str(data[user][PASSWORD]) + '\n' + str(data[user][LEVEL]) + '\n' \
             + str(data[user][usual_play]) + '\n\n'
        s.append(s1)
    s[-1] = s[-1].replace('\n\n', '')
    f = open('.\playerData.txt', 'w')
    s = ''.join(s)
    f.write(s)
    f.close()


def justice(pc, user):
    if pc == user:
        return 'tie'
    elif pc == MATCH[user]:
        return 'computer win'
    elif user == MATCH[pc]:
        return 'player win'

if __name__ == '__main__':
    main()
