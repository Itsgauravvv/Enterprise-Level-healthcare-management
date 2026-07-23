from database_connection import get_connection
from logger_module import log_info, log_error
from validation_module import (
    validate_appointment_id,
    validate_date,
    validate_time
)

import mysql.connector
from datetime import datetime

from validation_module import (
    validate_appointment_id,
    validate_date,
    validate_time
)
from logger_module import logger


def display_appointment(appointment):
    print("-" * 80)
    print(f"Appointment ID   : {appointment[0]}")
    print(f"Patient ID       : {appointment[1]}")
    print(f"Patient Name     : {appointment[2]}")
    print(f"Doctor ID        : {appointment[3]}")
    print(f"Doctor Name      : {appointment[4]}")
    print(f"Department       : {appointment[5]}")
    print(f"Appointment Date : {appointment[6]}")
    print(f"Appointment Time : {appointment[7]}")
    print(f"Status           : {appointment[8]}")
    print("-" * 80)


# ----------------------------------------
# Book Appointment
# ----------------------------------------

def book_appointment():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== BOOK APPOINTMENT ==========")

        appointment_id = input("Enter Appointment ID : ").strip()
        validate_appointment_id(appointment_id)

        cursor.execute(
            "SELECT appointment_id FROM appointments WHERE appointment_id=%s",
            (appointment_id,)
        )

        if cursor.fetchone():

            print("\nAppointment ID already exists.")
            log_error(f"Duplicate Appointment ID : {appointment_id}")
            return

        patient_id = input("Enter Patient ID : ").strip()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        if cursor.fetchone() is None:
            raise ValueError("Patient ID does not exist.")

        doctor_id = input("Enter Doctor ID : ").strip()

        cursor.execute(
            """
            SELECT availability_status
            FROM doctors
            WHERE doctor_id=%s
            """,
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor is None:
            raise ValueError("Doctor ID does not exist.")

        if doctor[0] != "Available":
            raise ValueError("Doctor is currently unavailable.")

        appointment_date = input(
            "Enter Appointment Date (DD-MM-YYYY): "
        ).strip()

        validate_date(appointment_date)

        appointment_time = input(
            "Enter Appointment Time (HH:MM AM/PM): "
        ).strip()

        validate_time(appointment_time)

        sql_date = datetime.strptime(
            appointment_date,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

        sql_time = datetime.strptime(
            appointment_time,
            "%I:%M %p"
        ).strftime("%H:%M:%S")

        cursor.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE doctor_id=%s
            AND appointment_date=%s
            AND appointment_time=%s
            AND status='Scheduled'
            """,
            (
                doctor_id,
                sql_date,
                sql_time
            )
        )

        if cursor.fetchone():

            raise ValueError(
                "Appointment slot is already booked."
            )

        cursor.execute(
            """
            INSERT INTO appointments
            (
                appointment_id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s
            )
            """,
            (
                appointment_id,
                patient_id,
                doctor_id,
                sql_date,
                sql_time,
                "Scheduled"
            )
        )

        connection.commit()

        print("\nAppointment Booked Successfully.")

        log_info(
            f"Appointment Booked : {appointment_id}"
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

def view_all_appointments():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                a.appointment_id,
                a.patient_id,
                p.patient_name,
                a.doctor_id,
                d.doctor_name,
                d.department,
                a.appointment_date,
                a.appointment_time,
                a.status
            FROM appointments a
            INNER JOIN patients p
                ON a.patient_id = p.patient_id
            INNER JOIN doctors d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date,
                     a.appointment_time
        """)

        appointments = cursor.fetchall()

        if len(appointments) == 0:

            print("\nNo Appointment Records Found.")
            return

        print("\n========== ALL APPOINTMENTS ==========\n")

        for appointment in appointments:
            display_appointment(appointment)

        print(f"\nTotal Appointments : {len(appointments)}")

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM appointments
            GROUP BY status
        """)

        summary = cursor.fetchall()

        print("\nAppointment Summary")
        print("--------------------------")

        for row in summary:
            print(f"{row[0]} : {row[1]}")

        log_info("Viewed All Appointments")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()

# ----------------------------------------
# Cancel Appointment
# ----------------------------------------

def cancel_appointment():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        appointment_id = input(
            "Enter Appointment ID to Cancel : "
        ).strip()

        cursor.execute("""
            SELECT status
            FROM appointments
            WHERE appointment_id=%s
        """, (appointment_id,))

        appointment = cursor.fetchone()

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        status = appointment[0]

        if status == "Completed":
            raise ValueError(
                "Completed appointment cannot be cancelled."
            )

        if status == "Cancelled":
            raise ValueError(
                "Appointment is already cancelled."
            )

        confirm = input(
            "Are you sure? (Y/N): "
        ).strip().upper()

        if confirm != "Y":

            print("\nCancellation Aborted.")
            return

        cursor.execute("""
            UPDATE appointments
            SET status='Cancelled'
            WHERE appointment_id=%s
        """, (appointment_id,))

        connection.commit()

        print("\nAppointment Cancelled Successfully.")

        log_info(
            f"Appointment Cancelled : {appointment_id}"
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

def complete_appointment():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        appointment_id = input(
            "Enter Appointment ID to Complete : "
        ).strip()

        cursor.execute("""
            SELECT status
            FROM appointments
            WHERE appointment_id=%s
        """, (appointment_id,))

        appointment = cursor.fetchone()

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        status = appointment[0]

        if status == "Cancelled":
            raise ValueError(
                "Cancelled appointment cannot be completed."
            )

        if status == "Completed":
            raise ValueError(
                "Appointment is already completed."
            )

        cursor.execute("""
            UPDATE appointments
            SET status='Completed'
            WHERE appointment_id=%s
        """, (appointment_id,))

        connection.commit()

        print("\nAppointment Completed Successfully.")

        log_info(
            f"Appointment Completed : {appointment_id}"
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