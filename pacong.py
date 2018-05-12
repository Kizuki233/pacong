# coding=gbk
import os
from lxml import etree
import requests
import multiprocessing


def download(a, b, url1, headers, n,items2_list):
    u='http://www.mm131.com/xinggan/'+b
    headers1 = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'img1.mm131.me',
        'Referer': u,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    req3 = requests.get(url1 + a)
    #req3 = requests.get(url1 + a,headers=headers)

    url_f = etree.HTML(req3.content).xpath("//div/div/a/img/@src")
    url_str = ''.join(url_f)  #返回通过指定字符连接序列中元素后生成的新字符串。
    
    with open("F:\\pypctest\\" + str(n) + ".jpg", "wb") as f:
        print("Saving {} pic,lefting {} pic".format(n,len(items2_list)))
        f.write((requests.get(url_str, headers=headers1)).content)
    items2_list.remove(a)  # 解析一条就会删除一条


def htmlparser2(i,headers,items2_list,items_list):
    
    resp2 = requests.get(i)
    #resp2 = requests.get(i, headers=headers)

    root2 = etree.HTML(resp2.content)
    items2 = root2.xpath('//div[@class="content-page"]/a/@href')
    #items2 = list(set(items2))  # 去重
    items2_list.extend(items2)
    items_list.remove(i) # 解析一条就会删除一条


def htmlparser(i,headers,items_list):
    url = "http://www.mm131.com/xinggan/list_6_{}.html".format(str(i))
    
    # req = requests.session().get(url, headers=headers)  #要用cookie headers的时候
    req = requests.get(url)
    #req = requests.get(url, headers=headers)
    
    root = etree.HTML(req.content)
    items = root.xpath('//dl[@class="list-left public-box"]/dd/a[@target="_blank" ]/@href')
    items_list.extend(items)


# Pool类可以提供指定数量的进程供用户调用，当有新的请求提交到Pool中时，
# 如果池还没有满，就会创建一个新的进程来执行请求。如果池满，请求就会告知先等待，直到池中有进程结束，才会创建新的进程来执行这些请求。 
# windows必须要 if __name__ == '__main__':
if __name__ == '__main__':

    output_dir='F:\\pypctest'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    url1 = "http://www.mm131.com/xinggan/"
    headers = {
        'User-Agent': 'Baiduspider+(+http://www.baidu.com/search/spider.html")',
        'Referer': 'https://www.baidu.com/link?url=mPARC6e0QgmXiBEX1UCXo62Hsl1XIxYOsAVJUsS9R_SumSXwtLn3_XcPCIxWUC7U&wd=&eqid=af85b81300074c38000000025ae83304',
        'Cookie': 'UM_distinctid=162299332741c7-07936edc87635f-7b113d-100200-162299332753a2; bdshare_firstime=1521115935504; CNZZDATA3866066=cnzz_eid%3D306650475-1494676185-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1494676185; Hm_lvt_9a737a8572f89206db6e9c301695b55a=1525162468,1525165327,1525165615,1525165652; Hm_lpvt_9a737a8572f89206db6e9c301695b55a=1525165916',
        'Upgrade - Insecure - Requests': '1',
        'Host': 'www.mm131.com',
        'Connection': 'keep - alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    } #伪装？

    n = 1  # TODO 直接开启
    items_list=multiprocessing.Manager().list()
    items2_list = multiprocessing.Manager().list()
    pool = multiprocessing.Pool(40)
    pool1 = multiprocessing.Pool(40)
    pool2 = multiprocessing.Pool(40)

    print("***************************First*****************************")  
    for i in range(2, 4):  #2-140页，每页20，该网站第一页无后缀，第二页后有后缀
        pool.apply_async(htmlparser, (i,headers,items_list))

    pool.close()#先close() 再join()
    pool.join()
    print("**************************First done*************************")


    print('Len of items_list is',len(items_list))
    print("***************************Second*****************************")
    for i in items_list:
        pool1.apply_async(htmlparser2, (i,headers,items2_list,items_list))

    pool1.close()
    pool1.join()
    print("**************************Second done*************************")

    print('Len of items2_list is',len(items2_list))
    print("***************************Download*****************************")
    for a in items2_list:
        b=a[:4]+a[-5:]
        #print(b) 3548_4.html -> 3548.html
        pool2.apply_async(download, (a, b, url1, headers, n,items2_list))
        n += 1

    pool2.close()
    pool2.join()
    print("It is over")
