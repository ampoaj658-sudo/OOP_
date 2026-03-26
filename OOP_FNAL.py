import json
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG      = "#F5F5F5"
CARD    = "#FFFFFF"
SIDEBAR = "#EEEEEE"
ACCENT  = "#AC0F0F"
HOVER   = "#7A0000"
HOVER2   = "#8A8686"
TXT     = "#1A1A1A"
SUBTXT  = "#666666"
BORDER  = "#DDDDDD"

window = ctk.CTk()
window.title("MediTrack")
window.geometry("500x540")
window.configure(fg_color=BG)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)


# ═══════════════════════════════════════════════════
#  MODEL LAYER
# ═══════════════════════════════════════════════════

class AdminUser():
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role     = role

    def get_username(self):  return self.__username
    def get_password(self):  return self.__password
    def get_role(self):      return self.__role

    def check_password(self, input_password):
        return input_password == self.__password


class Person():
    def __init__(self, person_id, first_name, last_name, contact):
        self.__person_id  = person_id
        self.__first_name = first_name
        self.__last_name  = last_name
        self.__contact    = contact

    def get_person_id(self):     return self.__person_id
    def get_first_name(self):    return self.__first_name
    def get_last_name(self):     return self.__last_name
    def get_contact(self):       return self.__contact
    def get_full_name(self):     return f"{self.__first_name} {self.__last_name}"
    def set_first_name(self, v): self.__first_name = v
    def set_last_name(self, v):  self.__last_name  = v
    def set_contact(self, v):    self.__contact    = v


class Patient(Person):
    def __init__(self, person_id, first_name, last_name, contact, birthdate, address):
        super().__init__(person_id, first_name, last_name, contact)
        self.__birthdate = birthdate
        self.__address   = address

    def get_birthdate(self):    return self.__birthdate
    def get_address(self):      return self.__address
    def set_birthdate(self, v): self.__birthdate = v
    def set_address(self, v):   self.__address   = v


class Doctor(Person):
    def __init__(self, person_id, first_name, last_name, contact, specialty, schedule):
        super().__init__(person_id, first_name, last_name, contact)
        self.__specialty = specialty
        self.__schedule  = schedule

    def get_specialty(self):    return self.__specialty
    def get_schedule(self):     return self.__schedule
    def set_specialty(self, v): self.__specialty = v
    def set_schedule(self, v):  self.__schedule  = v


class MedicalRecord():
    def __init__(self, record_id, patient_id, doctor_id, diagnosis, notes):
        self.__record_id  = record_id
        self.__patient_id = patient_id
        self.__doctor_id  = doctor_id
        self.__diagnosis  = diagnosis
        self.__notes      = notes

    def get_record_id(self):    return self.__record_id
    def get_patient_id(self):   return self.__patient_id
    def get_doctor_id(self):    return self.__doctor_id
    def get_diagnosis(self):    return self.__diagnosis
    def get_notes(self):        return self.__notes
    def set_diagnosis(self, v): self.__diagnosis = v
    def set_notes(self, v):     self.__notes     = v


# ── Data ───────────────────────────────────────────
admin    = AdminUser("admin", "admin123", "Administrator")
patients = []
doctors  = []
records  = []
DATABASE_FILE = "meditrack_data.json"

# ═══════════════════════════════════════════════════
#  SAVE DATA
# ═══════════════════════════════════════════════════
def save_data():
    data = {
        "patients": [
            {
                "id": p.get_person_id(),
                "first": p.get_first_name(),
                "last": p.get_last_name(),
                "contact": p.get_contact(),
                "birth": p.get_birthdate(),
                "address": p.get_address()
            } for p in patients
        ],
        "doctors": [
            {
                "id": d.get_person_id(),
                "first": d.get_first_name(),
                "last": d.get_last_name(),
                "contact": d.get_contact(),
                "spec": d.get_specialty(),
                "sched": d.get_schedule()
            } for d in doctors
        ],
        "records": [
            {
                "id": r.get_record_id(),
                "patient_id": r.get_patient_id(),
                "doctor_id": r.get_doctor_id(),
                "diagnosis": r.get_diagnosis(),
                "notes": r.get_notes()
            } for r in records
        ]
    }

    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    global patients, doctors, records
    try:
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)

            for p in data.get("patients", []):
                patients.append(Patient(p["id"], p["first"], p["last"],
                                        p["contact"], p["birth"], p["address"]))

            for d in data.get("doctors", []):
                doctors.append(Doctor(d["id"], d["first"], d["last"],
                                      d["contact"], d["spec"], d["sched"]))

            for r in data.get("records", []):
                records.append(MedicalRecord(r["id"], r["patient_id"],
                                             r["doctor_id"], r["diagnosis"], r["notes"]))
    except FileNotFoundError:
        pass

