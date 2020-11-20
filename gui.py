from functools import partial
import tkinter as tk
from threads import gui_queue
from threads import PROTOCOL_NO, PROTOCOL_VERSION, TIMESTAMP, STATUS, CONF_SIGNATURE, RESERVED

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Robot communication GUI')
        self.geometry('1000x320')
        self.gui_q = gui_queue

        row = 0
        self.label_line_no_name = tk.Label(self, text="Linia", font=("Arial", 25))
        self.label_line_no_name.grid(column=0, row=row)

        self.label_line_no = tk.Label(self, text="", justify='right', font=("Arial", 25), foreground='blue')
        self.label_line_no.grid(column=1, row=0, sticky=tk.E)

        self.label_text_name = tk.Label(self, text="Panel", font=("Arial", 25))
        self.label_text_name.grid(column=2, row=row)

        self.label_text = tk.Label(self, text="", justify='right', font=("Arial", 25), foreground='blue')
        self.label_text.grid(column=3, row=row, sticky=tk.E)

        row += 6
        self.label_message_name = tk.Label(self, text="UDP", font=("Arial", 25))
        self.label_message_name.grid(column=0, row=row)

        self.label_message = tk.Label(self, text="", justify='right', font=("Arial", 25), foreground='blue')
        self.label_message.grid(column=1, row=row, columnspan=4, sticky=tk.W)
        
        col_count, row_count = self.grid_size()

        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=150)

        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=25)

        self.update_labels()

    def update_labels(self):
        if self.gui_q.empty() is False:
            element = self.gui_q.get()
            print('element: ', element)
            message = str(PROTOCOL_NO) +' '+ str(PROTOCOL_VERSION) +' '+ str(element[2]) +' '+ str(element[3][0]) +'.'+ str(element[3][1]) +'.'+  str(element[3][2]) +'.'+  str(element[3][3]) +' '+  str(element[4]) +' '+ str(TIMESTAMP) +' '+ str(STATUS) +' '+ str(CONF_SIGNATURE) +' '+ str(RESERVED) +' '+ str(element[5]) +' '+ str(element[6]) +' '+ str(element[7]) +' ' 

            self.label_line_no.configure(text=element[5])
            if element[1].endswith('\n'):
                if element[1] == '\n':
                    self.label_text.configure(text='BRAK PANELU - PUSTY OPIS', background='red')
                else:
                    self.label_text.configure(text=element[1][:-2], background='lightgray')
            else:
                if element[1] == 'NOT_FOUND' or element[1] == '':
                    self.label_text.configure(text='BRAK PANELU - BRAK WPISU', background='red')

            self.label_message.configure(text=message)

        self.after(50, self.update_labels)

def gui():
    app = SampleApp()
    app.mainloop()