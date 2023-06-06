import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
from tkinter.ttk import Combobox
import time
import pyttsx3
import os
import socket

engine = pyttsx3.init('sapi5')


# Functions to send a requests to the server
def request_for_viewing_notes(request):
    str = ""
    server_address = ('localhost', 1234)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the request to the server
        client_socket.send(request.encode())

        # Receive and process the response from the server
        response = client_socket.recv(1024).decode()
        str = response
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Connection refused. Make sure the server is running.")
    finally:
        # Close the client socket
        client_socket.close()
        return str


def send_request_login(request):
    str = ""
    server_address = ('localhost', 1234)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the request to the server
        client_socket.send(request.encode())

        # Receive and process the response from the server
        response = client_socket.recv(1024).decode()
        str = response
        process_response(response)
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Connection refused. Make sure the server is running.")
    finally:
        # Close the client socket
        client_socket.close()
        return str


def send_request(request):
    server_address = ('localhost', 1234)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the request to the server
        client_socket.send(request.encode())

        # Receive and process the response from the server
        response = client_socket.recv(1024).decode()
        if (response != ""):
            process_response(response)
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Connection refused. Make sure the server is running.")
    finally:
        # Close the client socket
        client_socket.close()


# Process the response from the server
def process_response(response):
    messagebox.showinfo("Server Response", response)


def set_window(window, w, h):
    # get screen width and height
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.resizable(False, False)


def update_clock(clock_label):
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock, clock_label)


def talk(text_area, genderComboBox, speedComboBox):
    text = text_area.get("1.0", "end")
    gender = genderComboBox.get()
    speed = speedComboBox.get()
    voices = engine.getProperty('voices')

    def set_voice():
        if gender == 'Jane':
            engine.setProperty('voice', voices[0].id)
        elif gender == 'Anna':
            engine.setProperty('voice', voices[1].id)

        engine.say(text)
        engine.runAndWait()
    if text:
        if speed == 'Fast':
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 60)

        set_voice()


def save(text_area, genderComboBox, speedComboBox):
    text = text_area.get("1.0", "end")
    gender = genderComboBox.get()
    speed = speedComboBox.get()
    voices = engine.getProperty('voices')

    def set_voice():
        if gender == 'Jane':
            engine.setProperty('voice', voices[0].id)
        elif gender == 'Anna':
            engine.setProperty('voice', voices[1].id)
        path = filedialog.askdirectory()

        os.chdir(path)
        engine.save_to_file(text, 'text.mp3')
        engine.runAndWait()

    if text:
        if speed == 'Fast':
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 60)

        set_voice()


