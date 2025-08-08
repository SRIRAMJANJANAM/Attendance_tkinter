import tkinter as tk
from tkinter import ttk, simpledialog
import csv
from datetime import datetime

class AttendanceBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Bot")
        self.root.geometry("400x450")
        self.students = []
        self.attendance = {}
        self.date = datetime.now().strftime("%Y-%m-%d")

        # Title
        title = tk.Label(root, text="Attendance Bot", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        # Frame for student list and scrollbar
        list_frame = tk.Frame(root)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.student_label = tk.Label(list_frame, text="Students:", font=("Helvetica", 12))
        self.student_label.pack(anchor="w")

        self.listbox = tk.Listbox(list_frame, height=12, font=("Helvetica", 11))
        self.listbox.pack(side="left", fill="both", expand=True, pady=5)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Frame for buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(padx=20, pady=10, fill="x")

        btn_opts = {"font": ("Helvetica", 11), "bd": 0, "activebackground": "#555", "fg": "white"}

        self.add_btn = tk.Button(btn_frame, text="Add Student", bg="#4CAF50", **btn_opts, command=self.add_student)
        self.add_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.mark_btn = tk.Button(btn_frame, text="Mark Attendance", bg="#2196F3", **btn_opts, command=self.mark_attendance)
        self.mark_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.show_btn = tk.Button(btn_frame, text="Show Attendance", bg="#FF9800", **btn_opts, command=self.show_attendance)
        self.show_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.export_btn = tk.Button(root, text="Export to CSV", bg="#9C27B0", fg="white", font=("Helvetica", 11), bd=0, activebackground="#7B1FA2", command=self.export_csv)
        self.export_btn.pack(padx=20, pady=10, fill="x")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome! Add students to start.")
        self.status_label = tk.Label(root, textvariable=self.status_var, relief="sunken", anchor="w", font=("Helvetica", 10))
        self.status_label.pack(side="bottom", fill="x")

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter student name:", parent=self.root)
        if name:
            if name not in self.students:
                self.students.append(name)
                self.listbox.insert(tk.END, name)
                self.set_status(f"Student '{name}' added.", "green")
            else:
                self.set_status(f"Student '{name}' already exists.", "orange")

    def mark_attendance(self):
        selected = self.listbox.curselection()
        if not selected:
            self.set_status("Please select a student to mark attendance.", "red")
            return
        name = self.listbox.get(selected[0])
        if self.date not in self.attendance:
            self.attendance[self.date] = []
        if name not in self.attendance[self.date]:
            self.attendance[self.date].append(name)
            self.set_status(f"Attendance marked for {name} on {self.date}", "green")
        else:
            self.set_status(f"Attendance already marked for {name} today.", "orange")

    def show_attendance(self):
        if self.date in self.attendance and self.attendance[self.date]:
            names = "\n".join(self.attendance[self.date])
            message = f"Attendance on {self.date}:\n\n{names}"
        else:
            message = f"No attendance marked for {self.date} yet."
        self.popup_message("Today's Attendance", message)

    def export_csv(self):
        filename = f"attendance_{self.date}.csv"
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Student Name"])
                for date, names in self.attendance.items():
                    for name in names:
                        writer.writerow([date, name])
            self.set_status(f"Attendance exported to '{filename}'.", "green")
        except Exception as e:
            self.set_status(f"Error exporting file: {e}", "red")

    def set_status(self, message, color="black"):
        self.status_var.set(message)
        self.status_label.config(fg=color)

    def popup_message(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x300")
        popup.resizable(False, False)
        tk.Label(popup, text=message, justify="left", font=("Helvetica", 11)).pack(padx=15, pady=15)
        tk.Button(popup, text="Close", command=popup.destroy, bg="#2196F3", fg="white", bd=0, font=("Helvetica", 11)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceBotGUI(root)
    root.mainloop()




