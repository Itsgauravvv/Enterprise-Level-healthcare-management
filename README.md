# 🏥 Healthcare Management System Using Python

## 📌 Project Overview

The **Healthcare Management System** is a menu-driven Python application developed to manage patients, doctors, appointments, billing, and healthcare reports.

The project demonstrates core Python concepts such as:

* Functions
* User-defined Modules
* Lists
* Dictionaries
* Loops
* Conditional Statements
* Exception Handling
* Logging
* Input Validation
* Business Logic

This project does **not** use file handling, databases, classes, or external libraries. All data is stored temporarily in Python lists while the application is running.

---

# 📂 Project Structure

```text
healthcare_management_system/
│
├── main.py
├── data_store.py
├── logger_module.py
├── validation_module.py
├── patient_module.py
├── doctor_module.py
├── appointment_module.py
├── billing_module.py
├── report_module.py
└── README.md
```

---

# 🚀 Features

### 👤 Patient Management

* Register Patient
* View All Patients
* Search Patient
* Update Patient
* Delete Patient

### 👨‍⚕️ Doctor Management

* Add Doctor
* View All Doctors
* Search Doctor

### 📅 Appointment Management

* Book Appointment
* View All Appointments
* Cancel Appointment
* Complete Appointment

### 💰 Billing Management

* Generate Patient Bill
* View All Bills
* Search Patient Bills
* Update Payment Status

### 📊 Reports

* Patient Reports
* Doctor Reports
* Appointment Reports
* Billing Reports

---

# 🛠 Technologies Used

* Python 3.x
* Lists
* Dictionaries
* Functions
* User-defined Modules
* Logging
* Exception Handling

---

# 📋 Requirements

* Python 3.8 or above
* Visual Studio Code (Recommended)

---

# ▶️ How to Run

1. Download or clone the project.

2. Open the project folder in Visual Studio Code.

3. Open the integrated terminal.

4. Run the following command:

```bash
python main.py
```

If your system uses Python 3 explicitly:

```bash
python3 main.py
```

---

# 📌 Main Menu

```text
1. Register Patient
2. View All Patients
3. Search Patient
4. Update Patient
5. Delete Patient
6. Add Doctor
7. View All Doctors
8. Search Doctor
9. Book Appointment
10. View All Appointments
11. Cancel Appointment
12. Complete Appointment
13. Generate Patient Bill
14. View All Bills
15. Search Patient Bills
16. Update Payment Status
17. Healthcare Reports
18. Exit
```

---

# 📊 Data Storage

The application stores data using Python lists.

```python
patients = []
doctors = []
appointments = []
bills = []
```

Each record is stored as a dictionary.

---

# 📄 Modules

### `main.py`

Handles menu navigation and calls the required functions.

### `patient_module.py`

* Register Patient
* View Patients
* Search Patient
* Update Patient
* Delete Patient

### `doctor_module.py`

* Add Doctor
* View Doctors
* Search Doctor

### `appointment_module.py`

* Book Appointment
* View Appointments
* Cancel Appointment
* Complete Appointment

### `billing_module.py`

* Generate Bill
* View Bills
* Search Patient Bills
* Update Payment Status

### `report_module.py`

Generates:

* Patient Reports
* Doctor Reports
* Appointment Reports
* Billing Reports

### `validation_module.py`

Contains reusable validation functions.

### `logger_module.py`

Provides console logging using Python's `logging` module.

### `data_store.py`

Stores all application data in shared lists.

---

# ✅ Business Rules

* Duplicate IDs are not allowed.
* Appointment booking requires valid Patient and Doctor IDs.
* Doctors must be available to accept appointments.
* Appointment slots cannot be double-booked.
* Bills can only be generated for completed appointments.
* One bill is allowed per appointment.
* Charges cannot be negative.
* Discount cannot exceed the gross amount.
* Payment status must be either **Paid** or **Pending**.

---

# ⚠ Exception Handling

The project handles common exceptions including:

* ValueError
* TypeError
* IndexError
* KeyError
* ZeroDivisionError
* General Exception

The application continues running even if invalid input is entered.

---

# 📝 Logging

Console logging is implemented using Python's `logging` module.

Examples:

* Patient Registered
* Doctor Added
* Appointment Booked
* Appointment Cancelled
* Appointment Completed
* Bill Generated
* Payment Updated
* Invalid Input
* Unexpected Errors

---

# 🎯 Learning Outcomes

This project demonstrates:

* Modular Programming
* CRUD Operations
* Input Validation
* Exception Handling
* Logging
* Business Logic Implementation
* Lists and Dictionaries
* Menu-Driven Programming

---

# 👨‍💻 Author

**Gaurav Joshi**

---

# 📜 License

This project is created for educational purposes.
