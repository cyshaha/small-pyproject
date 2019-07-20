import urllib.request
import csv
from bs4 import BeautifulSoup

def get_html():
    '''
    逐页爬取房屋信息
    :return:
    '''
    #设置请求头
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    #在url中设置page用来翻页得到全部数据,用format方法格式化字符串

    #使用ip代理
    httpproxy_handler = urllib.request.ProxyHandler({'http':'125.110.116.76'})
    opener = urllib.request.build_opener(httpproxy_handler)
    urllib.request.install_opener(opener)

    #请求的url地址
    url = "https://sh.58.com/xuhui/pinpaigongyu/pn/{page}/?minprice=2000_3000"

    #定义初始页码page为0
    page = 0
    #打开re.csv文件，如果没有就创建一个
    csv_file = open('renting.csv','w',encoding='utf_8',newline='')
    #创建writer对象
    writer = csv.writer(csv_file,dialect='excel')
    #循环遍历页面
    while True:
        page += 1
        req = urllib.request.Request(url.format(page=page),headers=headers)
        resp = urllib.request.urlopen(req)
        # resp.encoding = 'utf-8'  #设置编码方式
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        #获取当前页房子的信息
        house_list = soup.select(".list > li")
        print("正在下载房屋列表",url.format(page=page))
        #当全部加载完成后，翻页按钮div由加载更多的class=‘loadbtn’变为没有更多信息了的class="loadbtn  disabled"
        #设定循环遍历结束的条件
        page_load_btn = soup.find('div',class_='loadbtn ')
        page_over = soup.find('div',class_='loadbtn disabled')
        #如果翻页按钮存在
        if page_load_btn != None:
                #数据写入,继续循环
            print(page_load_btn)
            write_file(house_list, writer)
        else:
            #把当前页面的数据写入, 关闭文件, 跳出循环
            write_file(house_list, writer)
            print(page_over)
            print("爬取结束")
            csv_file.close()
            break

def write_file(house_list,writer):
    '''
    csv文件写入数据
    :param house_list: 文本内容
    :param writer: 写入对象
    :return:
    '''
    for house in house_list:
        if house != None:
            #获取房子标题
            house_title = house.find('div',class_='img').img.get('alt')
            #对标题进行分割
            house_info_list = house_title.split()
            #获取房子位置
            house_location = house_info_list[1]
            #获取房子链接地址
            house_url = house.select('a')[0]['href']
            #写入一行数据
            writer.writerow([house_title,house_location,house_url])

if __name__ == "__main__":
    get_html()

#报错Temporary failure in name resolution
# sudo gedit /etc/resolv.conf打开DNS配置
#添加nameserver配置nameserver 180.118.86.33:9000
