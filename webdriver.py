from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import os
from bs4 import BeautifulSoup   #网页解析，数据获取
from docx import Document
import requests

findTitle = re.compile(r'<h1>(.*?)</h1>',re.S)
findEnd = re.compile(r'<div>(.*?)</div>',re.S)
findLink = re.compile(r'<a href="(.*?)">下一章</a>')

def main():
    #word
    Doc = Document()

    # 设置Chrome选项，模拟Chrome浏览器
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    #chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面

    # 初始化Chrome驱动
    driver = webdriver.Chrome(options=chrome_options)

    # test
    current_path = os.path.dirname(os.path.realpath(__file__))
    savepath = current_path + "/fuhuoquanrenlei.docx"
    print('save path', savepath)
    url = 'https://twkan.com/txt/73947/45140676'

    link = ""
    while(link!="https://twkan.com/txt/73947/end.html"):
        try:
            driver.get(url)
            #time.sleep(1)  # 等待页面加载，根据需要调整时间
            page_source = driver.page_source  # 获取页面源代码
            
            soup = BeautifulSoup(page_source, 'html5lib')
            items = soup.find_all('div',attrs = {'class':'txtnav'})
            for item in items:
                item = str(item)
                title = re.findall(findTitle, item)[0]
                print('title:',title)
                Doc.add_heading(title, level = 0)

            items = soup.find_all('div',attrs = {'id':'txtcontent0'})
            for item in items:
                for content in item.contents:
                    if not content.name:
                        Doc.add_paragraph(content.string)
                    #print(content)
            Doc.save(savepath)
            #跳转到下一页
            for item in soup.find_all('div', attrs = {'class':'page1'}):
                item = str(item)
                link = re.findall(findLink, item)[0]
                print('link', link)
                url = str(link)
        except requests.exceptions.RequestException as e:
            print(e)


    driver.quit()  # 关闭浏览器


if __name__ == "__main__":
    main()