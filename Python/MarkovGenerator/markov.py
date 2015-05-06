import random
import re
from pathlib import Path

def generateModel(text, order):
    model = {}
    for i in range(0, len(text) - order):
        fragment = text[i:i+order]
        next_char = text[i+order]
        if fragment not in model:
            model[fragment] = {}
        if next_char not in model[fragment]:
            model[fragment][next_char] = 1
        else:
            model[fragment][next_char] += 1
    return model

def getNextChar(model, fragment):
    chars = []
    if fragment not in model:
        return ''
    for char in model[fragment].keys():
        for times in range(0, model[fragment][char]):
            chars.append(char)
    return random.choice(chars)

def generateText(text, order, length):
    model = generateModel(text, order)
    randomIndex = random.randint(0,len(text)-1)
    currentFragment = text[randomIndex:randomIndex+order]
    output = ''
    for i in range(0, length-order):
        newChar = getNextChar(model, currentFragment)
        output += newChar
        currentFragment = currentFragment[1:] + newChar
    return output

def pureText(text):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？《》、“”：~@#￥%……&*（）]+", "", text)  

path = Path('yuliao')
text = ""
dfs = path.iterdir()
for i in dfs:
    if not i.is_dir():
        #print("加载语料:%s" % i.name)
        text += i.open().read()

count = 3
print('作为一个懂 Markov chain 的 Python，一开始让我讲段子我也是拒绝的。 看你姿势水平这么需要加强，我就赐你 %d 句金玉良言：\n' % count)

for i in range(count):
    print('%d. '% i + generateText(pureText(text), 2, 50) + '\n')
