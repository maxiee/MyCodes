from pathlib import Path
import json
import template
import re

p = Path('/home/maxiee/maxiee.github.io')
homepage_url = "/home/maxiee/maxiee.github.io/index.html"
URL_BASE="http://maxiee.github.io/static/html/"
PIC_BASE="https://raw.githubusercontent.com/maxiee/maxiee.github.io/master"
OUTPUT = str(p) + '/js/content.js'
HTML = str(p) + '/static/html/'
directory_blacklist = ['.git', 'css', 'js', 'static']
file_blacklist = ['README.md', 'index.html', '.swp', '.directory', '.png', '.gitignore', '.dia']
content_blacklist = ['resume.md']

total_count = 0
id_count = 0

def generateContent(p):
    global total_count
    global id_count
    res = []
    dfs = p.iterdir()
    for i in dfs:
        if i.is_dir(): #笔记目录
            if not isInBlacklist(directory_blacklist, i.name):
                dir_dict = {}
                dir_dict['label'] = i.name
                dir_dict['text'] = i.name
                dir_dict['id'] = id_count
                id_count += 1
                nodes = generateContent(i)
                if nodes is not []:
                    dir_dict['children'] = nodes
                res.append(dir_dict)
        else: #笔记文件
            if not isInBlacklist(file_blacklist, i.name):
                if '.md' in i.name: # .md 静态化
                    generateHtml(i)
                if not isInBlacklist(content_blacklist, i.name):
                    file_dict = {}
                    #file_dict['label'] = i.name.replace('.md', '')
                    #file_dict['href'] = URL_BASE + str.join(".", i.name.split('.')[:-1]) + '.html'
                    label = i.name.replace('.md', '')
                    href = URL_BASE + str.join(".", i.name.split('.')[:-1]) + '.html'
                    file_dict['text'] = label 
                    file_dict['label'] = '<a href="%s">%s</a>' % (href, label)
                    file_dict['id'] = id_count
                    id_count += 1
                    res.append(file_dict)
                    total_count += 1
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
    content = content.replace('<img ', '<img class="img-responsive" ')
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

def generateHomepage():
    header = template.HEADER % '主页'
    content = '共有笔记 %d 篇.' % total_count
    body = template.BODY % content
    homepage_file = open(homepage_url, 'w')
    homepage_file.write(header + body)
    homepage_file.close()
    

if __name__ == "__main__":
    # 生成笔记网页
    content = generateContent(p)
    # 生成目录
    f = open(OUTPUT, 'w')
    content = 'var data = ' + json.dumps(content, ensure_ascii=False)
    f.write(content)
    f.close()
    # 生成主页
    generateHomepage()
