import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import tkinter.simpledialog as simpledialog
from tkinter import ttk
import sqlite3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import email.mime.message as msg
from email.mime.multipart import MIMEMultipart
import datetime as dt
def destroy():
  root.destroy()

def open_user():
  destroy()
  user_main() 


def user_main():
    #this is the main user window
    root = Tk()
    root.title("Book Worms")
    root.geometry("1000x500")
    root.configure(bg='grey26')
    style = ttk.Style()

    style.theme_use("default")

    style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    style.map("Treeview",
        background=[("selected", "#347083")])

    tree_frame = Frame(root)
    tree_frame.pack(pady=10)



    # this is scrollbar
    tree_scroll= Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack()

    tree_scroll.config(command=my_tree.yview)

    my_tree["columns"] = ("Book's Name","Author's Name","ISBN-10","ISBN-13","Availability")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Book's Name", anchor=W, width=140)
    my_tree.column("Author's Name", anchor=W, width=140)
    my_tree.column("ISBN-10", anchor=CENTER, width=140)
    my_tree.column("ISBN-13", anchor=CENTER, width=140)
    my_tree.column("Availability", anchor=CENTER, width=140)

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("Book's Name", text="Book's Name", anchor=W)
    my_tree.heading("Author's Name", text="Author's Name", anchor=W)
    my_tree.heading("ISBN-10", text="ISBN-10", anchor=CENTER)
    my_tree.heading("ISBN-13", text="ISBN-13", anchor=CENTER)
    my_tree.heading("Availability", text="Availability", anchor=CENTER)


    #this is how we connect to our data base that contains the books
    conn = sqlite3.connect("library_crm.db")

    c = conn.cursor()


    c.execute("CREATE TABLE if not exists books(Book_Name text, Author_Name text, ISBN10 integer, ISBN13 integer, Availability text )")


    conn.commit()

    conn.close()


    #this function displays the books in the widget
    def queryDatabase():
        
        remove_all()

        conn = sqlite3.connect("library_crm.db")

        c = conn.cursor()


        c.execute("SELECT * FROM books")
        allBooks=c.fetchall()
        
        global count
        count = 0

        for record in allBooks  :
            if count %2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))
            count += 1



        conn.commit()

        conn.close()

    #this function shows the recommended books in the widget
    def showRec():
        remove_all()



        conn = sqlite3.connect("library_crm.db")

        c = conn.cursor()

        c.execute("CREATE TABLE if not exists bestbooks(Book_Name text, Author_Name text, ISBN10 integer, ISBN13 integer, Availability text )")
        
        c.execute("SELECT * FROM bestbooks")
        allBooks=c.fetchall()
        
        global count
        count = 0

        for record in allBooks  :
            if count %2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))
            count += 1



        conn.commit()

        conn.close() 
            


    #this function remove the books from the eyesite not from the main database
    def remove_all():
        for books in my_tree.get_children():
            my_tree.delete(books)


    #this function do the search functionality from the data base and it show the books in the main book area not in recommended 
    def search_books():
        book_name = search_entry.get()

        remove_all()

        search.destroy()

        conn = sqlite3.connect("library_crm.db")

        c = conn.cursor()

        c.execute("SELECT * FROM books WHERE Book_Name like ?", [book_name])
        all_stuff = c.fetchall()

        global count
        count = 0

        for book in all_stuff:
            if count %2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(book[0], book[1], book[2], book[3], book[4]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(book[0], book[1], book[2], book[3], book[4]), tags=("oddrow",))
            count += 1

        conn.commit()

        conn.close()



    def two_fun():
        enter_data()
        destroy_rent()

    #this function do alot of things it appends the names of people to the database for it and toggel change functions and thankyou and mail and insertdata
    def enter_data():
        
        accepted = accept_var.get()
        f =[]
        if accepted =="Accepted":
            email= email_entry.get()
            id = id_entry.get()
            name = name_entry.get()
            day = rent_spinbox.get()
            book = bookName_entry.get()
            f.append(email)
            f.append(id)
            f.append(name)
            f.append(bookTimeDate(int(day)))
            f.append(book)
            print(f)
            change()
            changeBest()
            thankyou(name)
            mail(f[1], f[0], f[2],f[4], bookTimeDate(int(day)))
            insert_data(f)
        else:
            messagebox.showwarning(title= "Error", message="you have not accepted the terms")
            

    def mail(id, email, name, book, date):
        def appendPpl(id, email, name):
            with open("ppl.txt", "a") as file:
                file.write(f"{id} {email} {name} {book} {date} \n")

        def emailSender(id, email, book, date):
            smtp_server = "smtp.titan.email"
            smtp_port = 465
            sender = "YOUR EMAIL"
            password = "YOUR PASS"
            recipients = [email]

            context = ssl.create_default_context()

            s = smtplib.SMTP_SSL(smtp_server, smtp_port, context)
            s.set_debuglevel(1)

            s.ehlo()
            s.login(sender, password)

            # create a MIMEMultipart object
            msg = MIMEMultipart()

            # set the font, size, and color using HTML tags
            html = f"""
            <html>
            <head></head>
            <body>
                <p style="font-family: serif; font-size: 20px; color: black;">
                Hello {name}, thank you for using our system.<br>
                ID: {id}<br>
                BOOK: {book}<br>
                DATE TO RETURN: {date}<br>
                please visit the library to take your book.<br>
                If you have any questions, please contact us on this email.<br>
                Regards, Bookworms Team.
                ----------------------------<br>
                    This is an automatically generated email, please do not reply.
                </p>
            </body>
            </html>
            """

            # create a MIMEText object with the HTML message
            text = MIMEText(html, "html")

            # add the text to the MIMEMultipart object
            msg.attach(text)

            # open the image file in binary mode
            with open('bookworms123.jpg', 'rb') as f:
                # set image as the payload for the MIMEImage object
                image = MIMEImage(f.read())

            # add the image to the MIMEMultipart object
            msg.attach(image)

            msg['From'] = sender
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = "Book Request"
            s.sendmail(sender, recipients, msg.as_string())
            s.close()

        appendPpl(id, email, name)
        emailSender(id, email, book, date)

    #it gives a time to return the book
    def bookTimeDate(x):
        current_timedate = dt.datetime.now()
        numDays= dt.timedelta(x)
        returnDate = current_timedate + numDays
        return returnDate

    #it check if the book is avalabel or not
    def avCheck():
        selected = my_tree.focus()

        values = my_tree.item(selected, "values")
        if values[4] == "no":
            messagebox.showwarning(title="Erorr", message="this book is already borrowed")
        else:
            rent()



    #it opens the rent window to get data
    def rent():
        global accept_var,email_entry,rent_spinbox,id_entry,name_entry,rent_window
        rent_window = Toplevel(root)

        frame = Frame(rent_window)
        frame.pack()

        user_info_frame = LabelFrame(frame, text="User information")
        user_info_frame.grid(row=0, column=0, padx=20, pady=10)

        email_label = Label(user_info_frame, text="Enter Email")
        email_label.grid(row=0, column=0)
        email_entry = Entry(user_info_frame)
        email_entry.grid(row=1, column=0)

        id_label = Label(user_info_frame, text="Enter ID")
        id_label.grid(row=0, column=1)
        id_entry = Entry(user_info_frame)
        id_entry.grid(row=1, column=1)

        name_label = Label(user_info_frame, text="Enter your Name")
        name_label.grid(row=0, column=2)
        name_entry = Entry(user_info_frame)
        name_entry.grid(row=1, column=2)

        rent_label = Label(user_info_frame, text="Enter time to Rent")
        rent_spinbox = Spinbox(user_info_frame, from_=1, to=15)
        rent_label.grid(row=2, column=0)
        rent_spinbox.grid(row=3, column=0)

        accept_var = StringVar(value="Not Accepted")
        terms_frame = LabelFrame(frame, text="Terms & Conditions")
        terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)

        terms_check = Checkbutton(terms_frame, text="I accept the terms and conditions. ", variable=accept_var, onvalue="Accepted", offvalue="Not Accepted" )
        terms_check.grid(row=0, column=0)

        button = Button(frame, text="Submit", command=two_fun)
        button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    #it hides the rent window
    def destroy_rent():
        rent_window.destroy


    #it puts the user info that he put in the rent function to a database
    def insert_data(list):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("CREATE TABLE if not exists user_info(email, ID, name, rent_time, book)")
        
        c.execute(f"INSERT INTO user_info(ID, email, name, rent_time, book) values('{list[0]}', '{list[1]}', '{list[2]}', '{list[3]}', '{list[4]}') ")

        conn.commit()
        conn.close()

    #this is the search window
    def search_pop():
        global search_entry, search

        search = Toplevel(root)
        search.title("Search Bar")
        search.geometry("400x200")
        search.configure(bg='grey26')

        search_frame = LabelFrame(search, text="enter book name ", font=("Comic Sans MS", 10))
        search_frame.pack(padx=10, pady=10)

        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(padx=20, pady=20)

        search_button_inner = Button(search, text="Search Books", command=search_books)
        search_button_inner.pack(padx=20, pady=20)
        search_button_inner.configure(bg='RoyalBlue1', activebackground='RoyalBlue4', height=1, width=13, bd=6, font=("Comic Sans MS", 9, "bold"))





    #this is the widget that contains the data of books
    my_tree.tag_configure("oddrow", background="white")
    my_tree.tag_configure("evenrow", background="lightblue")

    #this is the frame that contains the data for each book when press
    data_frame = LabelFrame(root, text="Book info", font=("Comic Sans MS", 10))
    data_frame.pack(fill="x", expand="yes", padx=20)

    av_entry = Entry(data_frame)
    av_entry.grid(row=0 , column=4, padx=10, pady=10)

    ISBN10_entry = Entry(data_frame)
    ISBN10_entry.grid(row=0, column=2, padx=10, pady=10)

    bookName_entry = Entry(data_frame)
    bookName_entry.grid(row=0, column=0, padx=10, pady=10)

    ISBN13_entry = Entry(data_frame)
    ISBN13_entry.grid(row=0, column=3, padx=10, pady=10)

    autherName_entry = Entry(data_frame)
    autherName_entry.grid(row=0, column=1, padx=10, pady=10)
        
    # this is where all buttons are created
    button_frame = LabelFrame(root, text="Commands", font=("Comic Sans MS", 10))
    button_frame.pack(fill="x", expand="yes", padx=20)

    reset_button = Button(button_frame, text="Reset", command=queryDatabase)
    reset_button.grid(row=0, column=4, padx=10, pady=10)
    reset_button.configure(bg='SteelBlue1', activebackground='SteelBlue4',  font=("Comic Sans MS", 9, "bold"), height=1, width=13, bd=6)

    return_button = Button(button_frame, text="Exit", command=root.destroy)
    return_button.grid(row=0, column=0, padx=10, pady=10)
    return_button.configure(bg='DeepSkyBlue3', activebackground='DeepSkyBlue4',  font=("Comic Sans MS", 9, "bold"), height=1, width=13, bd=6)

    rent_button = Button(button_frame, text="Rent the Book", command=avCheck)
    rent_button.grid(row=0, column=1, padx=10, pady=10)
    rent_button.configure(bg='SlateBlue2', activebackground='SlateBlue4',  font=("Comic Sans MS", 9, "bold"), height=1, width=13, bd=6)

    rec_button = Button(button_frame, text="show recommendation book page", command=showRec)
    rec_button.grid(row=0, column=2, padx=10, pady=10)
    rec_button.configure(bg='DodgerBlue2', activebackground='DodgerBlue4',  font=("Comic Sans MS", 9, "bold"), height=1, width=26, bd=6)

    search_button = Button(button_frame, text="search bar ", command=search_pop )
    search_button.grid(row=0, column=3, padx=10, pady=10)
    search_button.configure(bg='RoyalBlue1', activebackground='RoyalBlue4',  font=("Comic Sans MS", 9, "bold"), height=1, width=13, bd=6)


    #this function displays the data from tree view when it is beig selected
    def select(event):
        av_entry.delete(0, END)
        bookName_entry.delete(0, END)
        ISBN10_entry.delete(0, END)
        ISBN13_entry.delete(0, END)
        autherName_entry.delete(0, END)

        selected = my_tree.focus()

        values = my_tree.item(selected, "values")

        bookName_entry.insert(0, values[0])
        ISBN10_entry.insert(0, values[2])
        av_entry.insert(0, values[4])
        autherName_entry.insert(0, values[1])
        ISBN13_entry.insert(0, values[3])



    #this function changes the availability in the main books area
    def change():
        selected = my_tree.focus()

        my_tree.item(selected, text="", values=(av_entry.get(),ISBN10_entry.get(),bookName_entry.get(),autherName_entry.get(),ISBN13_entry.get()))

        conn = sqlite3.connect("library_crm.db")

        c = conn.cursor()

        c.execute("""UPDATE books SET
            Book_Name = :book ,
            Author_Name = :aut ,
            ISBN13 = :ISBN13,
            Availability = :AV 

            WHERE ISBN10 = :ISBN10""",
            {
                
                
                "book" : bookName_entry.get(),
                "aut": autherName_entry.get(),
                "ISBN10":ISBN10_entry.get(),
                "ISBN13":ISBN13_entry.get(),
                "AV":"no"
            },)


        conn.commit()
        conn.close()





    #this function changes the availability in the recommended list area
    def changeBest():
        selected = my_tree.focus()

        my_tree.item(selected, text="", values=(av_entry.get(),ISBN10_entry.get(),bookName_entry.get(),autherName_entry.get(),ISBN13_entry.get()))

        conn = sqlite3.connect("library_crm.db")

        c = conn.cursor()

        c.execute("""UPDATE bestbooks SET
            Book_Name = :book ,
            Author_Name = :aut ,
            ISBN13 = :ISBN13,
            Availability = :AV 

            WHERE ISBN10 = :ISBN10""",
            {
                
                
                "book" : bookName_entry.get(),
                "aut": autherName_entry.get(),
                "ISBN10":ISBN10_entry.get(),
                "ISBN13":ISBN13_entry.get(),
                "AV":"no"
            },)

    def thankyou(name):
            username = name
            if username:
                messagebox.showinfo('', f'thank you {username} for using our program ! :) ')
            else:
                messagebox.showerror('Error', 'Please enter a name before clicking Done')




    #this makes the buttons act when click release
    my_tree.bind("<ButtonRelease-1>",select)

    queryDatabase()

    root.mainloop()

