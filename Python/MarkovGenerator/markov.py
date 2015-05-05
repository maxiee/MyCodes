from random import choice
import re

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
    for char in model[fragment].keys():
        for times in range(0, model[fragment][char]):
            chars.append(char)
    return choice(chars)

def generateText(text, order, length):
    model = generateModel(text, order)
    
    currentFragment = text[0:order]
    output = ''
    for i in range(0, length-order):
        newChar = getNextChar(model, currentFragment)
        output += newChar
        currentFragment = currentFragment[1:] + newChar
    print(output)

def pureText(text):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、“”：~@#￥%……&*（）]+", "", text)  

text = \
'''
“互联网+”很火，创业很热。

　　“再不创业就老了！”在“大众创业、万众创新”的大潮下，凭着对互联网新技术的敏感和青春的激情，越来越多的年轻人加入“互联网+”创业的大军。

　　什么是“互联网+”？今年政府工作报告中指出，要“制定‘互联网+’行动计划，推动移动互联网、云计算、大数据、物联网等与现代制造业结合”。这表明，“互联网+”，就是要在传统行业与互联网新技术之间建立连接，利用互联网信息技术对传统行业进行升级改造，使传统生产方式互联网化。

　　这只是从宏观概念上对“互联网+”进行的阐释。而对于那些熟稔互联网的年轻人来说，进行“互联网+”创业，最难的可能并不是“互联网”的这一部分，“+”号后面的那部分以及怎么“+”或许才是更难搞定的。

　　如今，说起互联网创业，“低门槛”似乎已经成为共识。但从另一方面看，低门槛的背后，是不足10%的创业成功率。而低成功率的背后，往往是天马行空的想法多，而能落到实处的凤毛麟角。有人指出，其原因就在于不少创业者对传统行业了解得不够彻底，作出的很多设想不切实际。

　　创业圈有一句话广为流传：“站在风口，猪都能飞起来。”的确，如今在互联网之风的劲吹下，各行各业都在掀起革命，互联网金融、互联网农业、互联网医疗等等遍地开花。青年创业者对互联网技术的敏感度毋庸置疑，但由于缺乏在传统行业深耕的经验，对于“+”号后面的部分的理解以及怎么“+”往往还是致命缺陷。而另一方面，深耕传统行业的企业家们也并非都在坐以待毙，等着被互联网来革命，“互联网+”同时也正倒逼着传统行业进行“+互联网”的革命，这种激烈竞争更是让年轻人的互联网创业增添难度。

　　当下，随着国家政策的大力支持，年轻人进行互联网创业越来越容易，创业的速度也越来越快。但在追求“天下武功，唯快不破”的同时，似乎也应当脚踏实地地向传统行业学习经验。毕竟，大风吹过之后，一切总会落地，出落成凤凰的毕竟是少数，如若不慎，恐怕落下的将是一地鸡毛。
'''

print(generateText(pureText(text), 2, 100))
