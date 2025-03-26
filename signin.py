from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
import subprocess

# Function to reset password
def forget_pass():
    def change_password():
        username = user_entry.get()
        new_password = newpass_entry.get()
        confirm_password = confirmpass_entry.get()

        if username == '' or new_password == '' or confirm_password == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=window)
        elif new_password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match!', parent=window)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='aditya', database='userdatu')
                mycursor = con.cursor()
                query = 'SELECT * FROM data WHERE username=%s'
                mycursor.execute(query, (username,))
                row = mycursor.fetchone()

                if row is None:
                    messagebox.showerror('Error', 'Username not found!', parent=window)
                else:
                    query = 'UPDATE data SET password=%s WHERE username=%s'
                    mycursor.execute(query, (new_password, username))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success', 'Password reset successfully!', parent=window)
                    window.destroy()
            except Exception as e:
                messagebox.showerror('Database Error', str(e), parent=window)

    window = Toplevel()
    window.title('Reset Password')

    bgPic = ImageTk.PhotoImage(file='background.jpg')
    bgLabel = Label(window, image=bgPic)
    bgLabel.grid()

    Label(window, text='RESET PASSWORD', font=('Arial', 18, 'bold'), bg='white', fg='magenta2').place(x=480, y=60)

    Label(window, text='Username', font=('Arial', 12, 'bold'), bg='white', fg='orchid1').place(x=470, y=130)
    user_entry = Entry(window, width=25, fg='magenta2', font=('Arial', 11, 'bold'), bd=0)
    user_entry.place(x=470, y=160)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=180)

    Label(window, text='New Password', font=('Arial', 12, 'bold'), bg='white', fg='orchid1').place(x=470, y=210)
    newpass_entry = Entry(window, width=25, fg='magenta2', font=('Arial', 11, 'bold'), bd=0)
    newpass_entry.place(x=470, y=240)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)

    Label(window, text='Confirm Password', font=('Arial', 12, 'bold'), bg='white', fg='orchid1').place(x=470, y=290)
    confirmpass_entry = Entry(window, width=25, fg='magenta2', font=('Arial', 11, 'bold'), bd=0)
    confirmpass_entry.place(x=470, y=320)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=340)

    Button(window, text='Submit', bd=0, bg='magenta2', fg='white', font=('Open Sans', 16, 'bold'), width=19, 
           cursor='hand2', activebackground='magenta2', activeforeground='white', command=change_password).place(x=470, y=390)

    window.mainloop()


# Function to log in user
def login_user():
    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showerror('Error', 'All Fields Are Required')
        return

    try:
        con = pymysql.connect(host='localhost', user='root', password='aditya', database='userdatu')
        mycursor = con.cursor()

        query = 'SELECT * FROM data WHERE username=%s AND password=%s'
        mycursor.execute(query, (username, password))
        row = mycursor.fetchone()

        if row is None:
            messagebox.showerror('Error', 'Invalid username or password')
        else:
            messagebox.showinfo('Success', f'Login Successful! Welcome {username}')
            login_window.destroy()  # Close login window

            # ✅ Redirect to mainmenu.py with username
            subprocess.run(["python", "mainmenu.py", username])

        con.close()
    except Exception as e:
        messagebox.showerror('Database Error', str(e))


# Function to open sign-up page
def signup_page():
    login_window.destroy()
    import signup


def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


# GUI for login page
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title('Login Page')

bgImage = ImageTk.PhotoImage(file='bg.jpg')
Label(login_window, image=bgImage).place(x=0, y=0)

Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white', fg='firebrick1').place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

Frame(login_window, width=250, height=2, bg='firebrick1').place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

Frame(login_window, width=250, height=2, bg='firebrick1').place(x=580, y=282)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.place(x=800, y=255)

Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2',
       font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1', command=forget_pass).place(x=715, y=295)

Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='firebrick1',
       activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=19, command=login_user).place(x=578, y=350)

Label(login_window, text="Don't have an account?", font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white').place(x=593, y=500)
Button(login_window, text='Create new one', font=('Open Sans', 9, 'bold underline'), fg='blue', bg='white',
       activeforeground='blue', activebackground='white', cursor='hand2', bd=0, command=signup_page).place(x=727, y=500)

login_window.mainloop()
