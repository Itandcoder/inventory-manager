from tkinter import *
from tkinter import ttk
import sqlite3
import re
import csv
from tkinter import filedialog



# Create or connect to database
conn = sqlite3.connect('database.db')
c = conn.cursor()
conn.commit()

# Create tables  
try:
    c.execute("""CREATE TABLE inventory (
            label text NOT NULL PRIMARY KEY,
            item text,
            brand text,
            model text,
            serial text,
            invoice text,
            supply text,
            purchase_date text,
            receive_date text,
            user text
            )""")
    conn.commit()
except Exception:
    print("Table exist.")

# Create application window
window = Tk()
window.geometry("860x980+100+2")
window.title("Elintcode Inventory Manager")
window.configure(bg="#107DAC")


# Full Inventory #########################################################################################################
def tree_table(setwindow, x, y, inputdata, color_one, color_two):
    global tree
    tree_frame = Frame(setwindow)
    tree_frame.place(x=x, y=y)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=38)
    tree_scroll.config(command=tree.yview)
    tree['columns'] = ("LABEL", "ITEM", "BRAND", "MODEL", "SERIAL")
    tree.column("#0", width=0, stretch=NO)
    tree.column("LABEL", anchor=CENTER, width=100, minwidth=15)
    tree.column("ITEM", anchor=CENTER, width=200, minwidth=25)
    tree.column("BRAND", anchor=CENTER, width=200, minwidth=25)
    tree.column("MODEL", anchor=CENTER, width=150, minwidth=25)
    tree.column("SERIAL", anchor=CENTER, width=150, minwidth=25)
    tree.heading("#0", text="Label", anchor=W)
    tree.heading("LABEL", text="LABEL", anchor=CENTER)
    tree.heading("ITEM", text="ITEM", anchor=CENTER)
    tree.heading("BRAND", text="BRAND", anchor=CENTER)
    tree.heading("MODEL", text="MODEL", anchor=CENTER)
    tree.heading("SERIAL", text="SERIAL", anchor=CENTER)
    tree.tag_configure('oddrow', background=color_one)
    tree.tag_configure('evenrow', background=color_two)
    count = 1
    for i in inputdata:
        if count % 2 == 0:
            tree.insert(parent='', index='end', text="", values=(i[0], i[1], i[2], i[3], i[4]), tags=("oddrow"))
        else:
            tree.insert(parent='', index='end', text="", values=(i[0], i[1], i[2], i[3], i[4]), tags=("evenrow"))
            tree.pack(pady=20)
        count += 1

# Inventory table function
def inventory_list():
    global inputdata
    setwindow = window
    x = 20
    y = 130
    color_one = "lightgray"
    color_two = "lightblue"
    c.execute("SELECT * FROM inventory")
    inputdata = c.fetchall()
    conn.commit()
    inputdata.sort()
    tree_table(setwindow, x, y, inputdata, color_one, color_two)

# Buttons
btn = Button(window, text="FULL INVENTORY", command= inventory_list)
btn.place(height=22 ,x=266, y=20)


