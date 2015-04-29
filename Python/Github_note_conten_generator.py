from pathlib import Path
import json

path = Path('/home/maxiee/MyNotes')
p_len = len(str(path))

URL_BASE = 'https://github.com/maxiee/MyNotes/blob/master'

blacklist = ['.git']
file_blacklist = ['.png', 'README.md', '.directory']

def generateContent(p, dep):
    res = []
    depth = dep+1
    dfs = p.iterdir()
    for i in dfs:
        if i.is_dir():
            if i.name not in blacklist:
                # print(i.name)
                if depth == 0:
                    prefix = '###'
                elif depth == 1:
                    prefix = '####'
                else:
                    prefix = ''
                res.append(prefix+i.name+'\n')
                res.append(generateContent(i, depth))
        else:
            to_pass = False
            for fb in file_blacklist:
                if fb in i.name:
                    to_pass = True
                    break
            if not to_pass:
                res.append('* ' + '[%s](%s)' %(i.name, URL_BASE+str(i)[str(i).index(str(path))+p_len:])+'\n')
    return res

def isPureList(lst):
    for i in lst:
        if type(i) is list:
            return False
    return True

def printContent(cont):
    if isPureList(cont):
        cont = sorted(cont)
    for i in cont:
        if type(i) is list:
            printContent(i)
        else:
            print(i)
res = generateContent(path, -1)
# print(res)
printContent(res)