# ═══════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════
def make_row(parent, label_text, btn_cmds):
    row = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=8,
                       border_width=1, border_color=BORDER)
    row.pack(fill="x", padx=10, pady=4)
    ctk.CTkLabel(row, text=label_text, text_color=TXT,
                 font=("Open Sans", 12), anchor="w").pack(side="left", padx=12, pady=10)
    for (btn_text, cmd, color) in btn_cmds:
        ctk.CTkButton(row, text=btn_text, width=60, height=28,
                      fg_color=color, hover_color=HOVER2,
                      command=cmd).pack(side="right", padx=4, pady=6)


# ═══════════════════════════════════════════════════
#  LOGIN
# ═══════════════════════════════════════════════════
def login():
    entered_username = userEnter.get()
    entered_password = passEnter.get()
    try:
        if not entered_username or not entered_password:
            raise ValueError("Please fill in all fields.")
        if entered_username == admin.get_username() and admin.check_password(entered_password):
            window.withdraw()
            open_dashboard()
        else:
            raise ValueError("Invalid username or password.")
    except ValueError as e:
        error_label.configure(text=str(e))


# ═══════════════════════════════════════════════════
#  PATIENTS
# ═══════════════════════════════════════════════════
def open_patients(content):
    for w in content.winfo_children(): w.destroy()
    ctk.CTkLabel(content, text="Patients", font=("Open Sans", 22, "bold"),
                 text_color=TXT).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(content, text=f"{len(patients)} patient(s) registered",
                 font=("Open Sans", 11), text_color=SUBTXT).pack(anchor="w", padx=15)
    ctk.CTkButton(content, text="+ Add Patient", width=140, fg_color=ACCENT, hover_color=HOVER,
                  command=lambda: add_patient_dialog(content)).pack(anchor="w", padx=15, pady=10)
    scroll = ctk.CTkScrollableFrame(content, fg_color=BG)
    scroll.pack(fill="both", expand=True, padx=10, pady=5)
    for p in patients:
        make_row(scroll,
                 f"{p.get_person_id()}  |  {p.get_full_name()}  |  {p.get_contact()}",
                 [("View",   lambda p=p: view_patient(p),                 "#4A90D9"),
                  ("Edit",   lambda p=p: edit_patient_dialog(content, p), "#F0A500"),
                  ("Delete", lambda p=p: delete_patient(content, p),      "#D9534F")])