# EXPORT FULL INVENTORY TO CSV ################################################################################################
def export_inventory_csv():
    file_name = filedialog.asksaveasfilename(initialdir="/Users", title="Elintcode - Save File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if file_name:
        file_name = file_name + '.csv'
        with open(file_name, 'a', newline="") as f:
            w = csv.writer(f, dialect='excel')
            for row in inputdata:
                w.writerow(row)
            f.close()

# Buttons
btn = Button(window, text="FULL EXPORT CSV", command= export_inventory_csv)
btn.place(height=22 ,x=157, y=20)


# INVENTORY RECEIVING AREA ####################################################################################################
def inventory_receiving():
    # Get CSV file
    inputdata = []
    csvfile = filedialog.askopenfile(initialdir="/Users", title="Elintcode - Search File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            inputdata.append(row)

        # Create application window
        window_receiving = Tk()
        window_receiving.geometry("1050x900+50+50")
        window_receiving.title("Elintcode Inventory Receiving")
        window_receiving.configure(bg="#107DAC")

        frame = LabelFrame(window_receiving, text="Invoice Info.", padx=5, pady=5)
        frame.place(x=810, y=100)

        # Entry labels and cells
        invoice_label = Label(frame, text="INVOICE NUMBER     ")
        invoice_label.pack()
        invoice = Entry(frame, width=30, borderwidth=2)
        invoice.pack()

        supply_label = Label(frame, text="SUPPLY NAME        ")
        supply_label.pack()
        supply = Entry(frame, width=30, borderwidth=2)
        supply.pack()

        purchase_date_label = Label(frame, text="INVOICE DATE        ")
        purchase_date_label.pack()
        purchase_date = Entry(frame, width=30, borderwidth=2)
        purchase_date.pack()

        received_date_label = Label(frame, text="RECEIVED DATE       ")
        received_date_label.pack()
        receive_date = Entry(frame, width=30, borderwidth=2)
        receive_date.pack()

        user_label = Label(frame, text="EMPLOYEE NAME     ")
        user_label.pack() 
        user = Entry(frame, width=30, borderwidth=2)
        user.pack()


        # Table parameters
        x = 20
        y = 20
        color_one = "lightgray"
        color_two = "lightblue"
        # Create table
        tree_frame = Frame(window_receiving)
        tree_frame.place(x=x, y=y)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=40)
        tree_scroll.config(command=tree.yview)
        tree['columns'] = ("LABEL", "ITEM", "BRAND", "MODEL", "SERIAL")
        tree.column("#0", width=0, stretch=NO)
        tree.column("LABEL", anchor=CENTER, width=100, minwidth=15)
        tree.column("ITEM", anchor=CENTER, width=200, minwidth=25)
        tree.column("BRAND", anchor=CENTER, width=150, minwidth=25)
        tree.column("MODEL", anchor=CENTER, width=150, minwidth=25)
        tree.column("SERIAL", anchor=CENTER, width=150, minwidth=25)
        tree.heading("#0", text="Label", anchor=W)
        tree.heading("LABEL", text="LABEL", anchor=CENTER)
        tree.heading("ITEM", text="ITEM", anchor=CENTER)
        tree.heading("BRAND", text="BRAND", anchor=CENTER)
        tree.heading("MODEL", text="MODEL", anchor=CENTER)
        tree.heading("SERIAL", text="SERIAL", anchor=CENTER)
        tree.tag_configure('oddrow', background=color_one)
        tree.tag_configure('evenrow', background=color_two)
        count = 1
        for i in inputdata:
            if count % 2 == 0:
                tree.insert(parent='', index='end', text="", values=(i[0], i[1], i[2], i[3], i[4]), tags=("oddrow"))
            else:
                tree.insert(parent='', index='end', text="", values=(i[0], i[1], i[2], i[3], i[4]), tags=("evenrow"))
                tree.pack(pady=20)
            count += 1

        def save_data():
            # Create or connect to database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            conn.commit()
            try:
                for row in inputdata:  
                    label = row[0].upper()
                    item = row[1].upper()
                    brand = row[2].upper()
                    model = row[3].upper()
                    serial = row[4].upper()
                    # Get Entry cells data
                    invoice_input = invoice.get().upper()
                    supply_input = supply.get().upper()
                    purchase_date_input = purchase_date.get().upper()
                    receive_date_input = receive_date.get().upper()
                    user_input = user.get().upper()
                    c.execute("INSERT INTO inventory VALUES (:label, :item, :brand, :model, :serial, :invoice, :supply, :purchase_date, :receive_date, :user)",
                                {
                            "label": label,
                            "item": item,
                            "brand": brand,
                            "model": model,
                            "serial": serial, 
                            "invoice": invoice_input,
                            "supply": supply_input,
                            "purchase_date": purchase_date_input,
                            "receive_date": receive_date_input,
                            "user": user_input
                            })
                conn.commit()
                window_receiving.destroy()
                notification_window= Tk()
                notification_window.configure(bg="#107DAC")
                notification_window.title("Notification")
                notification_window.geometry("200x150+720+200")
                titulo = Label(notification_window, text="Received.")
                titulo.pack(pady=20)
                btn = Button(notification_window, text="Ok", command= notification_window.destroy)
                btn.pack(pady=15)
                inventory_list()
            except Exception:
                notification_window= Tk()
                notification_window.configure(bg="#107DAC")
                notification_window.title("Notification")
                notification_window.geometry("200x150+720+200")
                titulo = Label(notification_window, text="Label already exist.")
                titulo.pack(pady=20)
                btn = Button(notification_window, text="Ok", command= notification_window.destroy)
                btn.pack(pady=15)
            conn.close()

        # Buttons
        btn = Button(window_receiving, text="SAVE RECEIVING", command= save_data)
        btn.place(height=22 ,x=865, y=370)
        

        window_receiving.mainloop()

btn = Button(window, text="INVENTORY RECEIVING", command= inventory_receiving)
btn.place(height=22 ,x=20, y=20)

# SEARCH AREA ###############################################################################################################

# Entry cells
clicked = StringVar()
clicked.set("   LABEL   ")
drop = OptionMenu(window, clicked, "   LABEL   ", "   ITEM   ", "   BRAND   ", "   MODEL   ", "   SERIAL   ")
drop.place(height=21, x=601, y=20)

search_query = Entry(window,width=30, borderwidth=2, font='Arial 10')
search_query.place(height=22, x=385, y=19)


def search_list():
    global search_output
    # Query
    selection = clicked.get()
    search_item = search_query.get().upper()
    search_output = []

    # Get data from table in database
    c.execute("SELECT * FROM inventory")
    inventory_table = c.fetchall()
    conn.commit()

    # Label Search
    if selection == "   LABEL   ":
        for i in inventory_table:
            if bool(re.search(search_item, i[0])):
                get_item = i[0]
                c.execute("SELECT * FROM inventory WHERE label = :label",
                        {
                        'label':get_item
                        })
                label_row = c.fetchone()
                conn.commit()
                search_output.append(label_row)
    # Item Search
    elif selection == "   ITEM   ":
        for i in inventory_table:
            if bool(re.search(search_item, i[1])):
                get_item = i[1]
                c.execute("SELECT * FROM inventory WHERE item = :item",
                        {
                        'item':get_item
                        })
                item_row = c.fetchone()
                conn.commit()
                search_output.append(item_row)
    # Brand Search
    elif selection == "   BRAND   ":
        for i in inventory_table:
            if bool(re.search(search_item, i[2])):
                get_item = i[2]
                c.execute("SELECT * FROM inventory WHERE brand = :brand",
                        {
                        'brand':get_item
                        })
                brand_row = c.fetchone()
                conn.commit()
                search_output.append(brand_row)
    # Model Search
    elif selection == "   MODEL   ":
        for i in inventory_table:
            if bool(re.search(search_item, i[3])):
                get_item = i[3]
                c.execute("SELECT * FROM inventory WHERE model = :model",
                        {
                        'model':get_item
                        })
                model_row = c.fetchone()
                conn.commit()
                search_output.append(model_row)
    # Serial Search
    elif selection == "   SERIAL   ":
        for i in inventory_table:
            if bool(re.search(search_item, i[4])):
                get_item = i[4]
                c.execute("SELECT * FROM inventory WHERE serial = :serial",
                        {
                        'serial':get_item
                        })
                serial_row = c.fetchone()
                conn.commit()
                search_output.append(serial_row)

    # Inventory table function
    setwindow = window
    x = 20
    y = 130
    color_one = "lightgray"
    color_two = "lightblue"
    tree_table(setwindow, x, y, search_output, color_one, color_two)

    search_query.delete(0, END)

btn = Button(window, text="SEARCH", command= search_list)
btn.place(height=22 ,x=701, y=20)


# EXPORT SEARCH TO CSV ###################################################################################################
def export_search_csv():
    file_name = filedialog.asksaveasfilename(initialdir="/Users", title="Elintcode - Save File", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if file_name:
        file_name = file_name + '.csv'
        with open(file_name, 'a', newline="") as f:
            w = csv.writer(f, dialect='excel')
            for row in search_output:
                w.writerow(row)
            f.close()

# Buttons
btn = Button(window, text="SEARCH CSV", command= export_search_csv)
btn.place(height=22 ,x=759, y=20)


# MODIFY INVENTORY AREA ##################################################################################################
label_box = Entry(window, width=15, borderwidth=2, font='Arial 10')
label_box.place(height=21, x=20, y=100)
item_box = Entry(window, width=27, borderwidth=2, font='Arial 10')
item_box.place(height=21, x=135, y=100)
brand_box = Entry(window, width=27, borderwidth=2, font='Arial 10')
brand_box.place(height=21, x=334, y=100)
model_box = Entry(window, width=20, borderwidth=2, font='Arial 10')
model_box.place(height=21, x=533, y=100)
serial_box = Entry(window, width=20, borderwidth=2, font='Arial 10')
serial_box.place(height=21, x=683, y=100)


def add_item():
    try:
        label = label_box.get().upper()
        item = item_box.get().upper()
        brand = brand_box.get().upper()
        model = model_box.get().upper()
        serial = serial_box.get().upper()
        invoice_input = "N/A"
        supply_input = "N/A"
        purchase_date_input = "N/A"
        receive_date_input = "N/A"
        user_input = "N/A"
        c.execute("INSERT INTO inventory VALUES (:label, :item, :brand, :model, :serial, :invoice, :supply, :purchase_date, :receive_date, :user)",
                    {
                "label": label,
                "item": item,
                "brand": brand,
                "model": model,
                "serial": serial,
                "invoice": invoice_input,
                "supply": supply_input,
                "purchase_date": purchase_date_input,
                "receive_date": receive_date_input,
                "user": user_input
                })
        conn.commit()
    except Exception:
        notification_window= Tk()
        notification_window.configure(bg="#107DAC")
        notification_window.title("Notification")
        notification_window.geometry("200x150+720+200")
        titulo = Label(notification_window, text="Label already exist.")
        titulo.pack(pady=20)
        btn = Button(notification_window, text="Ok", command= notification_window.destroy)
        btn.pack(pady=15)
    label_box.delete(0, END)
    item_box.delete(0, END)
    brand_box.delete(0, END)
    model_box.delete(0, END)
    serial_box.delete(0, END)
    inventory_list()


def select_item():
    label_box.delete(0, END)
    item_box.delete(0, END)
    brand_box.delete(0, END)
    model_box.delete(0, END)
    serial_box.delete(0, END)
    selected = tree.focus()
    values = tree.item(selected, 'values')
    label_box.insert(0, values[0])
    item_box.insert(0, values[1])
    brand_box.insert(0, values[2])
    model_box.insert(0, values[3])
    serial_box.insert(0, values[4])


def update_item():
    selected = tree.focus()
    tree.item(selected, text="", values=(label_box.get(), item_box.get(), brand_box.get(), model_box.get(), serial_box.get()))
    c.execute("""UPDATE inventory SET
        label = :label,
        item = :item,
        brand = :brand,
        model = :model,
        serial = :serial
        WHERE label = :label""",
        {
            'label': label_box.get().upper(),
            'item': item_box.get().upper(),
            'brand': brand_box.get().upper(),
            'model': model_box.get().upper(),
            'serial': serial_box.get().upper()
        })
    label_box.delete(0, END)
    item_box.delete(0, END)
    brand_box.delete(0, END)
    model_box.delete(0, END)
    serial_box.delete(0, END)
    inventory_list()


def remove_item():
    notification_window= Tk()
    notification_window.configure(bg="#107DAC")
    notification_window.title("Notification")
    notification_window.geometry("200x150+720+200")
    titulo = Label(notification_window, text="Remove permanently?")
    titulo.pack(pady=20)
    def proceed():
        try:
            label = label_box.get()
            c.execute("DELETE FROM inventory WHERE label = :label",
                {
                    "label" :label
                })
            conn.commit()
        except Exception:
            notification_window= Tk()
            notification_window.configure(bg="#107DAC")
            notification_window.title("Notification")
            notification_window.geometry("200x150+720+200")
            titulo = Label(notification_window, text="Label already exist.")
            titulo.pack(pady=20)
            btn = Button(notification_window, text="Ok", command= notification_window.destroy)
            btn.pack(pady=15)
        label_box.delete(0, END)
        item_box.delete(0, END)
        brand_box.delete(0, END)
        model_box.delete(0, END)
        serial_box.delete(0, END)
        inventory_list()

    btn = Button(notification_window, text="Ok", command= proceed)
    btn.pack(pady=15)


btn = Button(window, text="SELECT", command= select_item)
btn.place(height=22 ,width= 70 ,x=230, y=70)
btn = Button(window, text="UPDATE", command= update_item)
btn.place(height=22 ,width= 70 ,x=340, y=70)
btn = Button(window, text="REMOVE", command= remove_item)
btn.place(height=22 ,width= 70 ,x=450, y=70)
btn = Button(window, text="ADD", command= add_item)
btn.place(height=22 ,width= 70 ,x=560, y=70)


# MAIN FOOTER #########################################################################################################
# Call Inventory list
inventory_list()

window.mainloop()
conn.close()