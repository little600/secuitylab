import os,random,time,hashlib



def sleep():
    time.sleep(random.random())


def get_invite_code(s):
    sha256=hashlib.sha256()
    sha256.update(s.encode('utf-8'))
    res = sha256.hexdigest()
    return res[0:16]