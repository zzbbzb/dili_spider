#coding:utf-8

import requests
from bs4 import BeautifulSoup
from Tkinter import *
import webbrowser

animations = []
animations_details=[]

top = Tk()
listL = Listbox(top)
listR = Listbox(top)

def gethtmlbyUrl(url):
    hearder = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Host":"www.dilidili.wang"
    }
    con = requests.get(url,hearder)
    # print con.content
    return con.content

def main():
    global animations
    html = gethtmlbyUrl("http://www.dilidili.wang/anime/201710/")
    bs = BeautifulSoup(html,"lxml")
    animation_lists = bs.find_all("div",class_ = 'anime_list')
    for a_list in animation_lists:
        a = a_list.find_all("h3")
        for x in a:
            k = x.find('a')
            link = k.get('href')
            if link:
                animations.append({
                    'name':k.text,
                    'link':link })
                #print (k.text+":"+link)

    #html2 = gethtmlbyUrl("http://www.dilidili.wang"+animations[0]['link'])
    #print (html2)

    for x in animations:
        listL.insert(END,x['name'])
    listL.bind("<Double-Button-1>",lambda x:doubleClick(x,listL))

def doubleClick(event,list):
    #print(11)
    global animations
    index = list.curselection()[0]
    #print index
    url = "http://www.dilidili.wang"+animations[int(index)]['link']
    html = gethtmlbyUrl(url)
    #print (html)
    main2(html)

def doubleClickR(event,listR):
    global animations_details
    index = listR.curselection()[0]
    #print index
    #print animations_details
    if index!=0:
        url = animations_details[int(index)]['src']
        webbrowser.open(url)

def main2(html):
    global  animations_details
    animations_details = []
    bs = BeautifulSoup(html,'lxml')
    li_lists = bs.find("ul",class_="clear").find_all('li')
    for li in li_lists:
        if li.text != 'undefined':
            name = li.find('em').text
            src = li.find('a').get('href')
            if src:
                animations_details.append({
                    "name":name,
                    "src":src
                })
                #print(name+":"+src)
    listR.delete(0,END)
    if len(animations_details)!=0:
        for list in animations_details:
            listR.insert(END,list['name'])
        listR.bind("<Double-Button-1>",lambda x:doubleClickR(x,listR))
    else:
        listR.insert(END,"暂无信息")

if __name__ == "__main__":
    main()
    listL.pack(side=LEFT)
    listR.pack(side=RIGHT)

    top.mainloop()




