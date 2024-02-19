from bs4 import BeautifulSoup
import requests
import re
import time
from fake_http_header import FakeHttpHeader
import mysql.connector
def getdata(url):
    website = 'https://www.iranketab.ir'
    dic_page_ajax = {}
    max_page = 0
    current_page = 1
    list_translater = []
    count_req = 0


    cnx= mysql.connector.connect(user='root', password='AaA123456789@', host='127.0.0.1')
    cursor = cnx.cursor()


    # url section

    # ajax = 'https://www.iranketab.ir/tag/filtertags/437/literature?pagenumber=19&ispager=True&pagesize=20&sortOrder
    # =date_desc&tagid=437' ajax2 = 'https://www.iranketab.ir/tag/97-american-literature?pagenumber=15&pagesize=20
    # &sortOrder=date_desc&tagid=97' 'https://www.iranketab.ir/tag/512-best-historical-books'
    # f'https://www.iranketab.ir/tag/512-best-historical-books?page=1'
    def set_url(state='', url='', header={}):
        if state == 'get':
            base_url = url
            site_1 = requests.get(base_url, headers=header)
            return site_1
        elif state == 'post':
            base_url = url
            site_1 = requests.post(base_url, headers=header)
            return site_1
        else:
            print('wrong values entered')


    # find the class for number of pages
    #https://www.iranketab.ir/tag/512-best-historical-books?page=1
    #'https://www.iranketab.ir/tag/102-romantic-stories'
    #category_url = 'https://www.iranketab.ir/tag/512-best-historical-books?page=1'
    category_url = url
    site = set_url('get', category_url)
    print(site)
    soup = BeautifulSoup(site.text, 'html.parser')
    page_numbers = soup.find_all('ul', attrs={'class': 'pagination'})
    pagesub_txt = str(page_numbers)
    soup_sub = BeautifulSoup(pagesub_txt, 'html.parser')
    list_page_number = soup_sub.find_all('a', url=True)
    # put the numbers of page and the link in a dic
    for item in range(0, len(list_page_number)):
        temp = [list_page_number[int(item)]['url']][0]
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
        # max_page = 1
    # getting the data after we find max page and current page
    end = False
    count = 0

    index_loop = 0
    title_category = soup.find("span", attrs={"class": "brief-header-name"}).text
    title_category = title_category.replace('کتاب های   ', '').strip().lstrip().rstrip()
    title_category = title_category.replace("'" , "")
    print(title_category)
    category_id = 0
    while True:

        if current_page > max_page:
            print("out of the main loop")
            break
        else:
            # take link of details for a book
            link_product = str(soup.find_all('h4', attrs={'class': 'product-name-title'}))
            soup_sub_2 = BeautifulSoup(link_product, 'html.parser')
            link_product = soup_sub_2.find_all('a', href=True)

            cursor.execute("select cat_url from web_data.category where cat_url = '%s' ;" %category_url)
            for a in cursor:
                temp =a[0]

            if temp != category_url:
                cursor = cnx.cursor()
                cursor.execute("insert into web_data.category ( cat_title, cat_url, maxpage_done) ""values ('%s','%s','%s');" % (title_category,category_url,str(max_page)) )
                cnx.commit()
                cursor.execute("select cat_id from web_data.category where cat_url = '%s' ;" % category_url)
                for id in cursor:
                    category_id = id

            else:
                cursor = cnx.cursor()
                cursor.execute("SELECT * FROM web_data.category ORDER BY cat_id DESC LIMIT 1")
                for id in cursor:
                    category_id = id






            count_req = 0
            fake_header = FakeHttpHeader()
            fake_header_dict = fake_header.as_header_dict()
            for a in link_product:
                if count_req == 6:
                    count_req = 0
                    fake_header = FakeHttpHeader()
                    fake_header_dict = fake_header.as_header_dict()
                limit_loop = 2
                index_loop = 0
                end = False
                # this is where we enter every page to extract the data
                page_url = a['href']
                url_page_book = f'{website}{page_url}'
                #url_page_book = "https://www.iranketab.ir/book/2239-tarikh-i-bayhaqi"

                # find the data table
                time.sleep(3)
                site_details_book = set_url('get', url_page_book , fake_header_dict)
                time.sleep(3)
                soup_details = BeautifulSoup(site_details_book.text, 'html.parser')
                info_table = soup_details.find_all('table', attrs={"class": "product-table"})
                # this is where we check if the page have more than one book
                if info_table != []:
                    if len(info_table) <= 1:
                        print(url_page_book)
                        title = str(soup_details.find("h1", attrs={"class": "product-name"}).text)
                        title = title.replace("'" , "")
                        print(title)
                        if soup_details.find("span", attrs={"class": "price price-special"}).text != None:
                            price = soup_details.find("span", attrs={"class": "price price-special"}).text
                            price = price.replace(",", "")
                            price = price.strip()
                            price = int(price)
                            print(price)
                        else:
                            price = soup_details.find("span", attrs={"class": "price"}).text
                            price = price.replace(",", "")
                            price = price.strip()
                            price = int(price)
                            print(price)
                        # find the "tr" in the table and go to a loop to fill data for database
                        info_table = str(info_table)
                        soup_details = BeautifulSoup(info_table, 'html.parser')
                        translater = soup_details.find_all('span', attrs={'itemprop': 'name'})
                        for match in soup_details.find_all('span'):
                            match.replace_with('')
                        while not end:

                            pointer = soup_details.find_all('td', limit=limit_loop)[index_loop - 2].text
                            pointer = pointer.strip().lstrip().rstrip()

                            if pointer == "کد کتاب :":
                                book_id = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                            elif pointer == "مترجم":
                                if translater != []:
                                    if len(translater) > 1:
                                        for trans in translater:
                                            list_translater.append(trans.text)
                                            list_translater.append(">>")
                                        translater = ''.join(list_translater)
                                        print(translater)
                                    else:
                                        translater = translater[0].text
                                        print(translater)
                                else:
                                    print('author  empty')
                            elif pointer == "شابک":
                                shabak1 = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                print(shabak1)
                            elif pointer == "تعداد صفحه":
                                page_count = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                print(page_count)
                            elif pointer == "سال انتشار شمسی":
                                date = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                print(date)
                                print("__________________________________________")
                            elif pointer == "زودترین زمان ارسال":
                                end = True
                            limit_loop += 2

                        cursor.execute("select book_id from web_data.iranketab_books where book_id = '%i';" % int(book_id))
                        for id in cursor:
                            temp = id[0]

                        if temp != int(book_id):

                            cursor.execute("select cat_id from web_data.category where cat_url = '%s';" % category_url)
                            for cat_id in cursor:
                                temp = int(cat_id[0])
                            cursor.execute("insert into web_data.iranketab_books "
                                           "(book_id, book_category_id, book_name, book_shabak, book_pages, book_publish_date,book_price, book_translater, book_group)"
                                           " values ('%s','%i','%s','%s','%i','%i','%i','%s','%s');" %(book_id,temp,title,shabak1,int(page_count),int(date),price,translater,'0'))
                            cnx.commit()

                        count += 1
                        list_translater = []
                        translater = ''
                        count_req += 1
                    else:
                        # pages with multi book should get restricted and search table and price for each element of their own
                        soup_details = soup_details.find('div', attrs={"class": "product-container well clearfix"})
                        books_in_table = len(info_table)
                        list_title_main = []
                        list_price_main = []
                        list_codebook_main = []
                        list_translater_main = []
                        list_translater_check = [0] * books_in_table
                        index_translater_check = 0
                        list_shabak_main = []
                        list_pagecount_main = []
                        list_date_main = []
                        title = str(soup_details.find("h1", attrs={"class": "product-name"}).text.lstrip().rstrip().strip())
                        title = title.replace("'" , "")
                        list_title_main.append(title)
                        title = soup_details.find_all("div", attrs={"class": "product-name"})
                        for t in title:
                            list_title_main.append(t.text.lstrip().rstrip().strip())
                        #code to find prices
                        soup_details = soup_details.find_all('div', attrs={"class": "clearfix"})
                        for clearfix in soup_details:
                                price = clearfix.find_all("span", attrs={"class": "price"})
                                if len(price) == 2:
                                    final_price = price[1].text
                                    final_price = final_price.replace(",", "")
                                    final_price = final_price.strip()
                                    final_price = int(final_price)
                                    list_price_main.append(final_price)
                                elif len(price) == 1:
                                    final_price = price[0].text
                                    final_price = final_price.replace(",", "")
                                    final_price = final_price.strip()
                                    final_price = int(final_price)
                                    list_price_main.append(final_price)

                        for table in info_table:
                            end = False
                            limit_loop = 2
                            index_loop = 0
                            soup_details = BeautifulSoup(str(table), 'html.parser')
                            translater = soup_details.find_all('span', attrs={'itemprop': 'name'})
                            for match in soup_details.find_all('span'):
                                match.replace_with('')
                            while not end:
                                pointer = soup_details.find_all('td', limit=limit_loop)[index_loop - 2].text
                                pointer = pointer.strip().lstrip().rstrip()
                                if pointer == "کد کتاب :":
                                    book_id = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                    list_codebook_main.append(book_id)
                                elif pointer == "مترجم":
                                    if translater != []:
                                        if len(translater) > 1:
                                            for trans in translater:
                                                list_translater.append(trans.text)
                                                list_translater.append(">>")
                                            translater = ''.join(list_translater)
                                            list_translater_main.append(translater)
                                            list_translater_check[index_translater_check] = 1
                                            index_translater_check +=1
                                        else:
                                            translater = translater[0].text
                                            list_translater_main.append(translater)
                                            list_translater_check[index_translater_check] = 1
                                            index_translater_check += 1
                                    else:
                                       list_translater_main.append('')

                                elif pointer == "شابک":
                                    shabak1 = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                    list_shabak_main.append(shabak1)
                                elif pointer == "تعداد صفحه":
                                    page_count = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                    list_pagecount_main.append(page_count)
                                elif pointer == "سال انتشار شمسی":
                                    date = soup_details.find_all('td', limit=limit_loop)[index_loop - 1].text
                                    list_date_main.append(date)

                                elif pointer == "زودترین زمان ارسال":
                                    end = True
                                limit_loop += 2

                        print(list_translater_main)
                        for item in range(0 , len(list_translater_check)):
                            if list_translater_check[item] == 0:
                                list_translater_main.insert(item, " ")
                        print(list_translater_main)

                        for index in range(0,len(list_title_main)):
                            print(f" سری کتاب ،{list_title_main[0]}")
                            print(list_title_main[index] )
                            print(list_price_main[index])
                            print(list_codebook_main[index])
                            if len(list_translater_main) == len(info_table):
                                print(list_translater_main[index])
                            print(list_shabak_main[index])
                            print(list_pagecount_main[index])
                            print(list_date_main[index])
                            print("__________________________________________")

                            cursor.execute("select book_id from web_data.iranketab_books where book_id = '%i';" % int(list_codebook_main[index]))
                            for id in cursor:
                                temp = id[0]

                            if temp != int(list_codebook_main[index]):

                                cursor.execute("select cat_id from web_data.category where cat_url = '%s';" % category_url)
                                for cat_id in cursor:
                                    temp = int(cat_id[0])
                                cursor.execute("insert into web_data.iranketab_books (book_id, book_category_id, book_name, book_shabak, book_pages, book_publish_date,book_price, book_translater, book_group)"
                                               " values ('%s','%i','%s','%s','%i','%i','%i','%s','%s');"
                                               %(list_codebook_main[index],temp,list_title_main[index],list_shabak_main[index],int(list_pagecount_main[index]),int(list_date_main[index]),list_price_main[index],list_translater_main[index],list_codebook_main[0]))
                                cnx.commit()

                            list_translater = []
                            translater = ''
                            count_req += 1

                        print('more than one book in page')
                        count += 1
                else:
                    print(site_details_book.text)
                    print("page content not found")
            current_page += 1
            if current_page <= max_page:
                print("entered next page ")
                site = set_url('post', dic_page_ajax[str(current_page)] , fake_header_dict)
                print(site.text)
                soup = BeautifulSoup(site.text, 'html.parser')
    cursor.close()
    cnx.close()
