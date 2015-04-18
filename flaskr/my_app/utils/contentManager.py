from pathlib import Path
import json

p = Path('.') / 'my_app' / 'posts'
results = [] 
seperator = '-'

def generateContent(p, url):
    import urllib.parse
    r = []
    dfs = p.iterdir()
    for i in dfs:
        if i.is_dir():
            dir_dict = {}
            dir_dict['text'] = i.name
            res = generateContent(i, url)
            if res is not []:
                dir_dict['nodes'] = res
            r.append(dir_dict)
        else: # file
            file_dict = {}
            file_dict['text'] = i.name
            file_dict['href'] = str(i)[str(i).find('posts')+len('posts/'):].replace('.mk','').replace("/","-")
            if i.name.replace(".mk",'') == url.split(seperator)[-1]:
                file_dict['state'] = {'selected':True}
            r.append(file_dict)
    return r

def getContent(url):
    return json.dumps(generateContent(p, url))

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
    print(getContent())
