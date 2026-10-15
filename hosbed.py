import tkinter as tk

from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import sqlite3

class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Bed Booking System")
        self.root.config(bg="#cfe2f3")  # Set overall background color

        self.current_user = None
        self.login_frame = None
        self.booking_frame = None
        self.availability_frame = None

        self.create_database()
        self.create_tables()
        self.create_gui()

    def create_database(self):
        # Create or connect to the database
        self.conn = sqlite3.connect("llllll.db")
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                gender TEXT,
                age INTEGER,
                bed_type TEXT
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS beds (
                bed_type TEXT,
                bed_number INTEGER,
                status INTEGER,
                booked_by TEXT,
                booking_time TEXT,
                booking_duration INTEGER,
                PRIMARY KEY (bed_type, bed_number)
            )
        ''')
        self.conn.commit()

    def create_tables(self):
        # Initialize bed availability
        bed_types = ['Luxury Bed', 'AC Bed', 'Normal Bed']
        for bed_type in bed_types:
            for bed_number in range(1, 11):
                self.conn.execute("INSERT OR IGNORE INTO beds VALUES (?, ?, 0, NULL, NULL, NULL)", (bed_type, bed_number))
        self.conn.commit()

    def create_gui(self):
        # Create the main login frame
        self.login_frame = tk.Frame(self.root, bg="#cfe2f3")  # Set login frame background color
        self.login_frame.pack()
        self.show_login_page()


    def show_login_page(self):
        self.clear_frame()
        self.booking_frame = None
        self.availability_frame = None

        if self.login_frame:
            self.login_frame.destroy()

        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Login", font=("Helvetica", 20, "bold")).grid(row=0, column=1, pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=1, column=0, pady=5)
        username_entry = tk.Entry(self.login_frame)
        username_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=2, column=0, pady=5)
        password_entry = tk.Entry(self.login_frame, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.grid(row=3, column=1, pady=10)

        create_profile_button = tk.Button(self.login_frame, text="Create Profile", command=self.create_profile)
        create_profile_button.grid(row=4, column=1, pady=5)

    def show_booking_page(self):
        self.clear_frame()
        self.login_frame = None
        self.availability_frame = None
        self.create_view_profile_button()

        welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Helvetica", 20))
        welcome_label.pack(pady=10)

        book_button = tk.Button(self.root, text="Book a Bed", command=self.book_bed)
        book_button.pack(pady=10)

        unbook_button = tk.Button(self.root, text="Release a Bed", command=self.unbook_bed)
        unbook_button.pack(pady=5)

        view_availability_button = tk.Button(self.root, text="View Bed Availability", command=self.view_bed_availability)
        view_availability_button.pack(pady=5)

        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

    def create_view_profile_button(self):
        # Create a button to view profile information
        view_profile_button = tk.Button(self.root, text="View Profile Info", command=self.view_profile_info)
        view_profile_button.pack(pady=5)

    def view_profile_info(self):
        # Display profile information
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (self.current_user,))
        user_data = cursor.fetchone()

        if user_data:
            messagebox.showinfo("Profile Information", f"Username: {user_data[0]}\nGender: {user_data[2]}\nAge: {user_data[3]}")
        else:
            messagebox.showerror("Error", "Profile not found.")


    def show_availability_page(self):
        self.clear_frame()
        self.login_frame = None
        self.booking_frame = None

        back_button = tk.Button(self.root, text="Back", command=self.show_booking_page)
        back_button.pack(pady=5)

        beds = self.get_bed_availability()
        self.availability_frame = tk.Frame(self.root, padx=20, pady=20)
        self.availability_frame.pack()

        for bed_type, bed_info in beds.items():
            tk.Label(self.availability_frame, text=bed_type, font=("Helvetica", 16, "bold")).pack(pady=5)

            bed_type_frame = tk.Frame(self.availability_frame)
            bed_type_frame.pack()

            for bed_number, (status, booked_by, booking_duration, booking_time) in bed_info.items():
                bed_status = "Available" if status == 0 else f"Booked by {booked_by}" if status == 1 else "Unavailable"
                bed_color = "green" if status == 0 else "yellow" if status == 1 and booked_by == self.current_user else "red"

                days_left = self.calculate_days_left(booking_time, booking_duration)
                bed_button = tk.Button(bed_type_frame, text=f"Bed {bed_number}\n{bed_status}\nDays Left: {days_left}", bg=bed_color,
                                       command=lambda b=bed_type, n=bed_number: self.book_bed_from_availability(b, n))
                bed_button.pack(side=tk.LEFT, padx=5, pady=5)

                # if status == 1:
                #     self.display_days_left(bed_button, days_left)

    def calculate_days_left(self, booking_time, booking_duration):
        if booking_time is None:
            return 0

        booking_datetime = datetime.strptime(booking_time, "%Y-%m-%d %H:%M:%S.%f")
        remaining_days = booking_duration - (datetime.now() - booking_datetime).days
        return max(remaining_days, 0)

    def display_days_left(self, widget, days_left):
        days_left_label = tk.Label(widget, text=f"Days Left: {days_left}")
        days_left_label.pack()




    # New method to handle bed booking from the availability page
    def book_bed_from_availability(self, bed_type, bed_number):
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, booked_by, booking_duration, booking_time FROM beds WHERE bed_type = ? AND bed_number = ?", (bed_type, bed_number))
        bed_data = cursor.fetchone()

        if not bed_data:
            messagebox.showerror("Error", "Invalid bed type or bed number.")
            return

        status, booked_by, _, _ = bed_data

        if status == 0:
            self.book_bed(bed_type, bed_number)
            self.show_availability_page()
        else:
            messagebox.showerror("Error", f"{bed_type} {bed_number} is already booked by {booked_by}.")


    def clear_frame(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self, username, password):
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            self.current_user = username
            self.show_booking_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_profile(self):
        # Get user input
        username = simpledialog.askstring("Create Profile", "Enter a username:")

        # Check if username is unique
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
        user_exists = cursor.fetchone()

        if user_exists:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return
        

        password = simpledialog.askstring("Create Profile", "Enter a password:")

        # Check password length
        if len(password) < 8:
            messagebox.showerror("Error", "Password should be at least 8 characters long.")
            return
        

        gender = simpledialog.askstring("Create Profile", "Enter your gender (Male, Female, Other):")

        # Check valid gender
        valid_genders = ["male", "female", "other"]
        if gender.lower() not in valid_genders:
            messagebox.showerror("Error", "Invalid gender. Please enter Male, Female, or Other.")
            return
        

        age = simpledialog.askinteger("Create Profile", "Enter your age:")

        # Check positive age
        if age < 0:
            messagebox.showerror("Error", "Age should be a positive whole number.")
            return

        # Check for valid input
        if not username or not password or not gender or age is None:
            messagebox.showerror("Error", "All fields are required.")
            return


        # Insert the new user into the database
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, NULL)", (username, password, gender, age))
        self.conn.commit()

        self.current_user = username
        self.show_booking_page()

            

    def logout(self):
        self.current_user = None
        self.show_login_page()


    def unbook_bed(self):
        bed_type = simpledialog.askstring("Unbook a Bed", "Enter bed type (Luxury Bed, AC Bed, Normal Bed):")
        bed_number = simpledialog.askinteger("Unbook a Bed", "Enter bed number (1-10):")

        if not bed_type or not bed_number:
            messagebox.showerror("Error", "Both bed type and bed number are required.")
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT status, booked_by FROM beds WHERE bed_type = ? AND bed_number = ?", (bed_type, bed_number))
        bed_data = cursor.fetchone()

        if not bed_data:
            messagebox.showerror("Error", "Invalid bed type or bed number.")
            return

        status, booked_by = bed_data

        if status == 1 and booked_by == self.current_user:
            cursor.execute("UPDATE beds SET status = 0, booked_by = NULL, booking_duration = NULL, booking_time = NULL WHERE bed_type = ? AND bed_number = ?",
                           (bed_type, bed_number))
            self.conn.commit()
            messagebox.showinfo("Success", f"{bed_type} {bed_number} unbooked successfully.")
            self.show_booking_page()
        else:
            messagebox.showerror("Error", "You can only unbook your own booked bed.")

    def view_bed_availability(self):
        self.show_availability_page()

    def book_bed_from_availability(self, bed_type, bed_number):
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, booked_by, booking_duration, booking_time FROM beds WHERE bed_type = ? AND bed_number = ?", (bed_type, bed_number))
        bed_data = cursor.fetchone()

        if not bed_data:
            messagebox.showerror("Error", "Invalid bed type or bed number.")
            return

        status, booked_by, booking_duration, booking_time = bed_data

        if status == 0:
            cursor.execute("UPDATE beds SET status = 1, booked_by = ?, booking_duration = ?, booking_time = ? WHERE bed_type = ? AND bed_number = ?",
                           (self.current_user, booking_duration, datetime.now(), bed_type, bed_number))
            self.conn.commit()
            messagebox.showinfo("Success", f"{bed_type} {bed_number} booked successfully for {booking_duration} minutes.")
            self.show_availability_page()
        else:
            messagebox.showerror("Error", f"{bed_type} {bed_number} is already booked by {booked_by}.")

    # def display_timer(self, widget, duration, start_time):
    #     start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    #     duration_seconds = int(duration.split()[0]) * 60  # Extract the numerical part and convert to seconds
    #     remaining_time = duration_seconds - int((datetime.now() - start_time).total_seconds())

    #     def update_timer():
    #         nonlocal remaining_time
    #         if remaining_time >= 0:
    #             timer_label.config(text=f"Time left: {remaining_time // 60}m {remaining_time % 60}s")
    #             remaining_time -= 1
    #             self.root.after(1000, update_timer)
    #         else:
    #             timer_label.config(text="Booking Expired")

    #     timer_label = tk.Label(widget, text="")
    #     timer_label.pack()
    #     update_timer()


    def profile_info(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (self.current_user,))
            user_data = cursor.fetchone()

            if user_data:
                messagebox.showinfo("Profile Information", f"Username: {user_data[0]}\nGender: {user_data[2]}\nAge: {user_data[3]}")
            else:
                messagebox.showerror("Error", "Profile not found.")

    def get_bed_availability(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT bed_type, bed_number, status, booked_by, booking_duration, booking_time FROM beds")
            beds = cursor.fetchall()

            bed_availability = {
                'Luxury Bed': {i: (0, None, None, None) for i in range(1, 11)},
                'AC Bed': {i: (0, None, None, None) for i in range(1, 11)},
                'Normal Bed': {i: (0, None, None, None) for i in range(1, 11)}
            }

            for bed_type, bed_number, status, booked_by, booking_duration, booking_time in beds:
                bed_availability[bed_type][bed_number] = (status, booked_by, booking_duration, booking_time)

            return bed_availability
    
    def book_bed(self, bed_type=None, bed_number=None):
            if bed_type is None or bed_number is None:
                bed_type = simpledialog.askstring("Book a Bed", "Enter bed type (Luxury Bed, AC Bed, Normal Bed):")
                bed_number = simpledialog.askinteger("Book a Bed", "Enter bed number (1-10):")

            if not bed_type or not bed_number:
                messagebox.showerror("Error", "Both bed type and bed number are required.")
                return

            booking_duration = simpledialog.askinteger("Book a Bed", "Enter booking duration (in days):")

            if not booking_duration:
                messagebox.showerror("Error", "Booking duration is required.")
                return

            cursor = self.conn.cursor()
            cursor.execute("SELECT status, booked_by FROM beds WHERE bed_type = ? AND bed_number = ?", (bed_type, bed_number))
            bed_data = cursor.fetchone()

            if not bed_data:
                messagebox.showerror("Error", "Invalid bed type or bed number.")
                return

            status, booked_by = bed_data

            if status == 0:
                cursor.execute("UPDATE beds SET status = 1, booked_by = ?, booking_duration = ?, booking_time = ? WHERE bed_type = ? AND bed_number = ?",
                (self.current_user, booking_duration, datetime.now(), bed_type, bed_number))

                self.conn.commit()
                messagebox.showinfo("Success", f"{bed_type} {bed_number} booked successfully for {booking_duration} days.")
                self.show_booking_page()
            else:
                messagebox.showerror("Error", f"{bed_type} {bed_number} is already booked by {booked_by}.")

    def book_bed_from_availability(self, bed_type, bed_number):
        self.book_bed(bed_type, bed_number)

    def view_bed_availability(self):
        self.show_availability_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
