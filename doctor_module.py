
from database_connection import get_connection
from logger_module import log_info, log_error
from validation_module import *

import mysql.connector




def display_doctor(doctor):

    print("-" * 70)
    print(f"Doctor ID            : {doctor[0]}")
    print(f"Doctor Name          : {doctor[1]}")
    print(f"Department           : {doctor[2]}")
    print(f"Consultation Fee     : ₹{doctor[3]}")
    print(f"Availability Status  : {doctor[4]}")
    print("-" * 70)



def add_doctor():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== ADD DOCTOR ==========")

        doctor_id = input("Enter Doctor ID : ").strip()

        validate_doctor_id(doctor_id)

        cursor.execute(
            "SELECT doctor_id FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        if cursor.fetchone():

            print("\nDoctor ID already exists.")
            log_error(f"Duplicate Doctor ID : {doctor_id}")
            return

        doctor_name = input("Enter Doctor Name : ").strip()

        validate_name(doctor_name)

        department = input("Enter Department : ").strip()

        validate_department(department)

        consultation_fee = float(
            input("Enter Consultation Fee : ")
        )

        validate_consultation_fee(consultation_fee)

        availability_status = input(
            "Availability (Available/Unavailable/On Leave) : "
        ).strip()

        validate_availability_status(availability_status)

        sql = """
        INSERT INTO doctors
        (
            doctor_id,
            doctor_name,
            department,
            consultation_fee,
            availability_status
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
        """

        values = (

            doctor_id,
            doctor_name,
            department,
            consultation_fee,
            availability_status

        )

        cursor.execute(sql, values)

        connection.commit()

        print("\nDoctor Added Successfully.")

        log_info(f"Doctor Added : {doctor_id}")

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

def view_all_doctors():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                doctor_id,
                doctor_name,
                department,
                consultation_fee,
                availability_status
            FROM doctors
            ORDER BY doctor_id
        """)

        doctors = cursor.fetchall()

        if len(doctors) == 0:

            print("\nNo Doctor Records Found.")
            return

        print("\n========== ALL DOCTORS ==========\n")

        for doctor in doctors:
            display_doctor(doctor)

        print(f"\nTotal Doctors : {len(doctors)}")

        log_info("Viewed All Doctors")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()




def search_doctor():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== SEARCH DOCTOR ==========")

        print("1. Doctor ID")
        print("2. Doctor Name")
        print("3. Department")
        print("4. Availability Status")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":

            doctor_id = input("Enter Doctor ID : ").strip()

            cursor.execute("""
                SELECT *
                FROM doctors
                WHERE doctor_id=%s
            """, (doctor_id,))

        elif choice == "2":

            doctor_name = input("Enter Doctor Name : ").strip()

            cursor.execute("""
                SELECT *
                FROM doctors
                WHERE doctor_name LIKE %s
            """, ("%" + doctor_name + "%",))

        elif choice == "3":

            department = input("Enter Department : ").strip()

            cursor.execute("""
                SELECT *
                FROM doctors
                WHERE department LIKE %s
            """, ("%" + department + "%",))

        elif choice == "4":

            status = input(
                "Enter Status (Available/Unavailable/On Leave) : "
            ).strip()

            cursor.execute("""
                SELECT *
                FROM doctors
                WHERE availability_status=%s
            """, (status,))

        else:

            print("\nInvalid Choice.")
            return

        doctors = cursor.fetchall()

        if len(doctors) == 0:

            print("\nNo Matching Doctor Found.")
            return

        print("\n========== SEARCH RESULT ==========\n")

        for doctor in doctors:
            display_doctor(doctor)

        print(f"\nTotal Records Found : {len(doctors)}")

        log_info("Doctor Search Performed")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()


def update_doctor():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== UPDATE DOCTOR ==========")

        doctor_id = input("Enter Doctor ID : ").strip()

        validate_doctor_id(doctor_id)

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor is None:

            print("\nDoctor Not Found.")
            return

        print("\nCurrent Doctor Details")
        display_doctor(doctor)

        print("\nEnter New Details")

        doctor_name = input("Doctor Name : ").strip()
        validate_name(doctor_name)

        department = input("Department : ").strip()
        validate_department(department)

        consultation_fee = float(
            input("Consultation Fee : ")
        )
        validate_consultation_fee(consultation_fee)

        availability_status = input(
            "Availability (Available/Unavailable/On Leave) : "
        ).strip()

        validate_availability_status(availability_status)

        sql = """
        UPDATE doctors
        SET
            doctor_name=%s,
            department=%s,
            consultation_fee=%s,
            availability_status=%s
        WHERE doctor_id=%s
        """

        values = (
            doctor_name,
            department,
            consultation_fee,
            availability_status,
            doctor_id
        )

        cursor.execute(sql, values)

        connection.commit()

        print("\nDoctor Updated Successfully.")

        log_info(f"Doctor Updated : {doctor_id}")

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




def delete_doctor():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== DELETE DOCTOR ==========")

        doctor_id = input("Enter Doctor ID : ").strip()

        validate_doctor_id(doctor_id)

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if doctor is None:

            print("\nDoctor Not Found.")
            return

        display_doctor(doctor)


        cursor.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE doctor_id=%s
            AND status='Scheduled'
            """,
            (doctor_id,)
        )

        if cursor.fetchone():

            print("\nCannot Delete Doctor.")
            print("Doctor has Scheduled Appointments.")

            log_error(
                f"Delete Failed : Scheduled Appointment Exists ({doctor_id})"
            )

            return

        confirm = input("\nAre you sure? (Y/N) : ").strip().upper()

        if confirm != "Y":

            print("\nDeletion Cancelled.")
            return

        cursor.execute(
            "DELETE FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        connection.commit()

        print("\nDoctor Deleted Successfully.")

        log_info(f"Doctor Deleted : {doctor_id}")

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
        