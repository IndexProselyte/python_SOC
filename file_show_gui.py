import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Treeview demo')
root.geometry('620x200')

# define columns
columns = ('first_name', 'last_name', 'email')

tree = ttk.Treeview(root, columns=columns, show='headings')

# define headings
tree.heading('first_name', text='First Name')
tree.heading('last_name', text='Last Name')
tree.heading('email', text='Email')


# add data to the treeview

with open("Data/output.txt", "r", encoding="utf-8") as file:
    for line in file:
        tree.insert('', tk.END, values=)


def item_selected(event): 
    print(tree.selection()) #   Why wont it return a tuple



tree.bind('<<TreeviewSelect>>', item_selected) # WE CAN DETECT TOUCH

tree.grid(row=0, column=0, sticky='nsew')

# add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# run the app
root.mainloop()