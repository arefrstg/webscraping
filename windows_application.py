import tkinter as tk
from tkinter import ttk
import mysql.connector
import popup_window
import scrap_iranketab
import time


def show_data():
    data = []

    temptuple = ()
    cnx = mysql.connector.connect(user='root', password='AaA123456789@', host='127.0.0.1')
    cursor = cnx.cursor()
    cursor2 = cnx.cursor()
    query = " SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id;"
    cursor.execute("USE web_data;")
    cursor.execute(query)

    for cat_title, book_id, book_cat_id, name, shabak, pages, date, price, tran, book_group, extra in cursor:
        name = str(name).lstrip().rstrip().strip()
        shabak = str(shabak).lstrip().rstrip().strip()
        pages = str(pages).lstrip().rstrip().strip()
        date = str(date).lstrip().rstrip().strip()
        if len(tran) < 1 or tran == "[]" or tran == " ":
            tran = "-"
        temptuple = (cat_title, name, shabak, pages, date, price, tran)
        data.append(temptuple)
        temptuple = ()

    for row in tree.get_children():
        tree.delete(row)

    for row_data in data:
        tree.insert("", "end", values=row_data)
def filter_data(selected_option_price, selected_option_page, selected_option_year):
    if selected_option_price[0] == "بدون فیلتر" and selected_option_page[0] == "بدون فیلتر" and selected_option_year[0] == "بدون فیلتر":
        popup_window.final_text("لطفا فیلتر ها را انتخاب و دوباره دکمه فیلتر را بزنید ")
    else:

        data = []
        temptuple = ()
        cnx = mysql.connector.connect(user='root', password='AaA123456789@', host='127.0.0.1')
        cursor = cnx.cursor()

        if selected_option_price[0] != "بدون فیلتر":
            selected_option_price[1] = int(selected_option_price[1])
            query = f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id where book_price{selected_option_price[0]} {selected_option_price[1]} ;"
        if selected_option_page[0] != "بدون فیلتر":
            selected_option_page[1] = int(selected_option_page[1])
            query = f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id where book_pages{selected_option_page[0]} {selected_option_page[1]} ;"

        if selected_option_year[0] != "بدون فیلتر":
            selected_option_year[1] = int(selected_option_year[1])

            query = f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id where book_publish_date{selected_option_year[0]} {selected_option_year[1]} ;"
            print(query)

        if selected_option_price[0] != "بدون فیلتر" and selected_option_page[0] != "بدون فیلتر":
            query = (f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id "
                     f"where book_price{selected_option_price[0]} {selected_option_price[1]} and book_pages{selected_option_page[0]} {selected_option_page[1]} ;")
        if selected_option_price[0] != "بدون فیلتر" and selected_option_year[0] != "بدون فیلتر":
            query = (f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id where"
                     f" book_price{selected_option_price[0]} {selected_option_price[1]} and book_publish_date{selected_option_year[0]} {selected_option_year[1]} ;")

        if selected_option_page[0] != "بدون فیلتر" and selected_option_year[0] != "بدون فیلتر":
            query = (f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id "
                     f"where book_pages{selected_option_page[0]} {selected_option_page[1]} and book_publish_date{selected_option_year[0]} {selected_option_year[1]} ;")
        if selected_option_price[0] != "بدون فیلتر"  and selected_option_page[0] != "بدون فیلتر" and selected_option_year[0] != "بدون فیلتر":
            query = (f" SELECT c.cat_title, b.* FROM category c JOIN iranketab_books b ON c.cat_id = b.book_category_id where book_price{selected_option_price[0]} {selected_option_price[1]} "
                     f"and book_pages{selected_option_page[0]} {selected_option_page[1]} and book_publish_date{selected_option_year[0]} {selected_option_year[1]} ;")
        cursor.execute("USE web_data;")
        print(query)
        cursor.execute(query)
        for cat_title, book_id, book_cat_id, name, shabak, pages, date, price, tran, book_group, extra in cursor:
            name = str(name).lstrip().rstrip().strip()
            shabak = str(shabak).lstrip().rstrip().strip()
            pages = str(pages).lstrip().rstrip().strip()
            date = str(date).lstrip().rstrip().strip()
            if len(tran) < 1 or tran == "[]" or tran == " ":
                tran = "-"
            temptuple = (cat_title, name, shabak, pages, date, price, tran)
            data.append(temptuple)
            temptuple = ()

        for row in tree.get_children():
            tree.delete(row)

        for row_data in data:
            tree.insert("", "end", values=row_data)
