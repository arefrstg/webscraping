import tkinter as tk
def final_text(text = "", Errorcode=""):
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.attributes('-topmost', True)
    root = tk.Tk()
    root.title("صفحه نهایی")
    window_width = 700
    window_height = 600
    center_window(root, window_width, window_height)
    label = tk.Label(root, text=text)
    label.pack()
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    label2 = tk.Label(root, text=Errorcode)
    label2.pack()
    label2.place(relx=0.6, rely=0.6, anchor=tk.CENTER)
    root.mainloop()




