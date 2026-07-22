# 🏥 Healthcare Management System

A console-based Healthcare Management System developed using **Python** and **MySQL**.

This project helps hospitals and clinics manage patients, doctors, appointments, billing, and reports efficiently.

---

# Features

## Patient Management

- Register Patient
- View All Patients
- Search Patient
- Update Patient
- Delete Patient

---

## Doctor Management

- Add Doctor
- View All Doctors
- Search Doctor
- Update Doctor
- Delete Doctor

---

## Appointment Management

- Book Appointment
- View All Appointments
- Search Appointment
- Update Appointment Status
- Cancel Appointment

---

## Billing Management

- Generate Bill
- View Bills
- Search Bill
- Update Payment Status

---

## Reports

- Patient Report
- Doctor Report
- Appointment Report
- Billing Report

---

# Technologies Used

- Python 3.x
- MySQL
- mysql-connector-python
- Object-Oriented Programming
- Modular Programming

---

# Project Structure

```
HealthcareManagementSystem/
│
├── healthcare_db.sql
├── main.py
├── database_connection.py
├── validation_module.py
├── logger_module.py
├── test_connection.py
├── patient_module.py
├── doctor_module.py
├── appointment_module.py
├── billing_module.py
├── report_module.py
├── README.md
├── requirements.txt
│
└── logs/
    └── healthcare.log
```

---

# Database Tables

## patients

- patient_id
- patient_name
- age
- gender
- contact_number
- city
- blood_group
- disease

---

## doctors

- doctor_id
- doctor_name
- department
- consultation_fee
- availability_status

---

## appointments

- appointment_id
- patient_id
- doctor_id
- appointment_date
- appointment_time
- status

---

## bills

- bill_id
- appointment_id
- patient_id
- consultation_fee
- medicine_charge
- laboratory_charge
- other_charge
- gross_amount
- discount
- total_amount
- payment_status

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/HealthcareManagementSystem.git
```

---

## Go to Project Folder

```bash
cd HealthcareManagementSystem
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Database

Open MySQL Workbench and execute:

```
healthcare_db.sql
```

---

## Configure Database

Open

```
database_connection.py
```

Update:

```python
HOST = "localhost"
USER = "root"
PASSWORD = "your_password"
DATABASE = "healthcare_db"
```

---

## Test Connection

```bash
python test_connection.py
```

---

## Run Project

```bash
python main.py
```

---

# Menu

```
1. Register Patient
2. View Patients
3. Search Patient
4. Update Patient
5. Delete Patient

6. Add Doctor
7. View Doctors
8. Search Doctor
9. Update Doctor
10. Delete Doctor

11. Book Appointment
12. View Appointments
13. Search Appointment
14. Update Appointment Status
15. Cancel Appointment

16. Generate Bill
17. View Bills
18. Search Bill
19. Update Payment Status

20. Reports
21. Exit
```

---

# Python Modules

- database_connection.py
- validation_module.py
- logger_module.py
- patient_module.py
- doctor_module.py
- appointment_module.py
- billing_module.py
- report_module.py

---

# Reports

### Patient Report

- Total Patients
- Gender Statistics
- City Statistics
- Blood Group Statistics
- Disease Statistics
- Average Age

---

### Doctor Report

- Department-wise Doctors
- Availability Status
- Consultation Fee Statistics

---

### Appointment Report

- Total Appointments
- Status-wise Appointments
- Doctor-wise Appointments
- Patient-wise Appointments
- Most Busy Doctor

---

### Billing Report

- Total Revenue
- Paid Bills
- Pending Bills
- Average Bill Amount
- Highest Bill
- Lowest Bill

---

# Logging

Every important operation is recorded automatically in

```
logs/healthcare.log
```

---

# Exception Handling

The project handles:

- Validation Errors
- Database Errors
- Unexpected Errors

---

# Author

**Revanth Sai Bomma**

---

# License

This project is developed for educational purposes.