class NoteFunctional:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def view_content_window(self):
        def view_note_content():
            note_title = note_title_entry.get()
            request = f"view_note_content {self.login} {self.password} {note_title}"
            str = request_for_viewing_notes(request)
            note_textbox.configure(state="normal")
            note_textbox.delete("1.0", "end")
            note_textbox.insert("1.0", str)
            note_textbox.pack()

        def save_note_content():
            note_title = note_title_entry.get()
            text = note_textbox.get("1.0", "end")
            request = f"save_note_content {self.login} {self.password} {note_title} {text}"

            send_request(request)

            note_textbox.configure(state="normal")
            note_textbox.delete("1.0", "end")
            note_textbox.pack()

        window = tk.Tk()

        window.configure(bg="#303030")  # Set background color to a dark gray tone
        w = 600  # width for the Tk root
        h = 600  # height for the Tk root

        set_window(window, w, h)

        window.title("Content of Note")

        # Set font styles
        label_font = Font(family="Helvetica", size=14, weight="bold")
        entry_font = Font(family="Helvetica", size=12)
        button_font = Font(family="Helvetica", size=12, weight="bold")

        # Note Title Label
        note_title_label = tk.Label(window, text="Note title:", bg="#303030", fg="white", font=label_font)
        note_title_label.pack()

        # Note Title Entry
        note_title_entry = tk.Entry(window, bg="#505050", fg="white", font=entry_font)
        note_title_entry.pack()

        # Note Textbox
        note_textbox = tk.Text(window, bg="#505050", fg="white", font=entry_font)
        note_textbox.pack(fill="both", expand=True)

        # Show Content Button
        show_content_button = tk.Button(window, text="Show content", bg="#4080bf", fg="white", font=button_font,
                                        command=lambda: view_note_content())
        show_content_button.pack()

        # Save Content Button
        save_content_button = tk.Button(window, text="Save content", bg="#4080bf", fg="white", font=button_font,
                                        command=lambda: save_note_content())
        save_content_button.pack()

        # Run the window
        window.mainloop()

    def view_notes_titles_window(self, main_frame):
        def view_notes():
            request = f"view_notes {self.login} {self.password}"
            str = request_for_viewing_notes(request)
            notes_textbox.configure(state="normal")
            notes_textbox.delete("1.0", "end")
            notes_textbox.insert("1.0", str)
            notes_textbox.pack()

        frame = tk.Frame(main_frame, width=400, height=400)
        frame.configure(bg='#303030', pady=10)
        frame.pack()


        # View Notes Button
        view_notes_button = tk.Button(frame, text="View Notes", bg="Gray", fg="black", font=("Arial", 14, "bold"),
                                      command=lambda: view_notes())
        view_notes_button.pack()

        # Notes Textbox
        notes_textbox = tk.Text(frame, bg="black", fg="white", font=("Courier", 14))
        notes_textbox.configure(state="disabled")
        notes_textbox.pack(fill="both", expand=True)

    def add_note_window(self, main_frame):
        def add_note():
            note_title = note_title_entry.get()
            note_content = note_content_entry.get()
            request = f"add_note {self.login} {self.password} {note_title} {note_content}"
            send_request(request)

        frame = tk.Frame(main_frame, width=450, height=300)
        frame.configure(bg='#303030', pady=10)
        frame.pack_propagate(0)
        frame.pack(pady=30)

        # Set font styles
        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12, "bold")
        button_font = ("Arial", 12, "bold")

        # Note Title Label
        note_title_label = tk.Label(frame, text="Note title:", bg="#303030", fg="white", font=label_font)
        note_title_label.pack()

        # Note Title Entry
        note_title_entry = tk.Entry(frame, bg="#505050", fg="white", font=entry_font)
        note_title_entry.pack()

        # Note Content Label
        note_content_label = tk.Label(frame, text="Note content:", bg="#303030", fg="white", font=label_font)
        note_content_label.pack()

        # Note Content Entry
        note_content_entry = tk.Entry(frame, bg="#505050", fg="white", font=entry_font)
        note_content_entry.pack()

        # Add Note Button
        add_note_button = tk.Button(frame, text="Add Note", bg="#4080bf", fg="white", font=button_font,
                                    command=lambda: add_note())
        add_note_button.pack()

    def delete_note_window(self, main_frame):
        def delete_note():
            note_title = note_title_entry.get()
            request = f"delete_note {self.login} {self.password} {note_title}"
            send_request(request)

        frame = tk.Frame(main_frame)
        frame.configure(bg='#303030', width=450, height=300)
        frame.pack()
        frame.pack_propagate(0)
        frame.pack(pady=30)

        # Set font styles
        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12, "bold")
        button_font = ("Arial", 12, "bold")

        # Note Title Label
        note_title_label = tk.Label(frame, text="Note title:", bg="#303030", fg="white", font=label_font)
        note_title_label.pack(pady=10)

        # Note Title Entry
        note_title_entry = tk.Entry(frame, bg="#505050", fg="white", font=entry_font)
        note_title_entry.pack(padx=10, pady=5)

        # Delete Note Button
        delete_note_button = tk.Button(frame, text="Delete Note", bg="#bf4040", fg="white", font=button_font,
                                       command=lambda: delete_note())
        delete_note_button.pack(pady=10)

        # Run the delete note window