root = Tk()
root.title("main login page")
root.minsize(320, 200)
root.configure(bg='grey26')
# root.state('zoomed')
Label(root, text='Welcome to BookWorms !', bg='grey26', fg='white', font=("Comic Sans MS", 15, "bold")).place(x=35, y=20)


def returnLoginPage(window_to_destroy, window_to_open):
    # destroy the current window
    window_to_destroy.destroy()

    # open the new window
    window_to_open.pack()



# THE ADMIN PAGE FUNCTION IS NOT WORKING PROPERLY AND I DON'T KNOW WHY
def new():
    def admin():
        # create a function to append a book to the database
        def appendBooks():
            # create the dialog to prompt the user for the book information
            title_dialog = simpledialog.askstring("Input", "Enter the title of the book:", parent=admin)
            author_dialog = simpledialog.askstring("Input", "Enter the author of the book:", parent=admin)
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book:", parent=admin)
            isbn13_dialog = simpledialog.askstring("Input", "Enter the ISBN13 of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()
            # create a table named books in the database
            c.execute(
                "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, Book_Name TEXT, Author_Name TEXT, ISBN10 integer, ISBN13 integer)")

            # insert the book into the database
            c.execute("INSERT INTO books (Book_Name, Author_Name, ISBN10, ISBN13) VALUES (?, ?, ?, ?)", (title_dialog, author_dialog, isbn10_dialog, isbn13_dialog))
            conn.commit()
            conn.close()

        # create a function to delete a book from the database
        def deleteBooks():
            # create the dialog to prompt the user for the book ISBN10
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # delete the book from the database
            c.execute("DELETE FROM books WHERE ISBN10 = ?", (isbn10_dialog,))
            conn.commit()
            conn.close()

        # create a function to view the user data in the sqlite database
        def viewData():
            # connect to the database
            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            # create a table named users in the database
            c.execute("CREATE TABLE if not exists user_info(email, ID, name, rent_time, book)")

            # select all rows from the users table
            c.execute("SELECT * FROM user_info")
            rows = c.fetchall()

            # create a new window to display the data
            data_window = tk.Tk()
            data_window.title("Users Data")

            # create the labels for the table headings
            id_label = tk.Label(data_window, text="ID")
            id_label.grid(row=0, column=0)
            email_label = tk.Label(data_window, text="Email")
            email_label.grid(row=0, column=1)
            name_label = tk.Label(data_window, text="Name")
            name_label.grid(row=0, column=2)
            time_label = tk.Label(data_window, text="Rent Time")
            time_label.grid(row=0, column=3)
            book_label = tk.Label(data_window, text="Book")
            book_label.grid(row=0, column=4)

            # display the data in a table format using the grid geometry manager
            for i, row in enumerate(rows, start=1):
                id_label = tk.Label(data_window, text=row[0])
                id_label.grid(row=i, column=0)
                email_label = tk.Label(data_window, text=row[1])
                email_label.grid(row=i, column=1)
                name_label = tk.Label(data_window, text=row[2])
                name_label.grid(row=i, column=2)
                time_label = tk.Label(data_window, text=row[3])
                time_label.grid(row=i, column=3)
                book_label = tk.Label(data_window, text=row[4])
                book_label.grid(row=i, column=4)

            conn.close()

        # create a function to edit a book in the database
        def editBooks():
            # create the dialogs to prompt the user for the book id and the new book information
            isbn10_before_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book to edit:", parent=admin)
            name_dialog = simpledialog.askstring("Input", "Enter the new Name of the book:", parent=admin)
            author_dialog = simpledialog.askstring("Input", "Enter the new author of the book:", parent=admin)
            isbn10_dialog = simpledialog.askstring("Input", "Enter the new ISBN10 of the book:", parent=admin)
            isbn13_dialog = simpledialog.askstring("Input", "Enter the new ISBN13 of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # update the book in the database
            c.execute("UPDATE books SET Book_Name = ?, Author_Name = ?, ISBN10 = ?, ISBN13 = ? WHERE ISBN10 = ?",
                      (name_dialog, author_dialog, isbn10_dialog, isbn13_dialog, isbn10_before_dialog))
            conn.commit()
            conn.close()

        def viewBooks():
            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # select all rows from the users table
            c.execute("SELECT * FROM books")
            rows = c.fetchall()

            # create a new window to display the data in a table format using the grid geometry manager
            books_data_window = tk.Tk()
            books_data_window.title("Books Data")

            # create the labels for the table headings
            name_label = tk.Label(books_data_window, text="Book Name")
            name_label.grid(row=0, column=0)
            author_label = tk.Label(books_data_window, text="Author Name")
            author_label.grid(row=0, column=1)
            isbn10_label = tk.Label(books_data_window, text="ISBN10")
            isbn10_label.grid(row=0, column=2)
            isbn13_label = tk.Label(books_data_window, text="ISBN13")
            isbn13_label.grid(row=0, column=3)
            book_available_label = tk.Label(books_data_window, text="Availability")
            book_available_label.grid(row=0, column=4)

            # display the data in a table format using the grid geometry manager
            for i, row in enumerate(rows, start=1):
                name_label = tk.Label(books_data_window, text=row[0])
                name_label.grid(row=i, column=0)
                author_label = tk.Label(books_data_window, text=row[1])
                author_label.grid(row=i, column=1)
                isbn10_label = tk.Label(books_data_window, text=row[2])
                isbn10_label.grid(row=i, column=2)
                isbn13_label = tk.Label(books_data_window, text=row[3])
                isbn13_label.grid(row=i, column=3)
                book_available_label = tk.Label(books_data_window, text=row[4])
                book_available_label.grid(row=i, column=4)

        # create a function to change the availability of a book in the database to "Yes" or "No"
        def availability():
            # create the dialog to prompt the user for the book id and the new book information
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book to edit:", parent=admin)
            book_available_dialog = simpledialog.askstring("Input", "Enter the availability of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # update the book in the database
            c.execute("UPDATE books SET Availability = ? WHERE ISBN10 = ?", (book_available_dialog, isbn10_dialog))

            # commit the changes to the database
            conn.commit()

            # close the connection to the database
            conn.close()

        # create a function to make admin add a recommended book to new database called bestBooks.db
        def addRec():
            # create the dialog to prompt the user for the book information
            title_dialog = simpledialog.askstring("Input", "Enter the title of the book:", parent=admin)
            author_dialog = simpledialog.askstring("Input", "Enter the author of the book:", parent=admin)
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book:", parent=admin)
            isbn13_dialog = simpledialog.askstring("Input", "Enter the ISBN13 of the book:", parent=admin)
            recAvailability_dialog = simpledialog.askstring("Input", "Enter the availability of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()
            # create a table named books in the database
            c.execute(
                "CREATE TABLE IF NOT EXISTS bestbooks (Book_Name TEXT, Author_Name TEXT, ISBN10 integer, ISBN13 integer, Availability TEXT)")
            # insert the book into the database
            c.execute("INSERT INTO bestbooks VALUES (?, ?, ?, ?, ?)",
                      (title_dialog, author_dialog, isbn10_dialog, isbn13_dialog, recAvailability_dialog))
            conn.commit()
            conn.close()

        # create a function to make admin delete a recommended book from the database
        def deleteRec():
            # create the dialog to prompt the user for the book ISBN10
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book to delete:", parent=admin)
            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()
            # delete the book from the database
            c.execute("DELETE FROM bestbooks WHERE ISBN10 = ?", (isbn10_dialog,))
            # commit the changes to the database
            conn.commit()

            # close the connection to the database
            conn.close()

        # create a function to make admin edit a recommended book in the database
        def editRec():
            # create the dialog to prompt the user for the book isbn and the new book information
            before_isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book to edit:", parent=admin)
            title_dialog = simpledialog.askstring("Input", "Enter the title of the book:", parent=admin)
            author_dialog = simpledialog.askstring("Input", "Enter the author of the book:", parent=admin)
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book:", parent=admin)
            isbn13_dialog = simpledialog.askstring("Input", "Enter the ISBN13 of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # update the book in the database
            c.execute("UPDATE bestbooks SET Book_Name = ?, Author_Name = ?, ISBN10 = ?, ISBN13 = ? WHERE ISBN10 = ?", (title_dialog, author_dialog, isbn10_dialog, isbn13_dialog, before_isbn10_dialog))

            # commit the changes to the database
            conn.commit()

            # close the connection to the database
            conn.close()

        # create a function to view the recommended books in the database
        def viewRec():
            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()
            # create a table named books in the database
            c.execute(
                "CREATE TABLE IF NOT EXISTS bestbooks (Book_Name TEXT, Author_Name TEXT, ISBN10 integer, ISBN13 integer, Availability TEXT)")
            # select all the books from the database
            c.execute("SELECT * FROM bestbooks")
            rows = c.fetchall()
            # commit the changes to the database
            conn.commit()
            # close the connection to the database
            conn.close()
            # create a new window to show the books
            books_data_window = tk.Toplevel(admin)
            books_data_window.title("Recommended Books")
            books_data_window.geometry("750x400")
            # create the labels for the columns of the table
            book_name_label = tk.Label(books_data_window, text="Book Name", font=("Arial", 12))
            book_name_label.grid(row=0, column=0, padx=10, pady=10)
            author_name_label = tk.Label(books_data_window, text="Author Name", font=("Arial", 12))
            author_name_label.grid(row=0, column=1, padx=10, pady=10)
            isbn10_label = tk.Label(books_data_window, text="ISBN10", font=("Arial", 12))
            isbn10_label.grid(row=0, column=2, padx=10, pady=10)
            isbn13_label = tk.Label(books_data_window, text="ISBN13", font=("Arial", 12))
            isbn13_label.grid(row=0, column=3, padx=10, pady=10)
            availability_label = tk.Label(books_data_window, text="Availability", font=("Arial", 12))
            availability_label.grid(row=0, column=4, padx=10, pady=10)
            # create the labels for the rows of the table
            for i in range(len(rows)):  # rows
                for j in range(len(rows[i])):  # columns
                    e = tk.Entry(books_data_window, width=20, fg='blue')
                    e.grid(row=i + 1, column=j)
                    e.insert(tk.END, rows[i][j])

        # create a function to change avisibility of recommended books
        def recAvailability():
            # create the dialog to prompt the user for the book id and the new book information
            isbn10_dialog = simpledialog.askstring("Input", "Enter the ISBN10 of the book to edit:", parent=admin)
            recAvailability_dialog = simpledialog.askstring("Input", "Enter the availability of the book:", parent=admin)

            # connect to the database
            conn = sqlite3.connect('library_crm.db')
            c = conn.cursor()

            # update the book in the database
            c.execute("UPDATE bestbooks SET Availability = ? WHERE ISBN10 = ?", (recAvailability_dialog, isbn10_dialog))

            # commit the changes to the database
            conn.commit()

            # close the connection to the database
            conn.close()

        # create function to make admin exit and return to the login page
        def exitAdmin():
            admin.destroy()

        # create the window
        admin = tk.Tk()
        admin.title("Admin Page")
        admin.geometry("850x800")
        admin.configure(bg='grey26')

        # add a welcome text
        functionality_text = tk.Label(admin, text="Functionalities : ", bg='grey26', fg='white', font=("Comic Sans MS", 24))
        functionality_text.place(x=40, y=30)
        welcome_text = tk.Label(admin, text="Welcome admin !", bg='grey26', fg='white', font=("Comic Sans MS", 30, "bold"))
        welcome_text.place(x=450, y=250)

        # create the buttons
        append_button = tk.Button(admin, text="Add a Book", command=appendBooks, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='SlateBlue4')
        delete_button = tk.Button(admin, text="Delete a Book", command=deleteBooks, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='SlateBlue3')
        view_button = tk.Button(admin, text="View Users", command=viewData, height=1, font=("Comic Sans MS", 10, "bold"), width=40, bd=6, bg='SlateBlue2')
        edit_button = tk.Button(admin, text="Edit Book", command=editBooks, height=1, font=("Comic Sans MS", 10, "bold"), width=40, bd=6, bg='SlateBlue1')
        view_books = tk.Button(admin, text="View Books", command=viewBooks, height=1, font=("Comic Sans MS", 10, "bold"), width=40, bd=6, bg='RoyalBlue1')
        availability_button = tk.Button(admin, text="Change Availability", command=availability, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='RoyalBlue2')
        addRec_button = tk.Button(admin, text="Add a Recommended Book", command=addRec, height=1, font=("Comic Sans MS", 10, "bold"), width=40, bd=6, bg='RoyalBlue3')
        deleteRec_button = tk.Button(admin, text="Delete a Recommended Book", command=deleteRec, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='RoyalBlue4')
        editRec_button = tk.Button(admin, text="Edit a Recommended Book", command=editRec, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='DodgerBlue4')
        viewRec_button = tk.Button(admin, text="View Recommended Books", command=viewRec, font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6, bg='DodgerBlue3')
        recAvailability_button = tk.Button(admin, text="Change Availability of Recommended Books", command=recAvailability,font=("Comic Sans MS", 10, "bold"), height=1, width=40, bd=6,  bg='DodgerBlue2')
        exit_button = tk.Button(admin, text="Exit", command=exitAdmin)

        # pack the buttons
        append_button.place(x=25, y=100)
        delete_button.place(x=25, y=150)
        view_button.place(x=25, y=200)
        edit_button.place(x=25, y=250)
        view_books.place(x=25, y=300)
        availability_button.place(x=25, y=350)
        addRec_button.place(x=25, y=400)
        deleteRec_button.place(x=25, y=450)
        editRec_button.place(x=25, y=500)
        viewRec_button.place(x=25, y=550)
        recAvailability_button.place(x=25, y=600)
        exit_button.place(x=550, y=650)

        # start the window
        admin.mainloop()

    # added the adminlogin function into the (new) function
    def adminlogin():
        global entry1
        global entry2
        # Initialize entry1 and entry2
        entry1 = entry1
        entry2 = entry2
        username = entry1.get()
        password = entry2.get()
        if username == 'admin' and password == 'admin123':
            messagebox.showinfo('', 'login success')
            # after the login success it will open the admin page and close the current window (login page)
            branch.destroy()
            root.destroy()
            returnLoginPage(branch, admin())
        else:
            messagebox.showerror('', 'user unidentified')
            # now we will use the returnLoginPage function to return and close the current window
            returnLoginPage(branch, root)

    branch = Tk()
    branch.title("administrator Login")
    branch.geometry("300x200")
    branch.configure(bg='grey26')

    Label(branch, text='username : ', bg='grey26', fg='white', font=("Comic Sans MS", 12)).place(x=30, y=15)
    Label(branch, text='password : ', bg='grey26', fg='white', font=("Comic Sans MS", 12)).place(x=30, y=65)

    global entry1
    global entry2

    # Define entry1 and entry2
    entry1 = Entry(branch, bd=1)
    entry1.place(x=140, y=20)
    entry2 = Entry(branch, bd=1)
    entry2 = Entry(branch, show='*')
    entry2.place(x=140, y=70)

    def show_password():
        if entry2.cget('show') == '*':
            entry2.config(show='')
        else:
            entry2.config(show='*')

    Button(branch, text='login', command=adminlogin, font=("Comic Sans MS", 10), bg='SteelBlue1', activebackground='SteelBlue4', height=1, width=10, bd=6).place(x=100, y=140)

    check_button = Checkbutton(branch, text='show password', bg='grey26', fg='white', font=("Comic Sans MS", 9), command=show_password)
    check_button.place(x=135, y=100)

    branch.mainloop()


Button(root, text='admin', height=1, width=10, bd=6, command=new, font=("Comic Sans MS", 10), bg='SlateBlue2', activebackground='SlateBlue4').place(x=20, y=100)
Button(root, text='user', height=1, width=10, bd=6, command=open_user, font=("Comic Sans MS", 10), bg='DodgerBlue2', activebackground='DodgerBlue4').place(x=200, y=100)

root.mainloop()