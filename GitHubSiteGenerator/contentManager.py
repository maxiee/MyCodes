from pathlib import Path
import json
import template
import re

p = Path('/home/maxiee/maxiee.github.io')
URL_BASE="http://maxiee.github.io/static/html/"
PIC_BASE="https://raw.githubusercontent.com/maxiee/maxiee.github.io/master"
OUTPUT = str(p) + '/js/content.js'
HTML = str(p) + '/static/html/'
directory_blacklist = ['.git', 'css', 'js', 'static']
file_blacklist = ['README.md', 'index.html', '.swp', '.directory', '.png', '.gitignore', '.dia']

def generateContent(p):
    res = []
    dfs = p.iterdir()
    for i in dfs:
        if i.is_dir():
            if not isInBlacklist(directory_blacklist, i.name):
                dir_dict = {}
                dir_dict['text'] = i.name
                nodes = generateContent(i)
                if nodes is not []:
                    dir_dict['nodes'] = nodes
                res.append(dir_dict)
        else: # file
            if not isInBlacklist(file_blacklist, i.name):
                if '.md' in i.name: # .md 静态化
                    generateHtml(i)
                file_dict = {}
                file_dict['text'] = i.name
                #file_dict['href'] = str(i)[str(i).find('posts')+len('posts/'):].replace('.mk','').replace("/","-")
                file_dict['href'] = URL_BASE + str.join(".", i.name.split('.')[:-1]) + '.html'
                res.append(file_dict)
    return sorted(res, key=lambda k: k['text'])

def isInBlacklist(blacklist, filename):
    for fb in blacklist:
        if fb in filename:
            return True
    return False

def generateHtml(mdPath):
    import markdown
    mdFile = mdPath.open()
    content = mdFile.read()
    content = markdown.markdown(
            content,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables'])
    # convert pics
    content = re.sub(r'(figure+)', PIC_BASE + str(mdPath.parent).replace(str(p), "") + r'/\1', content)
    header = template.HEADER % str.join(".", mdPath.name.split('.')[:-1])
    body = template.BODY % content
    content = header + body
    htmlFile = open(HTML + str.join(".", mdPath.name.split('.')[:-1]) + '.html', 'w')
    htmlFile.write(content)
    mdFile.close()
    htmlFile.close()
    

def getContent():
    return json.dumps(generateContent(p))

def getPost(url):
    try:
        post = open(str(p)+'/'+url.replace("-","/")+'.mk')
    except:
        return "Get Post Error."
    post = post.read()
    post += '\n' + url
    import markdown
    return markdown.markdown(post)

if __name__ == "__main__":
    content = generateContent(p)
    f = open(OUTPUT, 'w')
    content = 'var tree = ' + json.dumps(content, ensure_ascii=False)
    f.write(content)
    f.close()