class StartMenu:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.noteFunctional = NoteFunctional(username, password)
        self.root = tk.Tk()
        self.root.geometry('600x400')
        self.root.title("Menu")
        self.main_frame = tk.Frame(self.root, highlightbackground='black', highlightthickness=2)
        self.options_frame = tk.Frame(self.root, bg='gray')

        self.home_btn = tk.Button(self.options_frame, text='Home', font=('Bold', 15),
                                  fg='gray', bd=0, bg='black', command=lambda: self.show_indicator(self.homeIndicate, self.home_page))
        self.home_btn.place(x=10, y=50)
        self.homeIndicate = tk.Label(self.options_frame, text='', bg='gray')
        self.homeIndicate.place(x=3, y=50, width=5, height=40)

        self.notes_btn = tk.Button(self.options_frame, text='Notes', font=('Bold', 15),
                                   fg='gray', bd=0, bg='black', command=lambda: self.show_indicator(self.notesIndicate, self.notes_page))
        self.notes_btn.place(x=10, y=100)
        self.notesIndicate = tk.Label(self.options_frame, text='', bg='gray')
        self.notesIndicate.place(x=3, y=100, width=5, height=40)

        self.paint_btn = tk.Button(self.options_frame, text='Paint', font=('Bold', 15),
                                   fg='gray', bd=0, bg='black',  command=lambda: self.show_indicator(self.paintIndicate, self.paint_page))
        self.paint_btn.place(x=10, y=150)
        self.paintIndicate = tk.Label(self.options_frame, text='', bg='gray')
        self.paintIndicate.place(x=3, y=150, width=5, height=40)

        self.to_speech_btn = tk.Button(self.options_frame, text='Speech', font=('Bold', 15),
                                       fg='gray', bd=0, bg='black',  command=lambda: self.show_indicator(self.toSpeechIndicate, self.to_speech_page))
        self.to_speech_btn.place(x=10, y=200)
        self.toSpeechIndicate = tk.Label(self.options_frame, text='', bg='gray')
        self.toSpeechIndicate.place(x=3, y=200, width=5, height=40)

        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=100, height=400)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.propagate(False)
        self.main_frame.configure(height=400, width=500)

        self.hide_all_indicators()

    def hide_all_indicators(self):
        self.homeIndicate.configure(bg='gray')
        self.notesIndicate.configure(bg='gray')
        self.paintIndicate.configure(bg='gray')
        self.toSpeechIndicate.configure(bg='gray')

    def del_pages(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def show_indicator(self, lb, page):
        self.hide_all_indicators()
        lb.configure(bg='black')
        self.del_pages()
        page()

    # timer
    def home_page(self):
        home_frame = tk.Frame(self.main_frame)
        clock_label = tk.Label(home_frame, font=("Arial", 48), fg="black", bg="white")
        clock_label.pack(padx=50, pady=50)

        update_clock(clock_label)

        home_frame.pack(pady=50)

    # notes
    def btn_invoke(self, index):
        if index != 2:
            self.del_pages()

        if index == 1:
            self.noteFunctional.view_notes_titles_window(self.main_frame)
        elif index == 2:
            self.noteFunctional.view_content_window()
        elif index == 3:
            self.noteFunctional.add_note_window(self.main_frame)
        elif index == 4:
            self.noteFunctional.delete_note_window(self.main_frame)

    def notes_page(self):
        notes_frame = tk.Frame(self.main_frame, width=400, height=400)
        notes_frame.configure(bg='black')
        notes_frame.pack_propagate(0)

        button_style = {
            'relief': 'raised',
            'borderwidth': 2,
            'highlightthickness': 0,
            'font': ('Arial', 12),
            'bg': 'light blue',
            'fg': 'black',
            'padx': 10,
            'pady': 5
        }

        frame = tk.Frame(notes_frame, pady=50, bg="black")
        frame.pack()



        # View Notes Button
        view_notes_button = tk.Button(frame, text="View Notes Titles",
                                   command=lambda: self.btn_invoke(1), **button_style)
        view_notes_button.pack()

        # # View note content
        view_content_button = tk.Button(frame, text="View note content",
                                     command=lambda: self.btn_invoke(2), **button_style)
        view_content_button.pack()

        # # Add Note Button
        add_note_button = tk.Button(frame, text="Add Note", command=lambda: self.btn_invoke(3),
                                 **button_style)
        add_note_button.pack()

        # # Del Note Button
        delete_note_button = tk.Button(frame, text="Delete Note", command=lambda: self.btn_invoke(4),
                                    **button_style)
        delete_note_button.pack()

        notes_frame.pack(pady=20)

    # paint -
    def paint_page(self):
        paint_frame = tk.Frame(self.main_frame)
        lb = tk.Label(paint_frame, text='paint page')
        lb.pack()
        paint_frame.pack(pady=20)

    # text to speech -
    def to_speech_page(self):
        to_speech_frame = tk.Frame(self.main_frame, width=600, height=400)
        to_speech_frame.configure(bg='black')
        to_speech_frame.pack_propagate(0)

        text_box = tk.Text(to_speech_frame, font="Arial", bg='white')
        text_box.place(x=10, y=30, width=370, height=300)

        genderComboBox = Combobox(to_speech_frame, values=['Jane', 'Anna'], state='r', width=10)
        genderComboBox.place(x=400, y=50)
        genderComboBox.set('Jane')

        speedComboBox = Combobox(to_speech_frame, values=['Fast', 'Normal', 'Slow'], state='r', width=10)
        speedComboBox.place(x=400, y=100)
        speedComboBox.set('Normal')

        btnSpeak = tk.Button(to_speech_frame, text="Talk", font=('Arial', 10, 'bold'), width=10, command=lambda: talk(text_box, genderComboBox, speedComboBox))
        btnSpeak.place(x=400, y=150)

        btnSave = tk.Button(to_speech_frame, text="Save", font=('Arial', 10, 'bold'), width=10, command=save)
        btnSave.place(x=400, y=200)

        to_speech_frame.pack(pady=20)

    def run(self):
        self.root.mainloop()


class FirstWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.w = 300  # width for the Tk root
        self.h = 300  # height for the Tk root

        set_window(self.window, self.w, self.h)
        self.window.title("Note App")
        self.window.configure(bg="black")


        # Registration Button
        self.register_button = tk.Button(self.window, text="Register", command=self.register_window, width=10, height=4,
                                 font=("Arial", 12),
                                 bg="grey")
        self.register_button.place(x=110, y=50)


        # Login Button
        self.login_button = tk.Button(self.window, text="Login", command=self.login_window, width=10, height=4, font=("Arial", 12),
                              bg="grey")
        self.login_button.place(x=110, y=150)

    def register_window(self):
        # Create registration window
        self.register_window = RegistrationWindow()
        self.register_window.window.mainloop()

    def login_window(self):
        # Create registration window
        self.login_window = LoginWindow()
        self.login_window.window.mainloop()

    def run(self):
        self.window.mainloop()


class RegistrationWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="black")
        self.w = 300  # width for the Tk root
        self.h = 300  # height for the Tk root
        set_window(self.window, self.w, self.h)
        self.window.title("Registration")

        # Username Label and Entry
        self.username_label = tk.Label(self.window, text="Username:", font=("Arial", 16, "bold"), fg="grey",
                                    bg="black")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window, bg="grey", fg="white", font=("Arial", 14, "bold"))
        self.username_entry.pack()

        # Password Label and Entry
        self.password_label = tk.Label(self.window, text="Password:", font=("Arial", 16, "bold"), fg="grey",
                                    bg="black")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*", bg="grey", fg="white", font=("Arial", 14, "bold"))
        self.password_entry.pack()

        # Register Button
        self.register_button = tk.Button(self.window, text="Register", command=self.register, width=10, height=4,
                                      font=("Arial", 12), bg="grey")
        self.register_button.place(x=200, y=200)

        # Run the registration window
        self.window.mainloop()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        request = f"register {username} {password}"
        send_request(request)


class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="black")
        self.w = 300  # width for the Tk root
        self.h = 300  # height for the Tk root
        set_window(self.window, self.w, self.h)
        self.window.title("Login")

        # Username Label and Entry
        self.username_label = tk.Label(self.window, text="Username:", font=("Arial", 16, "bold"), fg="grey",
                                    bg="black")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window, bg="grey", fg="white", font=("Arial", 14, "bold"))
        self.username_entry.pack()

        # Password Label and Entry
        self.password_label = tk.Label(self.window, text="Password:", font=("Arial", 16, "bold"), fg="grey",
                                    bg="black")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*", font=("Arial", 14, "bold"), bg="grey", fg="white")
        self.password_entry.pack()

        # Login Button
        self.login_button = tk.Button(self.window, text="Login", command=self.login, width=10, height=4,
                                   font=("Arial", 12), bg="grey")
        self.login_button.place(x=200, y=200)

        # Run the login window
        self.window.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        request = f"login {username} {password}"
        str = send_request_login(request)

        print(str)
        if str == "Login was successful!":
            sideBarMenu = StartMenu(username, password)
            self.window.destroy()
            sideBarMenu.run()


if __name__ == '__main__':
    app = FirstWindow()
    app.run()