def add_patient_dialog(content):
    dialog = ctk.CTkToplevel()
    dialog.title("Add New Patient")
    dialog.geometry("420x480")
    dialog.configure(fg_color=BG)
    fields = {}
    for label in ["First Name", "Last Name", "Contact", "Birthdate (YYYY-MM-DD)", "Address"]:
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(10, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            vals = {k: v.get().strip() for k, v in fields.items()}
            if any(v == "" for v in vals.values()):
                raise ValueError("All fields are required.")
            pid = f"P{len(patients)+1:03d}"
            patients.append(Patient(pid, vals["First Name"], vals["Last Name"],
                                    vals["Contact"], vals["Birthdate (YYYY-MM-DD)"], vals["Address"]))
            save_data()
            dialog.destroy()
            open_patients(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save", fg_color=ACCENT, hover_color=HOVER, width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def edit_patient_dialog(content, patient):
    dialog = ctk.CTkToplevel()
    dialog.title("Edit Patient")
    dialog.geometry("420x480")
    dialog.configure(fg_color=BG)
    labels   = ["First Name", "Last Name", "Contact", "Birthdate", "Address"]
    defaults = [patient.get_first_name(), patient.get_last_name(), patient.get_contact(),
                patient.get_birthdate(), patient.get_address()]
    fields = {}
    for label, default in zip(labels, defaults):
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(10, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.insert(0, default)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            if any(v.get().strip() == "" for v in fields.values()):
                raise ValueError("All fields are required.")
            patient.set_first_name(fields["First Name"].get().strip())
            patient.set_last_name(fields["Last Name"].get().strip())
            patient.set_contact(fields["Contact"].get().strip())
            patient.set_birthdate(fields["Birthdate"].get().strip())
            patient.set_address(fields["Address"].get().strip())
            save_data()
            dialog.destroy()
            open_patients(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save Changes", fg_color=ACCENT, hover_color=HOVER,
                  width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def view_patient(patient):
    dialog = ctk.CTkToplevel()
    dialog.title("Patient Details")
    dialog.geometry("380x380")
    dialog.configure(fg_color=BG)
    ctk.CTkLabel(dialog, text="Patient Details", font=("Open Sans", 18, "bold"),
                 text_color=TXT).pack(pady=15)
    for label, value in [("ID", patient.get_person_id()), ("Full Name", patient.get_full_name()),
                          ("Contact", patient.get_contact()), ("Birthdate", patient.get_birthdate()),
                          ("Address", patient.get_address())]:
        row = ctk.CTkFrame(dialog, fg_color=CARD, corner_radius=6, border_width=1, border_color=BORDER)
        row.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(row, text=f"{label}:", font=("Open Sans", 11, "bold"),
                     text_color=SUBTXT, width=90, anchor="w").pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(row, text=value, text_color=TXT, font=("Open Sans", 11), anchor="w").pack(side="left")
    ctk.CTkButton(dialog, text="Close", fg_color=ACCENT, hover_color=HOVER2,
                  width=120, command=dialog.destroy).pack(pady=15)


def delete_patient(content, patient):
    if messagebox.askyesno("Delete", f"Delete {patient.get_full_name()}?"):
        patients.remove(patient)
        save_data()
        open_patients(content)


# ═══════════════════════════════════════════════════
#  DOCTORS
# ═══════════════════════════════════════════════════
def open_doctors(content):
    for w in content.winfo_children(): w.destroy()
    ctk.CTkLabel(content, text="Doctors", font=("Open Sans", 22, "bold"),
                 text_color=TXT).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(content, text=f"{len(doctors)} doctor(s) registered",
                 font=("Open Sans", 11), text_color=SUBTXT).pack(anchor="w", padx=15)
    ctk.CTkButton(content, text="+ Add Doctor", width=140, fg_color=ACCENT, hover_color=HOVER,
                  command=lambda: add_doctor_dialog(content)).pack(anchor="w", padx=15, pady=10)
    scroll = ctk.CTkScrollableFrame(content, fg_color=BG)
    scroll.pack(fill="both", expand=True, padx=10, pady=5)
    for d in doctors:
        make_row(scroll,
                 f"{d.get_person_id()}  |  {d.get_full_name()}  |  {d.get_specialty()}",
                 [("View",   lambda d=d: view_doctor(d),                 "#4A90D9"),
                  ("Edit",   lambda d=d: edit_doctor_dialog(content, d), "#F0A500"),
                  ("Delete", lambda d=d: delete_doctor(content, d),      "#D9534F")])


def add_doctor_dialog(content):
    dialog = ctk.CTkToplevel()
    dialog.title("Add New Doctor")
    dialog.geometry("420x460")
    dialog.configure(fg_color=BG)
    fields = {}
    for label in ["First Name", "Last Name", "Contact", "Specialty", "Schedule"]:
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(10, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            vals = {k: v.get().strip() for k, v in fields.items()}
            if any(v == "" for v in vals.values()):
                raise ValueError("All fields are required.")
            did = f"D{len(doctors)+1:03d}"
            doctors.append(Doctor(did, vals["First Name"], vals["Last Name"],
                                  vals["Contact"], vals["Specialty"], vals["Schedule"]))
            save_data()
            dialog.destroy()
            open_doctors(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save", fg_color=ACCENT, hover_color=HOVER, width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def edit_doctor_dialog(content, doctor):
    dialog = ctk.CTkToplevel()
    dialog.title("Edit Doctor")
    dialog.geometry("420x460")
    dialog.configure(fg_color=BG)
    labels   = ["First Name", "Last Name", "Contact", "Specialty", "Schedule"]
    defaults = [doctor.get_first_name(), doctor.get_last_name(), doctor.get_contact(),
                doctor.get_specialty(), doctor.get_schedule()]
    fields = {}
    for label, default in zip(labels, defaults):
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(10, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.insert(0, default)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            if any(v.get().strip() == "" for v in fields.values()):
                raise ValueError("All fields are required.")
            doctor.set_first_name(fields["First Name"].get().strip())
            doctor.set_last_name(fields["Last Name"].get().strip())
            doctor.set_contact(fields["Contact"].get().strip())
            doctor.set_specialty(fields["Specialty"].get().strip())
            doctor.set_schedule(fields["Schedule"].get().strip())
            save_data()
            dialog.destroy()
            open_doctors(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save Changes", fg_color=ACCENT, hover_color=HOVER,
                  width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def view_doctor(doctor):
    dialog = ctk.CTkToplevel()
    dialog.title("Doctor Details")
    dialog.geometry("380x360")
    dialog.configure(fg_color=BG)
    ctk.CTkLabel(dialog, text="Doctor Details", font=("Open Sans", 18, "bold"),
                 text_color=TXT).pack(pady=15)
    for label, value in [("ID", doctor.get_person_id()), ("Full Name", doctor.get_full_name()),
                          ("Contact", doctor.get_contact()), ("Specialty", doctor.get_specialty()),
                          ("Schedule", doctor.get_schedule())]:
        row = ctk.CTkFrame(dialog, fg_color=CARD, corner_radius=6, border_width=1, border_color=BORDER)
        row.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(row, text=f"{label}:", font=("Open Sans", 11, "bold"),
                     text_color=SUBTXT, width=90, anchor="w").pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(row, text=value, text_color=TXT, font=("Open Sans", 11), anchor="w").pack(side="left")
    ctk.CTkButton(dialog, text="Close", fg_color=ACCENT, hover_color=HOVER,
                  width=120, command=dialog.destroy).pack(pady=15)


def delete_doctor(content, doctor):
    if messagebox.askyesno("Delete", f"Delete Dr. {doctor.get_full_name()}?"):
        doctors.remove(doctor)
        save_data()
        open_doctors(content)


# ═══════════════════════════════════════════════════
#  MEDICAL RECORDS
# ═══════════════════════════════════════════════════
def open_records(content):
    for w in content.winfo_children(): w.destroy()
    ctk.CTkLabel(content, text="Medical Records", font=("Open Sans", 22, "bold"),
                 text_color=TXT).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(content, text=f"{len(records)} record(s) on file",
                 font=("Open Sans", 11), text_color=SUBTXT).pack(anchor="w", padx=15)
    ctk.CTkButton(content, text="+ Add Record", width=140, fg_color=ACCENT, hover_color=HOVER,
                  command=lambda: add_record_dialog(content)).pack(anchor="w", padx=15, pady=10)
    scroll = ctk.CTkScrollableFrame(content, fg_color=BG)
    scroll.pack(fill="both", expand=True, padx=10, pady=5)
    for r in records:
        pname = next((p.get_full_name() for p in patients if p.get_person_id() == r.get_patient_id()), "Unknown")
        dname = next((d.get_full_name() for d in doctors  if d.get_person_id() == r.get_doctor_id()),  "Unknown")
        make_row(scroll,
                 f"{r.get_record_id()}  |  {pname}  →  Dr. {dname}  |  {r.get_diagnosis()}",
                 [("View",   lambda r=r: view_record(r),                 "#4A90D9"),
                  ("Edit",   lambda r=r: edit_record_dialog(content, r), "#F0A500"),
                  ("Delete", lambda r=r: delete_record(content, r),      "#D9534F")])


def add_record_dialog(content):
    dialog = ctk.CTkToplevel()
    dialog.title("Add Medical Record")
    dialog.geometry("420x440")
    dialog.configure(fg_color=BG)
    fields = {}
    for label in ["Patient ID (e.g. P001)", "Doctor ID (e.g. D001)", "Diagnosis", "Notes"]:
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(10, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            pid  = fields["Patient ID (e.g. P001)"].get().strip()
            did  = fields["Doctor ID (e.g. D001)"].get().strip()
            diag = fields["Diagnosis"].get().strip()
            note = fields["Notes"].get().strip()
            if not pid or not did or not diag:
                raise ValueError("Patient ID, Doctor ID and Diagnosis are required.")
            if not any(p.get_person_id() == pid for p in patients):
                raise ValueError("Patient ID not found.")
            if not any(d.get_person_id() == did for d in doctors):
                raise ValueError("Doctor ID not found.")
            rid = f"R{len(records)+1:03d}"
            records.append(MedicalRecord(rid, pid, did, diag, note))
            save_data()
            dialog.destroy()
            open_records(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save", fg_color=ACCENT, hover_color=HOVER, width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def edit_record_dialog(content, record):
    dialog = ctk.CTkToplevel()
    dialog.title("Edit Record")
    dialog.geometry("420x340")
    dialog.configure(fg_color=BG)
    fields = {}
    for label, default in [("Diagnosis", record.get_diagnosis()), ("Notes", record.get_notes())]:
        ctk.CTkLabel(dialog, text=label, text_color=TXT).pack(pady=(15, 0))
        e = ctk.CTkEntry(dialog, width=320)
        e.insert(0, default)
        e.pack(pady=3)
        fields[label] = e
    err = ctk.CTkLabel(dialog, text="", text_color="red")
    err.pack()

    def save():
        try:
            if not fields["Diagnosis"].get().strip():
                raise ValueError("Diagnosis is required.")
            record.set_diagnosis(fields["Diagnosis"].get().strip())
            record.set_notes(fields["Notes"].get().strip())
            save_data()
            dialog.destroy()
            open_records(content)
        except ValueError as e:
            err.configure(text=str(e))

    ctk.CTkButton(dialog, text="Save Changes", fg_color=ACCENT, hover_color=HOVER,
                  width=160, command=save).pack(pady=15)
    ctk.CTkButton(dialog, text="Cancel", fg_color=BORDER, hover_color=HOVER2,
                  text_color=TXT, width=160, command=dialog.destroy).pack()


def view_record(record):
    dialog = ctk.CTkToplevel()
    dialog.title("Record Details")
    dialog.geometry("380x340")
    dialog.configure(fg_color=BG)
    ctk.CTkLabel(dialog, text="Record Details", font=("Open Sans", 18, "bold"),
                 text_color=TXT).pack(pady=15)
    pname = next((p.get_full_name() for p in patients if p.get_person_id() == record.get_patient_id()), "Unknown")
    dname = next((d.get_full_name() for d in doctors  if d.get_person_id() == record.get_doctor_id()),  "Unknown")
    for label, value in [("Record ID", record.get_record_id()), ("Patient", pname),
                          ("Doctor", f"Dr. {dname}"), ("Diagnosis", record.get_diagnosis()),
                          ("Notes", record.get_notes())]:
        row = ctk.CTkFrame(dialog, fg_color=CARD, corner_radius=6, border_width=1, border_color=BORDER)
        row.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(row, text=f"{label}:", font=("Open Sans", 11, "bold"),
                     text_color=SUBTXT, width=90, anchor="w").pack(side="left", padx=10, pady=8)
        ctk.CTkLabel(row, text=value, text_color=TXT, font=("Open Sans", 11),
                     anchor="w", wraplength=220).pack(side="left")
    ctk.CTkButton(dialog, text="Close", fg_color=ACCENT, hover_color=HOVER,
                  width=120, command=dialog.destroy).pack(pady=15)


def delete_record(content, record):
    if messagebox.askyesno("Delete", f"Delete record {record.get_record_id()}?"):
        records.remove(record)
        save_data()
        open_records(content)


# ═══════════════════════════════════════════════════
#  DASHBOARD HOME
# ═══════════════════════════════════════════════════
def open_home(content):
    for w in content.winfo_children(): w.destroy()
    ctk.CTkLabel(content, text=f"Welcome, {admin.get_username()}!",
                 font=("Open Sans", 22, "bold"), text_color=TXT).pack(anchor="w", padx=20, pady=(20, 5))
    ctk.CTkLabel(content, text="Here's a summary of your clinic.",
                 font=("Open Sans", 12), text_color=SUBTXT).pack(anchor="w", padx=20, pady=(0, 20))
    cards_frame = ctk.CTkFrame(content, fg_color="transparent")
    cards_frame.pack(fill="x", padx=20)
    for label, count, color in [("🧑‍⚕️  Patients", len(patients), "#D0E8FF"),
                                  ("👨‍⚕️  Doctors",  len(doctors),  "#D0FFE8"),
                                  ("📋  Records",  len(records),  "#FFF3D0")]:
        card = ctk.CTkFrame(cards_frame, fg_color=color, corner_radius=12, width=160, height=100)
        card.pack(side="left", padx=8, pady=5)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=str(count), font=("Open Sans", 32, "bold"), text_color=TXT).pack(pady=(15, 0))
        ctk.CTkLabel(card, text=label, font=("Open Sans", 12), text_color=SUBTXT).pack()


# ═══════════════════════════════════════════════════
#  DASHBOARD WINDOW
# ═══════════════════════════════════════════════════
def open_dashboard():
    dashboard = ctk.CTkToplevel()
    dashboard.title("MediTrack Dashboard")
    dashboard.geometry("900x650")
    dashboard.configure(fg_color=BG)

    sidebar = ctk.CTkFrame(dashboard, width=200, corner_radius=0, fg_color=SIDEBAR)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    ctk.CTkLabel(sidebar, text="🏥 MediTrack", font=("Open Sans", 18, "bold"),
                 text_color=ACCENT).pack(pady=30)

    content = ctk.CTkFrame(dashboard, fg_color=BG)
    content.pack(side="left", fill="both", expand=True)

    for label, cmd in [("🏠  Home",            lambda: open_home(content)),
                        ("🧑‍⚕️  Patients",       lambda: open_patients(content)),
                        ("👨‍⚕️  Doctors",        lambda: open_doctors(content)),
                        ("📋  Medical Records", lambda: open_records(content))]:
        ctk.CTkButton(sidebar, text=label, width=170, height=38,
                      fg_color="transparent", text_color=TXT,
                      hover_color=BORDER, anchor="w",
                      font=("Open Sans", 13), command=cmd).pack(pady=3, padx=10)
        
    def logout(db_window):
        db_window.destroy()  # Close the dashboard
        window.deiconify()   # Show the login window again
        # Optional: Clear the password field for security
        passEnter.delete(0, 'end')

    ctk.CTkButton(sidebar, text="🚪  Logout", width=170, height=38, fg_color="transparent",
                    text_color="#D9534F", hover_color=BORDER, anchor="w", 
                    font=("Open Sans", 13), 
                    command=lambda: logout(dashboard)).pack(side="bottom", pady=20, padx=10) 
    
    open_home(content)



# ═══════════════════════════════════════════════════
#  LOGIN WINDOW
# ═══════════════════════════════════════════════════
frame = ctk.CTkFrame(window, width=360, height=450, corner_radius=15,
                     fg_color=CARD, border_width=1, border_color=BORDER)

frame.grid(row=1, column=0, padx=20, pady=20, sticky="n") 
frame.grid_propagate(False)
frame.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(frame, text="🏥", font=("Open Sans", 36)).grid(row=0, column=0, pady=(30, 0))
ctk.CTkLabel(frame, text="MediTrack", font=("Open Sans", 26, "bold"),
             text_color=ACCENT).grid(row=1, column=0, pady=(0, 4))
ctk.CTkLabel(frame, text="Please sign in to continue",
             font=("Open Sans", 12), text_color=SUBTXT).grid(row=2, column=0, pady=(0, 20))

ctk.CTkLabel(frame, text="Username", anchor="w",
             text_color=TXT).grid(row=3, column=0, padx=50, pady=(0, 4), sticky="w")
userEnter = ctk.CTkEntry(frame, width=260, placeholder_text="Enter username")
userEnter.grid(row=4, column=0, padx=50)

ctk.CTkLabel(frame, text="Password", anchor="w",
             text_color=TXT).grid(row=5, column=0, padx=50, pady=(12, 4), sticky="w")
passEnter = ctk.CTkEntry(frame, width=260, show="*", placeholder_text="Enter password")
passEnter.grid(row=6, column=0, padx=50)

error_label = ctk.CTkLabel(frame, text="", text_color="red", font=("Open Sans", 11))
error_label.grid(row=8, column=0)

login_btn = ctk.CTkButton(frame, text="Login", width=260, fg_color=ACCENT,
                           hover_color=HOVER, command=login)
login_btn.grid(row=7, column=0, padx=50, pady=(20, 10))

ctk.CTkLabel(window, text="hint: admin / admin123", font=("Open Sans", 9),
             text_color=SUBTXT).grid(row=2, column=0, pady=(0, 10), sticky="n")

load_data()
window.mainloop()