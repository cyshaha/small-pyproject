'''
爬取天气信息
'''
#将汉字转拼音模块
from xpinyin import Pinyin
import requests
from lxml import etree

def get_weather(city):
    p = Pinyin()
    city = p.get_pinyin(city,'')
    url = "http://www.tianqi.com/"+city
    headers = {
        'User-Agent':'Mozilla/5.0'
    }
    html = requests.get(url,headers=headers).text
    tree = etree.HTML(html)
    #城市
    try:
        city_name = tree.xpath('//dd[@class="name"]/h2/text()')[0]
    except:
        content = "没有该城市天气信息，请确认你查询格式"
    #日期格式:"2019年06月25日　星期二　己亥年五月廿三" 
    week = tree.xpath('//dd[@class="week"]/text()')[0].split('\u3000')
    #当前温度
    now = tree.xpath('//p[@class="now"]')[0].xpath('string(.)')
    #今日天气
    temp = tree.xpath('//dd[@class="weather"]/span')[0].xpath('string(.)')
    #湿度匹配出三个元素:1.湿度：84%  2.风向：东风 2级  3.紫外线：无
    shidu = tree.xpath('//dd[@class="shidu"]/b/text()')
    #空气质量格式：空气质量：优
    kongqi = tree.xpath('//dd[@class="kongqi"]/h5/text()')[0]
    #PM格式：PM: 14
    pm = tree.xpath('//dd[@class="kongqi"]/h6/text()')[0]
    content = "【{0}】\n{1}  {2}\n当前温度：{3}\n今日天气：{4}\n{5}\n{6}\n{7}\n{8}\n{9}".format(
        city_name,week[0],week[1],now,temp,shidu[0],shidu[1],shidu[2],kongqi,pm)
    return content

if __name__ == "__main__":
    city = "上海"
    content = get_weather(city)
    print(content)



