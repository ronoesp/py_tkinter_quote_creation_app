import tkinter
from tkcalendar import Calendar, DateEntry
from tkinter import ttk

class TestTkcalender(tkinter.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.master.title("tkカレンダーテスト")
        self.master.geometry("800x600")

        self.data_entry_date = DateEntry()
        self.data_entry_date.place(x=250, y=230)

        # self.calender_date = Calendar()
        # self.calender_date.place(x=500, y=230)

def main():
    root = tkinter.Tk()
    root = TestTkcalender(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()