def add_data():

    progress_window = tk.Toplevel(root)
    progress_window.title("صفحه اضافه کردن اطلاعات")


    url_label = tk.Label(progress_window, text="URL:")
    url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    url_label2 = tk.Label(progress_window, text="لینک دسته بندی مد نظر را وارد کنید ")
    url_label2.grid(row=3, column=1, padx=5, pady=5, sticky="w")


    url_entry = tk.Entry(progress_window)
    url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")



    start_button = tk.Button(progress_window, text="شروع", command=lambda: start_progress(url_entry.get()))

    start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    def start_progress(url_entry):
        url_label2.config(text="بعد از کلیک بر روی شروع منتظر بمانید")
        try:
            scrap_iranketab.getdata(url_entry)
        except:
            popup_window.final_text("لطغا از درستی لینک اطمینان حاصل فرمایید ")
        url_label2.config(text="اطلاعات با موفقیت وارد شد ")
def open_price_window():
    price_window = tk.Toplevel(root)
    price_window.title("صفحه فیلتر")

    price_label = tk.Label(price_window, text="قیمت")
    price_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    page_label = tk.Label(price_window, text="تعداد صفحه")
    page_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    page_label = tk.Label(price_window, text="سال انتشار")
    page_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    selected_option_price = tk.StringVar()
    selected_option_price.set("بدون فیلتر")
    dropdown_menu_price = tk.OptionMenu(price_window, selected_option_price, "<", ">", "=", "بدون فیلتر")
    dropdown_menu_price.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    selected_option_page = tk.StringVar()
    selected_option_page.set("بدون فیلتر")
    dropdown_menu_page = tk.OptionMenu(price_window, selected_option_page, "<", ">", "=", "بدون فیلتر")
    dropdown_menu_page.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    selected_option_year = tk.StringVar()
    selected_option_year.set("بدون فیلتر")
    dropdown_menu_year = tk.OptionMenu(price_window, selected_option_year, "<", ">", "=", "بدون فیلتر")
    dropdown_menu_year.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    vcmd = price_window.register(validate_input)
    price_entry = tk.Entry(price_window, validate="key", validatecommand=(vcmd, "%P"))
    price_entry.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky="we")

    page_entry = tk.Entry(price_window, validate="key", validatecommand=(vcmd, "%P"))
    page_entry.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="we")

    year_entry_page = tk.Entry(price_window, validate="key", validatecommand=(vcmd, "%P"))
    year_entry_page.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="we")

    filter_button = tk.Button(price_window, text="نمایش فیلتر",
                              command=lambda: filter_data([selected_option_price.get(), price_entry.get()]
                                                          , [selected_option_page.get(), page_entry.get()]
                                                          , [selected_option_year.get(), year_entry_page.get()]))
    filter_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
def validate_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False


root = tk.Tk()
root.title("صفحه اصلی")

tree = ttk.Treeview(root, columns=("cat_title", "name", "shabak", "page_count", "date", "price", "translator"),
                    show="headings", height=20)

tree.heading("cat_title", text="عنوان دسته بندی")
tree.heading("name", text="نام کتاب")
tree.heading("shabak", text="شابک")
tree.column("shabak", width=100)
tree.heading("date", text="تاریخ انتشار")
tree.column("date", width=40)
tree.heading("page_count", text="تعداد صفحه")
tree.column("page_count", width=40)

tree.heading("price", text="قیمت")
tree.column("price", width=80)
tree.heading("translator", text="مترجم")

show_data_button = tk.Button(root, text="نمایش اطلاعات", command=show_data)
show_data_button.grid(row=4, column=0, pady=5)

add_data_button = tk.Button(root, text="اضافه کردن دسته بندی", command=add_data)
add_data_button.grid(row=2, column=0, pady=5)



filter_data_button = tk.Button(root, text="فیلتر", command=open_price_window)
filter_data_button.grid(row=1, column=0, pady=5)

root.grid_rowconfigure(1, minsize=20)

tree.grid(row=3, column=0, sticky="nsew")

root.mainloop()
