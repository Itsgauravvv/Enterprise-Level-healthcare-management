import re
from datetime import datetime


# -----------------------------
# Patient Validation
# -----------------------------

def validate_patient_id(patient_id):
    if patient_id.strip() == "":
        raise ValueError("Patient ID cannot be empty.")
    return True


def validate_name(name):
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    if not re.fullmatch(r"[A-Za-z ]+", name):
        raise ValueError("Name should contain only alphabets and spaces.")

    return True


def validate_age(age):
    try:
        age = int(age)

        if age < 1 or age > 120:
            raise ValueError("Age must be between 1 and 120.")

        return True

    except ValueError:
        raise ValueError("Invalid age. Please enter a numeric value.")


def validate_gender(gender):
    genders = ["Male", "Female", "Other"]

    if gender.title() not in genders:
        raise ValueError("Gender must be Male, Female or Other.")

    return True


def validate_contact_number(contact):
    if not re.fullmatch(r"\d{10}", contact):
        raise ValueError("Contact number must contain exactly 10 digits.")

    return True


def validate_city(city):
    if city.strip() == "":
        raise ValueError("City cannot be empty.")

    return True


def validate_blood_group(group):

    valid_groups = [
        "A+","A-",
        "B+","B-",
        "AB+","AB-",
        "O+","O-"
    ]

    if group.upper() not in valid_groups:
        raise ValueError("Invalid Blood Group.")

    return True


def validate_disease(disease):
    if disease.strip() == "":
        raise ValueError("Disease cannot be empty.")

    return True


# -----------------------------
# Doctor Validation
# -----------------------------

def validate_doctor_id(doctor_id):
    if doctor_id.strip() == "":
        raise ValueError("Doctor ID cannot be empty.")

    return True


def validate_department(department):
    if department.strip() == "":
        raise ValueError("Department cannot be empty.")

    return True


def validate_consultation_fee(fee):
    try:

        fee = float(fee)

        if fee <= 0:
            raise ValueError("Consultation fee must be greater than zero.")

        return True

    except ValueError:
        raise ValueError("Invalid consultation fee.")


def validate_availability_status(status):

    valid = [
        "Available",
        "Unavailable",
        "On Leave"
    ]

    if status.title() not in valid:
        raise ValueError("Invalid availability status.")

    return True


# -----------------------------
# Appointment Validation
# -----------------------------

def validate_appointment_id(app_id):
    if app_id.strip() == "":
        raise ValueError("Appointment ID cannot be empty.")

    return True


def validate_date(date):

    try:
        datetime.strptime(date, "%d-%m-%Y")
        return True

    except ValueError:
        raise ValueError("Date must be in DD-MM-YYYY format.")


def validate_time(time):

    try:
        datetime.strptime(time, "%I:%M %p")
        return True

    except ValueError:
        raise ValueError("Time must be in HH:MM AM/PM format.")


def validate_appointment_status(status):

    valid = [
        "Scheduled",
        "Completed",
        "Cancelled"
    ]

    if status.title() not in valid:
        raise ValueError("Invalid appointment status.")

    return True


# -----------------------------
# Billing Validation
# -----------------------------

def validate_bill_id(bill_id):

    if bill_id.strip() == "":
        raise ValueError("Bill ID cannot be empty.")

    return True


def validate_amount(amount):

    try:

        amount = float(amount)

        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        return True

    except ValueError:
        raise ValueError("Invalid amount.")


def validate_discount(discount, gross_amount):

    try:

        discount = float(discount)
        gross_amount = float(gross_amount)

        if discount < 0:
            raise ValueError("Discount cannot be negative.")

        if discount > gross_amount:
            raise ValueError("Discount cannot exceed Gross Amount.")

        return True

    except ValueError:
        raise ValueError("Invalid discount.")


def validate_payment_status(status):

    valid = [
        "Paid",
        "Pending"
    ]

    if status.title() not in valid:
        raise ValueError("Payment Status must be Paid or Pending.")

    return True