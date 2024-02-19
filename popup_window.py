import tkinter as tk

repeat = True
def main():

    def check_text_length(event):
        text = entry.get()
        if len(text) == 2:
            print(text)
            entry.delete(0 , 2)
            root.destroy()
            repeat = False
            return text
              # Close the window when two digits are entered

    # Create the main window
    root = tk.Tk()
    root.title("اخطار")

    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size
    window_width = 200
    window_height = 100

    # Calculate the coordinates for the top-right corner
    x_position = screen_width - window_width
    y_position = 0

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a label
    label = tk.Label(root, text="جواب کپچا")
    label.pack()

    # Create a textbox (Entry widget)
    entry = tk.Entry(root)
    entry.pack()
    entry.focus_set()

    # Bind the event to the entry widget
    entry.bind('<KeyRelease>', check_text_length)

    # Run the Tkinter event loop

    while repeat == True:
        root.mainloop()
def final_text(text = "", Errorcode=""):
    def center_window(window, width, height):
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the position for the window to be centered
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window position
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.attributes('-topmost', True)
    # Create the main window
    root = tk.Tk()
    root.title("صفحه نهایی")

    # Calculate the screen width and height


    # Set the window size
    window_width = 700
    window_height = 600

    # Calculate the coordinates for the top-right corner
    center_window(root, window_width, window_height)

    # Create a label
    label = tk.Label(root, text=text)
    label.pack()
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    label2 = tk.Label(root, text=Errorcode)
    label2.pack()
    label2.place(relx=0.6, rely=0.6, anchor=tk.CENTER)



    # Run the Tkinter event loop
    root.mainloop()




