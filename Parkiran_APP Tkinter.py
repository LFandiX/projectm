import tkinter as tk
from tkinter import messagebox, StringVar, Label, Entry, Radiobutton, Frame, OptionMenu, Button, ttk
import mysql.connector


class App(tk.Tk):
    """
    A class used to represent the main application window.
    Methods
    -------
    __init__():
        Initializes the main application window, sets up frames, and shows the login page.
    center_window():
        Centers the application window on the screen.
    connect_db():
        Connects to the MySQL database.
    load_admin():
        Loads admin data from the database.
    show_frame(cont):
        Displays the specified frame.
    login(username, password):
        Handles login authentication.
    create_navbar():
        Creates the navigation bar.
    logout():
        Handles logout.
    """

    def __init__(self):
        super().__init__()
        self.title("Parkiran CIT")
        self.geometry("800x600")
        self.center_window()
        self.position = ''

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.auth_required = [HomePage, AddMemberPage, ViewMemberPage, ViewMembershipPage,EditData,EditMembership,EditAdmin]

        for F in (LoginPage, HomePage, AddMemberPage, ViewMemberPage, ViewMembershipPage,EditData,EditMembership,EditAdmin):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)
        self.is_authenticated = False

    def center_window(self):
        """Center the window on the screen"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.geometry(f'800x600+{x}+{y}')

    def connect_db(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='FNDDatabase.1',
            database='parkiran_DB'
        )
    def fetch_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def update_data(self, member_id, updates):
        conn = self.connect_db()
        cursor = conn.cursor()
        set_clause = ", ".join(f"{field} = %s" for field in updates.keys())
        values = list(updates.values()) + [member_id]
        query = f"UPDATE members  SET {set_clause} WHERE ID = %s"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

    def delete_data(self, member_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Vehicles WHERE Member_ID = %s", (member_id,))
        cursor.execute("DELETE FROM Member WHERE ID = %s", (member_id,))
        conn.commit()
        cursor.close()
        conn.close()
    def load_admin(self):
        db = self.connect_db()
        cursor = db.cursor()
        query = 'SELECT * FROM admins;'
        cursor.execute(query)
        admins = cursor.fetchall()
        db.close()
        return admins

    def load_members(self):
        db = self.connect_db()
        cursor = db.cursor()
        query = 'SELECT * FROM members;'
        cursor.execute(query)
        members = cursor.fetchall()
        db.close()
        return members

    def load_members2(self):
        db = self.connect_db()
        cursor = db.cursor()
        query = """
            SELECT members.first_name, members.last_name,kendaraan.tipe, kendaraan.no_polisi,  kategori.kategori
            FROM members
            JOIN kendaraan ON (members.id_member = kendaraan.id_member)
            JOIN kategori ON (kendaraan.id_kategori = kategori.id)
            JOIN payment ON (payment.id_kategori = kategori.id);
           """
        cursor.execute(query)
        members = cursor.fetchall()
        db.close()
        return members

    def load_subscription_types(self):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT ID, Kategori, Durasi, Harga FROM TipeLangganan")
        subscriptions = cursor.fetchall()
        db.close()
        return subscriptions

    def show_frame(self, cont):
        """Show the specified frame"""
        if cont in self.auth_required and not self.is_authenticated:
            messagebox.showerror("Error", "Please login first!")
            self.show_frame(LoginPage)
            return
        frame = self.frames[cont]
        frame.tkraise()

    def login(self, username, password):
        """Handle login authentication"""
        admins = self.load_admin()
        for admin in admins:
            if username == admin[2] and password == admin[3]:
                self.is_authenticated = True
                self.create_navbar()
                self.position = admin[4]
                self.show_frame(HomePage)
                return
        messagebox.showerror("Error", "Invalid username or password!")

    def create_navbar(self):
        """Create navigation bar"""
        self.navbar = tk.Frame(self, bg='#2c3e50')
        self.navbar.pack(side='top', fill='x')

        # Navigation buttons
        btn_home = tk.Button(self.navbar, text="Home",
                             command=lambda: self.show_frame(HomePage),
                             bg='#2c3e50', fg='white', bd=0, padx=20, pady=10)
        btn_home.pack(side='left')

        btn_profile = tk.Button(self.navbar, text="Viwe Member",
                                command=lambda: self.show_frame(ViewMemberPage),
                                bg='#2c3e50', fg='white', bd=0, padx=20, pady=10)
        btn_profile.pack(side='left')

        btn_settings = tk.Button(self.navbar, text="Settings",
                                 command=lambda: self.show_frame(ViewMembershipPage),
                                 bg='#2c3e50', fg='white', bd=0, padx=20, pady=10)
        btn_settings.pack(side='left')

        # Logout button
        btn_logout = tk.Button(self.navbar, text="Logout",
                               command=self.logout,
                               bg='#e74c3c', fg='white', bd=0, padx=20, pady=10)
        btn_logout.pack(side='right')

    def logout(self):
        """Handle logout"""
        self.is_authenticated = False
        if hasattr(self, 'navbar'):
            self.navbar.destroy()
        self.show_frame(LoginPage)


class HomePage(tk.Frame):
    """
    A class used to represent the Home Page of the application.
    Attributes
    ----------
    controller : tk.Tk
        The main controller that manages the frames of the application.
    Methods
    -------
    __init__(parent, controller)
        Initializes the HomePage frame with a title and a content frame.
    create_card(parent, title, row, col, frame_class)
        Creates a card with a title and a button that navigates to the specified frame.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

        title = tk.Label(self, text="Welcome back to Dashboard!", font=('Helvetica', 24, 'bold'), bg='white')
        title.pack(pady=20)

        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(pady=20, padx=20)

        self.create_card(content_frame, "ADD MEMBER", 0, 0, AddMemberPage)
        self.create_card(content_frame, "EDIT DATA", 1, 0, EditData)
        self.create_card(content_frame, "EDIT MEMBERSHIP", 2, 0, EditMembership)
        self.create_card(content_frame, "VIEW MEMBER", 0, 1, ViewMemberPage)
        self.create_card(content_frame, "VIEW MEMBERSHIP", 1, 1, ViewMembershipPage)
        self.admin_card(content_frame, "EDIT ADMIN", 2, 1)

    def create_card(self, parent, title, row, col, frame_class):
        card = tk.Frame(parent, bg='#f8f9fa', padx=20, pady=20)
        card.grid(row=row, column=col, pady=10, padx=10, sticky='ew')

        tk.Label(card, text=title, font=('Helvetica', 16, 'bold'), bg='#f8f9fa').pack()
        tk.Button(card, text="Go", bg='#007bff', fg='white', padx=10, pady=5,
                  command=lambda: self.controller.show_frame(frame_class)).pack()
    def admin_card(self, parent, title, row, col):
        card = tk.Frame(parent, bg='#f8f9fa', padx=20, pady=20)
        card.grid(row=row, column=col, pady=10, padx=10, sticky='ew')

        tk.Label(card, text=title, font=('Helvetica', 16, 'bold'), bg='#f8f9fa').pack()
        tk.Button(card, text="Go", bg='#007bff', fg='white', padx=10, pady=5, command=self.look).pack()

    def look(self):
        if self.controller.position == 'Admin':
            self.controller.show_frame(EditAdmin).pack()
        else:
            messagebox.showerror("Error", "Jadi Boss dulu dek")



class AddMemberPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

        tk.Label(self, text="Add Member", font=('Helvetica', 20), bg='white').grid(row=0, column=1, pady=10)

        self.create_form(parent)

        self.create_submit_button()

    def create_form(self, parent):
        """Create form fields for member data input"""
        self.FirstNameEntry = self.create_entry("First Name", 2)
        self.LastNameEntry = self.create_entry("Last Name", 3)
        self.AlamatEntry = self.create_entry("Alamat", 4)

        self.KategoriRadioButton = StringVar()
        self.KategoriRadioButton.set("Mobil")
        Label(self, text="Kategori", bg='white').grid(row=5, column=0, padx=10, pady=5)
        Radiobutton(self, text="Mobil", variable=self.KategoriRadioButton, value="Mobil", bg='white').grid(row=5,
                                                                                                           column=1,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky='w')
        Radiobutton(self, text="Motor", variable=self.KategoriRadioButton, value="Motor", bg='white').grid(row=5,
                                                                                                           column=2,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky='w')

        self.TKendaraanEntry = self.create_entry("Tipe Kendaraan", 6)
        self.NoPolisiEntry = self.create_entry("No Polisi", 7)

        self.MembershipOptionMennu = StringVar(value="12 Bulan")
        MembershipList = ["1 Bulan", "3 Bulan", "6 Bulan", "12 Bulan"]
        Label(self, text="Membership Time", bg='white').grid(row=9, column=0, padx=10, pady=5)
        option = OptionMenu(self, self.MembershipOptionMennu, *MembershipList)
        option.config(bg='white', width=15)
        option.grid(row=9, column=1, padx=10, pady=5)

    def create_entry(self, label_text, row):
        Label(self, text=label_text, bg='white').grid(row=row, column=0, padx=10, pady=5)
        entry = Entry(self, font=("Italic", 12))
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def create_submit_button(self):
        self.create_table()
        Button(self, text="Submit", font=("Italic", 12, "bold"), command=self.submit_data).grid(row=10, column=0,
                                                                                                padx=10, pady=5)

    def create_table(self):
        self.TableFrame = Frame(self)
        self.TableFrame.grid(row=11, column=0, columnspan=3, padx=10, pady=10)
        data = [
            ("Mobil", "1 Bulan", "29.900"),
            ("Mobil", "3 Bulan", "79.900"),
            ("Mobil", "6 Bulan", "164.900"),
            ("Motor", "1 Bulan", "49.900"),
            ("Motor", "3 Bulan", "144.900"),
            ("Motor", "6 Bulan", "279.900"),
        ]
        Label(self.TableFrame, text="Kategori", font=("Italic", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        Label(self.TableFrame, text="Membership Time", font=("Italic", 12, "bold")).grid(row=0, column=1, padx=5,
                                                                                         pady=5)
        Label(self.TableFrame, text="Price", font=("Italic", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)
        for idx, (kategori, membership_time, price) in enumerate(data, start=1):
            Label(self.TableFrame, text=kategori, font=("Italic", 10)).grid(row=idx, column=0, padx=5, pady=5)
            Label(self.TableFrame, text=membership_time, font=("Italic", 10)).grid(row=idx, column=1, padx=5, pady=5)
            Label(self.TableFrame, text=price, font=("Italic", 10)).grid(row=idx, column=2, padx=5, pady=5)

    def submit_data(self):
        user_data = {
            "First Name": self.FirstNameEntry.get(),
            "Last Name": self.LastNameEntry.get(),
            "Alamat": self.AlamatEntry.get(),
            "Kategori": self.KategoriRadioButton.get(),
            "Tipe Kendaraan": self.TKendaraanEntry.get(),
            "No Polisi": self.NoPolisiEntry.get(),
            "Membership Time": self.MembershipOptionMennu.get()
        }

        # db = self.controller.connect_db()
        # cursor = db.cursor()
        # query = '''
        #     INSERT INTO members (first_name, last_name, alamat, kategori, tipe_kendaraan, no_polisi, membership_time)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s)
        # '''
        # values = (user_data["First Name"], user_data["Last Name"], user_data["Alamat"],
        #           user_data["Kategori"], user_data["Tipe Kendaraan"], user_data["No Polisi"],
        #           user_data["Membership Time"])
        # cursor.execute(query, values)
        # db.commit()
        # db.close()

        messagebox.showinfo("Success", "Member added successfully!")


class ViewMemberPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

        title = tk.Label(self, text="View Member", font=('Helvetica', 20), bg='white').grid(row=0, column=1, pady=10)
        content_frame = tk.Frame(self, bg='white').grid(row=1, column=0, padx=10, pady=10)

        self.create_table()

    def create_table(self):
        self.TableFrame = Frame(self)
        JudulLabel = Label(self, text="Member List", font=("Italic", 16, "bold"))

        JudulLabel.grid(row=1, column=0, columnspan=7, pady=10)

        self.TableFrame = Frame(self)
        self.TableFrame.grid(row=1, column=0, padx=10, pady=10, columnspan=7)
        self.RefreshButton = Button(self, text="Refresh", font=("Italic", 12),
                                    command=self.display_members)  # .grid(row=2, column=0, pady=10)
        self.RefreshButton.grid(row=2, column=0, pady=10)
        self.display_members()

    def display_members(self):
        # pass
        for widget in self.TableFrame.winfo_children():
            widget.destroy()

        # self.TableFrame = Frame(self)
        informasi = self.controller.load_members()
        # print(informasi)
        headers = ["ID", "First Name", "Last Name", "Alamat", "Kategori", "Tipe Kendaraan", "No Polisi"]
        for col, header in enumerate(headers):
            Label(self.TableFrame, text=header, font=("Italic", 12, "bold"), borderwidth=1, width=15, anchor="w").grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1)

        for idx, member in enumerate(informasi, start=1):
            values = [idx] + list(member)
            for col, value in enumerate(values):
                Label(self.TableFrame, text=value, font=("Italic", 10), borderwidth=1, width=15, anchor="w").grid(
                    row=idx, column=col, sticky="nsew", padx=1, pady=1)


class ViewMembershipPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

        title = tk.Label(self, text="View Membership", font=('Helvetica', 20), bg='white').grid(row=0, column=1, pady=10)
        content_frame = tk.Frame(self, bg='white').grid(row=1, column=0, padx=10, pady=10)

        self.create_table()

    def create_table(self):
        self.TableFrame = Frame(self)
        JudulLabel = Label(self, text="Member List", font=("Italic", 16, "bold"))

        JudulLabel.grid(row=1, column=0, columnspan=7, pady=10)

        self.TableFrame = Frame(self)
        self.TableFrame.grid(row=1, column=0, padx=10, pady=10, columnspan=7)
        self.RefreshButton = Button(self, text="Refresh", font=("Italic", 12),
                                    command=self.display_members)  # .grid(row=2, column=0, pady=10)
        self.RefreshButton.grid(row=2, column=0, pady=10)
        self.display_members()

    def display_members(self):
        # pass
        for widget in self.TableFrame.winfo_children():
            widget.destroy()

        # self.TableFrame = Frame(self)
        informasi = self.controller.load_members()
        # print(informasi)
        headers = ["ID", "First Name", "Last Name", "Alamat", "Kategori", "Tipe Kendaraan", "No Polisi"]
        for col, header in enumerate(headers):
            Label(self.TableFrame, text=header, font=("Italic", 12, "bold"), borderwidth=1, width=15, anchor="w").grid(
                row=0, column=col, sticky="nsew", padx=1, pady=1)

        for idx, member in enumerate(informasi, start=1):
            values = [idx] + list(member)
            for col, value in enumerate(values):
                Label(self.TableFrame, text=value, font=("Italic", 10), borderwidth=1, width=15, anchor="w").grid(
                    row=idx, column=col, sticky="nsew", padx=1, pady=1)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

        login_frame = tk.Frame(self, bg='white', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="Welcome Back!", font=('Helvetica', 24, 'bold'), bg='white').pack(pady=(0, 20))

        tk.Label(login_frame, text="Username", bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=(5, 15), ipady=8)

        tk.Label(login_frame, text="Password", bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(login_frame, width=30, show="•")
        self.password_entry.pack(pady=(5, 15), ipady=8)

        login_btn = tk.Button(login_frame, text="Login", command=self.login, bg='#007bff', fg='white', width=25, pady=8)
        login_btn.pack(pady=(15, 0))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(username, password)
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        self.controller.login(username, password)



class EditData(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="Edit Data Member", font=("Arial", 20), bg="white").pack(pady=10)

        # Table frame
        frame_table = tk.Frame(self, bg="white")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID", "First_name", "Last_name", "Email", "Phone_num", "Address", "Start_date", "End_date", "Duration"]
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Buttons frame
        frame_buttons = tk.Frame(self, bg="white")
        frame_buttons.pack(pady=10)

        btn_update = tk.Button(frame_buttons, text="Update Data", command=self.on_update, bg="#007bff", fg="white")
        btn_update.pack(side="left", padx=5)

        btn_remove = tk.Button(frame_buttons, text="Remove Data", command=self.on_remove, bg="#dc3545", fg="white")
        btn_remove.pack(side="left", padx=5)

        self.frame_update = tk.Frame(self, bg="white")

        self.display_data()


    def display_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = self.controller.fetch_data()
        for row in data:
            self.tree.insert("", "end", values=row)

    def update_form(self, selected_data):
        for widget in self.frame_update.winfo_children():
            widget.destroy()

        entries = {}
        member_id = selected_data[0]
        fields = ["First_name", "Last_name", "Email", "Phone_num", "Address", "Start_date", "End_date", "Duration"]

        tk.Label(self.frame_update, text="Update Data Member", font=("Arial", 14), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        for i, (field, value) in enumerate(zip(fields, selected_data[1:]), start=1):
            tk.Label(self.frame_update, text=field, bg="white").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(self.frame_update)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        def save_changes():
            updates = {field: entry.get() for field, entry in entries.items()}
            self.controller.update_data(member_id, updates)
            self.display_data()
            self.frame_update.pack_forget()
            messagebox.showinfo("Update", "Data berhasil diperbarui")

        tk.Button(self.frame_update, text="Save Changes", command=save_changes, bg="#28a745", fg="white").grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
        self.frame_update.pack(fill="x", padx=10, pady=10)

    def on_update(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih data untuk diupdate")
            return

        selected_data = self.tree.item(selected_item[0])["values"]
        self.update_form(selected_data)

    def on_remove(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih data untuk dihapus")
            return

        response = messagebox.askyesno("Confirmation", "Apakah Anda yakin ingin menghapus data ini beserta data terkait?")
        if response:
            selected_data = self.tree.item(selected_item[0])["values"]
            member_id = selected_data[0]
            self.controller.delete_data(member_id)
            self.display_data()
            messagebox.showinfo("Remove", "Data berhasil dihapus")


class EditMembership(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        self.controller.title("Update Data Membership")
        self.controller.state("zoomed")

        self.members = []
        self.subscriptions = []
        self.subscription_var = tk.StringVar()

        self.setup_ui()
        self.load_data()





    def update_subscription(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Pilih member terlebih dahulu!")
            return

        selected_member = self.tree.item(selected_item)['values'][0]
        selected_subscription_id = self.subscription_var.get()

        db = self.controller.connect_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE Payment SET ID_TipeLangganan = %s WHERE ID_Member = %s",
                (selected_subscription_id, selected_member)
            )
            db.commit()
            self.status_label.config(text="Subscription updated successfully", fg="green")
        except Exception as e:
            db.rollback()
            self.status_label.config(text=f"Error: {e}", fg="red")
        finally:
            db.close()

    def search_member(self):
        search_term = self.search_entry.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for member in self.members:
            full_name = f"{member[1]} {member[2]}"
            if search_term in full_name.lower():
                self.tree.insert("", "end", values=member)

    def setup_ui(self):
        # Title
        tk.Label(self, text="Update Data Membership", font=("Arial", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10, sticky="w"
        )

        # Search bar
        tk.Label(self, text="Search Member:").grid(row=1, column=0, sticky="w", padx=20)
        self.search_entry = tk.Entry(self, width=40)
        self.search_entry.grid(row=1, column=0, padx=(120, 0), pady=5)
        search_button = tk.Button(self, text="Search", command=self.search_member)
        search_button.grid(row=1, column=0, padx=(400, 0), pady=5)

        # Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "First_name", "Last_name", "Start_date", "End_date", "No_Polisi", "Kategori"),
            show="headings",
            height=20
        )
        self.tree.grid(row=2, column=0, padx=20, pady=10, sticky="nsw")

        for col in ("ID", "First_name", "Last_name", "Start_date", "End_date", "No_Polisi", "Kategori"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "ID" else 30)

        # Subscription frame
        self.subscription_frame = tk.Frame(self)
        self.subscription_frame.grid(row=2, column=1, padx=20, pady=10, sticky="ns")

        tk.Label(self.subscription_frame, text="Pilihan Langganan:", font=("Arial", 14)).pack(anchor="w", pady=(0, 10))





        self.status_label = tk.Label(self.subscription_frame, text="")
        self.status_label.pack()


    def load_data(self):
        self.members = self.controller.load_members2()
        self.subscriptions = self.controller.load_subscription_types()

        # Populate treeview
        for member in self.members:
            self.tree.insert("", "end", values=member)

        # Populate subscription options
        for subscription in self.subscriptions:
            radio_text = f"{subscription[1]} ({subscription[2]} bulan) - Rp{subscription[3]}"
            radio_button = tk.Radiobutton(
                self.subscription_frame,
                text=radio_text,
                variable=self.subscription_var,
                value=subscription[0]
            )
            radio_button.pack(anchor="w")
        self.subscription_var = tk.StringVar()
        update_button = tk.Button(self.subscription_frame, text="Update", command=self.update_subscription)
        update_button.pack(pady=20)


class EditAdmin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")




app = App()
app.mainloop()
