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
        if i.name == "from_weibo_233.txt":
            #print("搞笑加强")
            for k in range(5):
                text += i.open().read()
        text += i.open().read()

count = 8 
print('作为一个立志成为文联主席的段子机器人, 来来来, 听我吟诗一首:\n')

for i in range(count):
    #print('%d. '% i + generateText(pureText(text), 2, 8) + '\n')
    print('\t' + generateText(pureText(text) , 3, 10) + '\n')
#s = generateText(pureText(text), 3, 58)
#for i in range(8):
#    print(s[i*8: i*8+7] + '\n')
