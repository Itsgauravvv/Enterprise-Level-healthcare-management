"""
---------------------------------------------------------
File Name : billing_module.py
Description : Billing Management Module
---------------------------------------------------------
"""

from database_connection import get_connection
from logger_module import log_info, log_error
from validation_module import *

import mysql.connector



def display_bill(bill):

    print("-" * 90)
    print(f"Bill ID             : {bill[0]}")
    print(f"Appointment ID      : {bill[1]}")
    print(f"Patient ID          : {bill[2]}")
    print(f"Consultation Fee    : ₹{bill[3]:.2f}")
    print(f"Medicine Charge     : ₹{bill[4]:.2f}")
    print(f"Laboratory Charge   : ₹{bill[5]:.2f}")
    print(f"Other Charge        : ₹{bill[6]:.2f}")
    print(f"Gross Amount        : ₹{bill[7]:.2f}")
    print(f"Discount            : ₹{bill[8]:.2f}")
    print(f"Total Amount        : ₹{bill[9]:.2f}")
    print(f"Payment Status      : {bill[10]}")
    print("-" * 90)


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


        appointment_id = input("Enter Appointment ID : ").strip()

        validate_appointment_id(appointment_id)

        cursor.execute("""
            SELECT
                appointment_id,
                patient_id,
                doctor_id,
                status
            FROM appointments
            WHERE appointment_id=%s
        """, (appointment_id,))

        appointment = cursor.fetchone()

        if appointment is None:

            print("\nAppointment Not Found.")
            return

        if appointment[3] != "Completed":

            print("\nBill can be generated only for Completed Appointments.")
            return

        patient_id = appointment[1]
        doctor_id = appointment[2]


        cursor.execute("""
            SELECT bill_id
            FROM bills
            WHERE appointment_id=%s
        """, (appointment_id,))

        if cursor.fetchone():

            print("\nBill already exists for this Appointment.")
            return


        cursor.execute("""
            SELECT consultation_fee
            FROM doctors
            WHERE doctor_id=%s
        """, (doctor_id,))

        doctor = cursor.fetchone()

        if doctor is None:

            print("\nDoctor Record Not Found.")
            return

        consultation_fee = float(doctor[0])

        print(f"\nConsultation Fee : ₹{consultation_fee:.2f}")

 

        medicine_charge = float(
            input("Medicine Charge : ")
        )

        validate_amount(medicine_charge)

        laboratory_charge = float(
            input("Laboratory Charge : ")
        )

        validate_amount(laboratory_charge)

        other_charge = float(
            input("Other Charge : ")
        )

        validate_amount(other_charge)

        

        gross_amount = (
            consultation_fee +
            medicine_charge +
            laboratory_charge +
            other_charge
        )

        print(f"\nGross Amount : ₹{gross_amount:.2f}")


        discount = float(
            input("Enter Discount : ")
        )

        validate_discount(discount)

        if discount > gross_amount:

            print("\nDiscount cannot be greater than Gross Amount.")
            return

        total_amount = gross_amount - discount

        print(f"Total Amount : ₹{total_amount:.2f}")

       

        payment_status = input(
            "Payment Status (Paid/Pending) : "
        ).strip()

        validate_payment_status(payment_status)


        sql = """
        INSERT INTO bills
        (
            bill_id,
            appointment_id,
            patient_id,
            consultation_fee,
            medicine_charge,
            laboratory_charge,
            other_charge,
            gross_amount,
            discount,
            total_amount,
            payment_status
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (
            bill_id,
            appointment_id,
            patient_id,
            consultation_fee,
            medicine_charge,
            laboratory_charge,
            other_charge,
            gross_amount,
            discount,
            total_amount,
            payment_status
        )

        cursor.execute(sql, values)

        connection.commit()

        print("\nBill Generated Successfully.")

        print("\n========== BILL DETAILS ==========")

        cursor.execute("""
            SELECT *
            FROM bills
            WHERE bill_id=%s
        """, (bill_id,))

        bill = cursor.fetchone()

        display_bill(bill)

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
                b.appointment_id,
                b.patient_id,
                p.patient_name,
                b.consultation_fee,
                b.medicine_charge,
                b.laboratory_charge,
                b.other_charge,
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

        print("\n================ ALL BILLS ================\n")

        total_revenue = 0

        for bill in bills:

            print("-" * 90)
            print(f"Bill ID             : {bill[0]}")
            print(f"Appointment ID      : {bill[1]}")
            print(f"Patient ID          : {bill[2]}")
            print(f"Patient Name        : {bill[3]}")
            print(f"Consultation Fee    : ₹{bill[4]:.2f}")
            print(f"Medicine Charge     : ₹{bill[5]:.2f}")
            print(f"Laboratory Charge   : ₹{bill[6]:.2f}")
            print(f"Other Charge        : ₹{bill[7]:.2f}")
            print(f"Gross Amount        : ₹{bill[8]:.2f}")
            print(f"Discount            : ₹{bill[9]:.2f}")
            print(f"Total Amount        : ₹{bill[10]:.2f}")
            print(f"Payment Status      : {bill[11]}")
            print("-" * 90)

            total_revenue += float(bill[10])

        print(f"\nTotal Bills        : {len(bills)}")
        print(f"Total Revenue      : ₹{total_revenue:.2f}")

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


def search_bill():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== SEARCH BILL ==========")

        print("1. Bill ID")
        print("2. Appointment ID")
        print("3. Patient ID")
        print("4. Payment Status")

        choice = input("\nEnter Choice : ").strip()

       

        if choice == "1":

            bill_id = input("Enter Bill ID : ").strip()

            validate_bill_id(bill_id)

            cursor.execute("""
                SELECT *
                FROM bills
                WHERE bill_id=%s
            """, (bill_id,))


        elif choice == "2":

            appointment_id = input(
                "Enter Appointment ID : "
            ).strip()

            validate_appointment_id(appointment_id)

            cursor.execute("""
                SELECT *
                FROM bills
                WHERE appointment_id=%s
            """, (appointment_id,))


        elif choice == "3":

            patient_id = input(
                "Enter Patient ID : "
            ).strip()

            validate_patient_id(patient_id)

            cursor.execute("""
                SELECT *
                FROM bills
                WHERE patient_id=%s
            """, (patient_id,))


        elif choice == "4":

            payment_status = input(
                "Enter Payment Status (Paid/Pending) : "
            ).strip()

            validate_payment_status(payment_status)

            cursor.execute("""
                SELECT *
                FROM bills
                WHERE payment_status=%s
            """, (payment_status,))

        else:

            print("\nInvalid Choice.")
            return

        bills = cursor.fetchall()

        if len(bills) == 0:

            print("\nNo Matching Bill Found.")
            return

        print("\n========== SEARCH RESULT ==========\n")

        total_amount = 0

        for bill in bills:

            display_bill(bill)

            total_amount += float(bill[9])

        print(f"\nTotal Records : {len(bills)}")
        print(f"Total Amount  : ₹{total_amount:.2f}")

        log_info("Bill Search Performed")

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

        print("\n========== UPDATE PAYMENT STATUS ==========")

        bill_id = input("Enter Bill ID : ").strip()

        validate_bill_id(bill_id)

     

        cursor.execute("""
            SELECT *
            FROM bills
            WHERE bill_id=%s
        """, (bill_id,))

        bill = cursor.fetchone()

        if bill is None:

            print("\nBill Not Found.")
            return

        print("\n========== BILL DETAILS ==========\n")

        display_bill(bill)


        if bill[10] == "Paid":

            print("\nPayment has already been completed.")

            log_error(
                f"Payment Already Completed : {bill_id}"
            )

            return


        confirm = input(
            "\nMark this bill as Paid? (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print("\nPayment Status Update Cancelled.")
            return

       
        cursor.execute("""
            UPDATE bills
            SET payment_status='Paid'
            WHERE bill_id=%s
        """, (bill_id,))

        connection.commit()

        print("\nPayment Status Updated Successfully.")


        cursor.execute("""
            SELECT *
            FROM bills
            WHERE bill_id=%s
        """, (bill_id,))

        updated_bill = cursor.fetchone()

        print("\n========== UPDATED BILL ==========\n")

        display_bill(updated_bill)

        log_info(
            f"Payment Status Updated : {bill_id} -> Paid"
        )

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