import socket


def main():
    s = socket.socket()
    port = 22104
    host = socket.gethostname()
    s.bind((host, port))
    mail_box = {}
    situ = {'player':[]}
    while True:
        mail_box = box_update(mail_box, s)
        for msg in mail_box.keys():
            if mail_box[msg][type] == 'join':
                if len(situ['player']) < situ['max']:
                    situ['player'].append(mail_box[msg]['from'])
                    #tell him joined
                    mail_box.pop()
                else:
                    pass
                    # tell him full
                    # break connection


def box_update(box, skt):
    skt.listen(5)
