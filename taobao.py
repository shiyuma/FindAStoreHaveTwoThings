# coding:utf-8
import urllib2 as request
from bs4 import BeautifulSoup
import re
import time

#pages_searched指定在淘宝上每个商品爬几页，默认50页，返回的是店铺id
def onepagesearch(link, pages_searched=50):
    set_userid = set()
    for i in range(pages_searched):
        #肉眼观察得淘宝点击下一页offset+44
        link_ini = link + str(44*i)
        try:
            html_ini = request.urlopen(link_ini)
            soup_ini = BeautifulSoup(html_ini)
            a = soup_ini.find_all('script')
            b = a[4]
            c = b.string.strip()
            pattern = re.compile("\"user_id\"\:\"(\d*)\"")
            result = pattern.findall(c)

            list_userid_i=[]
            for ss in result:
                list_userid_i.append(int(ss))
            set_userid_i = set(list_userid_i)
            set_userid = set_userid|set_userid_i
        except:
            print "can't open the link"
    return set_userid

#利用两件商品名分别进行搜索，得到店铺id的交集
def runit(name1, name2):
    start = time.clock()
    link1_pre = 'http://s.taobao.com/search?q='+name1+'&bcoffset=-4&s='
    link2_pre = 'http://s.taobao.com/search?q='+name2+'&bcoffset=-4&s='
    store_pre = 'store.taobao.com\\/shop\\/view_shop.htm?user_number_id='
    goods1 = onepagesearch(link1_pre)
    goods2 = onepagesearch(link2_pre)
    good_inter = set.intersection(goods1, goods2)
    end = time.clock()
    print "search is done, cost %f " %(end-start)
    list_good = list(good_inter)
    list_shop = []
    for i in list_good:
        list_shop.append(store_pre+str(i))
    return list_shop

def main():
    name1 = raw_input("输入商品名1")
    name1 = name1.encode('utf8')
    name2 = raw_input("输入商品名2")
    name2 = name2.encode('utf8')
    list_shop = runit(name1,name2)
    for shop in list_shop:
        print shop+'\n'
    #return list_shop

