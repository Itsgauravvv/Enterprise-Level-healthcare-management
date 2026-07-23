from database_connection import get_connection
from logger_module import log_info, log_error
from validation_module import (
    validate_bill_id,
    validate_amount,
    validate_discount,
    validate_payment_status
)

import mysql.connector


def generate_bill():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== GENERATE BILL ==========")

        bill_id = input("Enter Bill ID : ").strip()
        validate_bill_id(bill_id)

        cursor.execute(
            "SELECT bill_id FROM bills WHERE bill_id=%s",
            (bill_id,)
        )

        if cursor.fetchone():

            print("\nBill ID already exists.")
            log_error(f"Duplicate Bill ID : {bill_id}")
            return

        patient_id = input("Enter Patient ID : ").strip()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Patient ID does not exist.")

        appointment_id = input("Enter Appointment ID : ").strip()

        cursor.execute(
            """
            SELECT patient_id, status
            FROM appointments
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        if appointment[0] != patient_id:
            raise ValueError(
                "Appointment does not belong to this patient."
            )

        if appointment[1] != "Completed":
            raise ValueError(
                "Bill can be generated only for completed appointments."
            )

        cursor.execute(
            """
            SELECT bill_id
            FROM bills
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        if cursor.fetchone():
            raise ValueError(
                "Bill already generated for this appointment."
            )

        consultation_fee = float(
            input("Consultation Fee : ")
        )
        validate_amount(consultation_fee)

        medicine_charges = float(
            input("Medicine Charges : ")
        )
        validate_amount(medicine_charges)

        laboratory_charges = float(
            input("Laboratory Charges : ")
        )
        validate_amount(laboratory_charges)

        room_charges = float(
            input("Room Charges : ")
        )
        validate_amount(room_charges)

        gross_amount = (
            consultation_fee +
            medicine_charges +
            laboratory_charges +
            room_charges
        )

        discount = float(
            input("Discount : ")
        )

        validate_discount(discount, gross_amount)

        total_amount = gross_amount - discount

        payment_status = input(
            "Payment Status (Paid/Pending): "
        ).strip().title()

        validate_payment_status(payment_status)

        cursor.execute(
            """
            INSERT INTO bills
            (
                bill_id,
                patient_id,
                appointment_id,
                consultation_fee,
                medicine_charges,
                laboratory_charges,
                room_charges,
                gross_amount,
                discount,
                total_amount,
                payment_status
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                bill_id,
                patient_id,
                appointment_id,
                consultation_fee,
                medicine_charges,
                laboratory_charges,
                room_charges,
                gross_amount,
                discount,
                total_amount,
                payment_status
            )
        )

        connection.commit()

        print("\nBill Generated Successfully.")

        print("\n----------- BILL -----------")
        print(f"Bill ID           : {bill_id}")
        print(f"Patient ID        : {patient_id}")
        print(f"Appointment ID    : {appointment_id}")
        print(f"Gross Amount      : ₹{gross_amount}")
        print(f"Discount          : ₹{discount}")
        print(f"Total Amount      : ₹{total_amount}")
        print(f"Payment Status    : {payment_status}")
        print("-----------------------------")

        log_info(f"Bill Generated : {bill_id}")

    except ValueError as e:

        print("\nValidation Error :", e)
        log_error(str(e))

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()

def display_bill(bill):

    print("-" * 80)
    print(f"Bill ID              : {bill[0]}")
    print(f"Patient ID           : {bill[1]}")
    print(f"Patient Name         : {bill[2]}")
    print(f"Appointment ID       : {bill[3]}")
    print(f"Consultation Fee     : {bill[4]}")
    print(f"Medicine Charges     : {bill[5]}")
    print(f"Laboratory Charges   : {bill[6]}")
    print(f"Room Charges         : {bill[7]}")
    print(f"Gross Amount         : {bill[8]}")
    print(f"Discount             : {bill[9]}")
    print(f"Total Amount         : {bill[10]}")
    print(f"Payment Status       : {bill[11]}")
    print("-" * 80)

def view_all_bills():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                b.bill_id,
                b.patient_id,
                p.patient_name,
                b.appointment_id,
                b.consultation_fee,
                b.medicine_charges,
                b.laboratory_charges,
                b.room_charges,
                b.gross_amount,
                b.discount,
                b.total_amount,
                b.payment_status
            FROM bills b
            INNER JOIN patients p
            ON b.patient_id = p.patient_id
            ORDER BY b.bill_id
        """)

        bills = cursor.fetchall()

        if len(bills) == 0:

            print("\nNo Bills Found.")
            return

        print("\n========== ALL BILLS ==========\n")

        total_revenue = 0
        total_paid = 0
        total_pending = 0

        for bill in bills:

            display_bill(bill)

            total_revenue += bill[10]

            if bill[11] == "Paid":
                total_paid += bill[10]
            else:
                total_pending += bill[10]

        print("\n========== BILL SUMMARY ==========")
        print(f"Total Bills        : {len(bills)}")
        print(f"Total Revenue      : ₹{total_revenue}")
        print(f"Total Paid Amount  : ₹{total_paid}")
        print(f"Total Pending      : ₹{total_pending}")
        print(f"Average Bill Amount: ₹{total_revenue/len(bills):.2f}")

        log_info("Viewed All Bills")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()
def search_patient_bills():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        patient_id = input("Enter Patient ID : ").strip()

        cursor.execute(
            """
            SELECT patient_name
            FROM patients
            WHERE patient_id=%s
            """,
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:
            raise ValueError("Patient ID does not exist.")

        patient_name = patient[0]

        cursor.execute(
            """
            SELECT
                b.bill_id,
                b.patient_id,
                p.patient_name,
                b.appointment_id,
                b.consultation_fee,
                b.medicine_charges,
                b.laboratory_charges,
                b.room_charges,
                b.gross_amount,
                b.discount,
                b.total_amount,
                b.payment_status
            FROM bills b
            INNER JOIN patients p
            ON b.patient_id=p.patient_id
            WHERE b.patient_id=%s
            ORDER BY b.bill_id
            """,
            (patient_id,)
        )

        bills = cursor.fetchall()

        if len(bills) == 0:
            raise ValueError("No bills found for this patient.")

        total_billed = 0
        total_paid = 0
        total_pending = 0

        print("\n========== PATIENT BILL DETAILS ==========\n")
        print(f"Patient ID   : {patient_id}")
        print(f"Patient Name : {patient_name}\n")

        for bill in bills:

            display_bill(bill)

            total_billed += bill[10]

            if bill[11] == "Paid":
                total_paid += bill[10]
            else:
                total_pending += bill[10]

        print("\n========== BILL SUMMARY ==========")
        print(f"Total Bills   : {len(bills)}")
        print(f"Total Billed  : ₹{total_billed}")
        print(f"Total Paid    : ₹{total_paid}")
        print(f"Total Pending : ₹{total_pending}")

        log_info(f"Searched Bills : {patient_id}")

    except ValueError as e:

        print("\nValidation Error :", e)
        log_error(str(e))

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()

def update_payment_status():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        bill_id = input("Enter Bill ID : ").strip()

        cursor.execute(
            """
            SELECT payment_status
            FROM bills
            WHERE bill_id=%s
            """,
            (bill_id,)
        )

        bill = cursor.fetchone()

        if bill is None:
            raise ValueError("Bill ID does not exist.")

        if bill[0] == "Paid":
            raise ValueError("Payment is already completed.")

        print(f"\nCurrent Payment Status : {bill[0]}")

        confirm = input(
            "Mark this bill as Paid? (Y/N): "
        ).strip().upper()

        if confirm != "Y":

            print("\nPayment Update Cancelled.")
            return

        cursor.execute(
            """
            UPDATE bills
            SET payment_status='Paid'
            WHERE bill_id=%s
            """,
            (bill_id,)
        )

        connection.commit()

        print("\nPayment Status Updated Successfully.")

        log_info(f"Payment Updated : {bill_id}")

    except ValueError as e:

        print("\nValidation Error :", e)
        log_error(str(e))

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()