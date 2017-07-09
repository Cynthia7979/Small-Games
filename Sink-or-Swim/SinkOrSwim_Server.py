import socket

max_player = 4

def main():
    s = socket.socket()
    port = 22104
    host = socket.gethostname()
    s.bind((host, port))
    mail_box = {}
    situ = {'player':[]}
    playersData = readPlayerData()
    while True:
        mail_box = box_update(mail_box, s)
        for addr in mail_box.keys:
            if mail_box[addr]['type'] == 'print type':
                print mail_box[addr]['string']
            elif mail_box[addr]['type'] == 'handle type':
                if mail_box[addr]['string'] == 'join':
                    if len(situ['player']) < max_player:
                        s.connect(addr)
                        s.send('print type_joined room 22104')
                        situ['player'].append((addr,playersData[addr]))
        #for msg in mail_box.keys():
        #    if mail_box[msg][type] == 'join':
        #        if len(situ['player']) < situ['max']:
        #            situ['player'].append(mail_box[msg]['from'])
        #            #tell him joined

                else:
                    pass
                    # tell him full
                    # break connection


def box_update(box, skt):
    skt.listen(5)
    c, addr = skt.accept()
    string = skt.recv(1024)
    type, string = string.split('_')
    if addr not in box.keys():
        box[addr] = {'type':type, 'string':string,'ip':c}
    else:
        c.send('print type_connection failed')
    skt.close()
    return box

def readPlayerData():
    f = open('./sink_swim_users_data.txt')
    baseRead = f.read()
    cuttedStrs = baseRead.split('\n\n')
    data = []
    for player in cuttedStrs:
        data.append(player.split('\n'))
    playerData = {}
    for d in data:
        playerData[d[0]] = d[1]
    return playerData
