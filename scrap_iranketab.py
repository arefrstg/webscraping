from bs4 import BeautifulSoup
import requests
import re

'''
حرکت در صفحات و پیدا کردن صفحه حاضر و اخرین صفحه درست شد 
لینک های صفحات و لینک های جزییات کتاب ها درست شد 
'''
# todo: رفتن داخل صفحات و گرفتن جزییات کتاب ها
# todo:طراحی استاندارد پایگاه داده
# todo: تست اولیه قرار گرفتن اطلاعات در دیتابیس 

website = 'https://www.iranketab.ir'
dic_page_ajax = {}
max_page = 0
current_page = 1


# url section

# ajax = 'https://www.iranketab.ir/tag/filtertags/437/literature?pagenumber=19&ispager=True&pagesize=20&sortOrder=date_desc&tagid=437'
# ajax2 = 'https://www.iranketab.ir/tag/97-american-literature?pagenumber=15&pagesize=20&sortOrder=date_desc&tagid=97'
# 'https://www.iranketab.ir/tag/512-best-historical-books'
#f'https://www.iranketab.ir/tag/512-best-historical-books?page=1'
def set_url(state, url='', ):
    if state == 'get':
        base_url = url
        site_1 = requests.get(base_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Cookie': '__RequestVerificationToken=xAsQOuQkDFjzIGtF7dXPvWf1uZy2zjuXyB_CToixrIEfhrK51OZXlMHp8oy4anVybBKmPyntst6mSxLTtKDdADgnSF4ZeMFItohmcovyBq81; _ga=GA1.1.1224430601.1702745675; analytics_token=cec90a4d-6b85-d2ae-b200-65b05af90cd1; _yngt_iframe=1; ASP.NET_SessionId=2zg05g0jhccl2whkxoyus3bf; _yngt=70485ff8-84c57-7272f-f9355-5985bf72cd122; analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; yektanet_session_last_activity=12/20/2023; analytics_session_token=fd34b465-31c2-afc3-cd3d-e15daf5e82cf; _ga_F7SRW3F8BJ=GS1.1.1703094354.8.1.1703097530.0.0.0'
        })
        return site_1
    elif state == 'post':
        base_url = url
        site_1 = requests.post(base_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Cookie': '__RequestVerificationToken=xAsQOuQkDFjzIGtF7dXPvWf1uZy2zjuXyB_CToixrIEfhrK51OZXlMHp8oy4anVybBKmPyntst6mSxLTtKDdADgnSF4ZeMFItohmcovyBq81; _ga=GA1.1.1224430601.1702745675; analytics_token=cec90a4d-6b85-d2ae-b200-65b05af90cd1; _yngt_iframe=1; ASP.NET_SessionId=2zg05g0jhccl2whkxoyus3bf; _yngt=70485ff8-84c57-7272f-f9355-5985bf72cd122; analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; yektanet_session_last_activity=12/20/2023; analytics_session_token=fd34b465-31c2-afc3-cd3d-e15daf5e82cf; _ga_F7SRW3F8BJ=GS1.1.1703094354.8.1.1703097530.0.0.0'
        })
        return site_1
    else:
        print('wrong values entered')


# find the class for number of pages
site = set_url('get', 'https://www.iranketab.ir/tag/512-best-historical-books?page=1')
soup = BeautifulSoup(site.text, 'html.parser')
page_numbers = soup.find_all('ul', attrs={'class': 'pagination'})
pagesub_txt = str(page_numbers)
soup_sub = BeautifulSoup(pagesub_txt, 'html.parser')
list_page_number = soup_sub.find_all('a', url=True)
# put the numbers of page and the link in a dic
for item in range(0, len(list_page_number)):
     temp= [list_page_number[int(item)]['url']][0]
     temp = f'{website}{temp}'
     dic_page_ajax[list_page_number[int(item)]['data-page-no']] = temp
# find the number of last page
long_page = dic_page_ajax.keys().__contains__('»»')
if long_page:
    last_page = dic_page_ajax['»»']
    last_page_number = re.findall(r'pagenumber=(.+)&pagesize', str(last_page))
    max_page = int(last_page_number[0])
else:
    last_page = list(dic_page_ajax)[-1]
    max_page = int(last_page)
# getting the data after we find max page and current page

count = 0
while True:
    if current_page > max_page:
        print("out of the main loop")
        break
    else:
        # take link of details for a book
        link_product = str(soup.find_all('h4', attrs={'class': 'product-name-title'}))
        soup_sub_2 = BeautifulSoup(link_product, 'html.parser')
        link_product = soup_sub_2.find_all('a', href=True)






        for a in link_product:
            if count >= 1:
                break
            # this is where we enter every page to extract the data

            page_url = a['href']
            url_page_book = f'{website}{page_url}'
            #find the data table
            site_details_book = set_url('get', url_page_book)
            soup_details = BeautifulSoup(site_details_book.text , 'html.parser')
            info_table = str(soup_details.find_all('table', attrs={'class' : 'product-table'}))
            # find the "tr" in the table
            soup_details = BeautifulSoup(info_table,'html.parser')
            book_id = soup_details.find_all('td', limit=2)[1].text
            author = soup_details.find_all('span' , attrs={'itemprop':'name'})
            print(author)
            if author!= []:
                if len(author) > 1:
                    print("two author")
                else:
                    print('one author')
            else:
                print('author  empty')

            # for data in info_table:
            #     string1 = str(data['td'])
            #     #.strip().replace('\n' , "")
            #     print(string1 , '\n')

            count +=1








        #print(f'page {current_page}')
        current_page += 1
        if current_page <= max_page:
             site = set_url('post', dic_page_ajax[str(current_page)])
             soup = BeautifulSoup(site.text, 'html.parser')


