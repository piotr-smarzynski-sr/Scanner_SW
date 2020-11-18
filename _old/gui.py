import tkinter as tk
from threads import gui_queue
from threads import PROTOCOL_NO, PROTOCOL_VERSION, TIMESTAMP, STATUS, CONF_SIGNATURE, RESERVED

class Application(tk.Frame):
    def __init__(self, queue_input, master=None):
        super().__init__(master)
        self.master = master
        self.gui_q = queue_input
        
        self.pack()
        self.create_widgets()        
        self.update_labels()

    def create_widgets(self):
        self.line_no_name = tk.Label(self, text="Line number", font=("Arial", 24), justify='left', width=20)
        self.line_no_name.grid(row=0, column=0)

        self.line_no = tk.Label(self, text="", font=("Arial", 24))
        self.line_no.grid(row=0, column=1)
        # self.line_no.pack(side=tk.LEFT)

        self.line_text_name = tk.Label(self, text="Line text", font=("Arial", 24), justify='left', width=20)
        self.line_text_name.grid(row=1, column=0)

        self.line_text = tk.Label(self, text="", font=("Arial", 24))
        self.line_text.grid(row=1, column=1)
        # self.line_text.pack(side=tk.LEFT)

        self.message_name = tk.Label(self, text="Message", font=("Arial", 24), justify='left', width=20)
        self.message_name.grid(row=2, column=0)
        self.message = tk.Label(self, text="", font=("Arial", 24))
        self.message.grid(row=2, column=1)
        # self.message.pack(side=tk.BOTTOM)
        # self.line_no.pack()

    def update_labels(self):
        if self.gui_q.empty() is False:
            element = self.gui_q.get()
            print('element: ', element)
            now = 'A'
            self.line_no.configure(text=element[5])
            if element[1].endswith('\n'):
                self.line_text.configure(text=element[1][:-2])
            else:
                self.line_text.configure(text=element[1])
            self.message.configure(text=now)

        self.after(50, self.update_labels)



def gui(queue_input):
    root = tk.Tk()
    root.geometry("400x500")
    app = Application(master=root, queue_input=queue_input)
    app.mainloop()
    # while True:
    #     if queue_input.empty() is False:
    #         element = queue_input.get()
    #         print(element)

# import tkinter as tk