'''
动态随机爬取糗百上的一条笑话
'''
import requests
from lxml import etree
from random import randint

def get_joke():
    url = "https://www.qiushibaike.com/text/page/" + str(randint(1,20))
    html = requests.get(url).text
    if html:
        tree = etree.HTML(html)
    else:
        url = "https://www.qiushibaike.com/text/page/" + str(randint(1,5))
        html = requests.get(url).text
        tree = etree.HTML(html)
    content_list = tree.xpath('//div[@class="content"]/span')
    jokes = []
    for content in content_list:
        #使用string()函数将所有子文本串联起来，必须传递单个节点，而不是节点集
        content = content.xpath('string(.)')
        jokes.append(content)
    joke = jokes[randint(1,len(jokes))].strip()
    return joke


if __name__ == "__main__":
    content = get_joke()
    print(content)
