

from database_connection import get_connection
from logger_module import log_info, log_error
from validation_module import *

import mysql.connector




def display_patient(patient):

    print("-" * 80)
    print(f"Patient ID      : {patient[0]}")
    print(f"Patient Name    : {patient[1]}")
    print(f"Age             : {patient[2]}")
    print(f"Gender          : {patient[3]}")
    print(f"Contact Number  : {patient[4]}")
    print(f"City            : {patient[5]}")
    print(f"Blood Group     : {patient[6]}")
    print(f"Disease         : {patient[7]}")
    print("-" * 80)



def register_patient():

    connection = get_connection()

    if connection is None:
        print("\nDatabase connection failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== Register Patient ==========")

        patient_id = input("Enter Patient ID : ").strip()

        validate_patient_id(patient_id)

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        if cursor.fetchone():

            print("\nPatient ID already exists.")
            log_error(f"Duplicate Patient ID : {patient_id}")
            return

        patient_name = input("Enter Patient Name : ").strip()
        validate_name(patient_name)

        age = int(input("Enter Age : "))
        validate_age(age)

        gender = input("Enter Gender (Male/Female/Other) : ").strip()
        validate_gender(gender)

        contact_number = input("Enter Contact Number : ").strip()
        validate_contact_number(contact_number)

        cursor.execute(
            "SELECT contact_number FROM patients WHERE contact_number=%s",
            (contact_number,)
        )

        if cursor.fetchone():

            print("\nContact Number already exists.")
            log_error(f"Duplicate Contact Number : {contact_number}")
            return

        city = input("Enter City : ").strip()
        validate_city(city)

        blood_group = input("Enter Blood Group : ").strip()
        validate_blood_group(blood_group)

        disease = input("Enter Disease : ").strip()
        validate_disease(disease)

        sql = """
        INSERT INTO patients
        (
            patient_id,
            patient_name,
            age,
            gender,
            contact_number,
            city,
            blood_group,
            disease
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (
            patient_id,
            patient_name,
            age,
            gender,
            contact_number,
            city,
            blood_group,
            disease
        )

        cursor.execute(sql, values)

        connection.commit()

        print("\nPatient Registered Successfully.")

        log_info(f"Patient Registered : {patient_id}")

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



def view_all_patients():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                patient_id,
                patient_name,
                age,
                gender,
                contact_number,
                city,
                blood_group,
                disease
            FROM patients
            ORDER BY patient_id
        """)

        patients = cursor.fetchall()

        if len(patients) == 0:
            print("\nNo Patient Records Found.")
            return

        print("\n========== ALL PATIENTS ==========\n")

        for patient in patients:
            display_patient(patient)

        print(f"\nTotal Patients : {len(patients)}")

        log_info("Viewed All Patients")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()


def search_patient():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== SEARCH PATIENT ==========")

        print("1. Patient ID")
        print("2. Patient Name")
        print("3. Contact Number")
        print("4. City")
        print("5. Blood Group")
        print("6. Disease")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":

            patient_id = input("Enter Patient ID : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE patient_id=%s
            """, (patient_id,))

        elif choice == "2":

            patient_name = input("Enter Patient Name : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE patient_name LIKE %s
            """, ("%" + patient_name + "%",))

        elif choice == "3":

            contact = input("Enter Contact Number : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE contact_number=%s
            """, (contact,))

        elif choice == "4":

            city = input("Enter City : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE city LIKE %s
            """, ("%" + city + "%",))

        elif choice == "5":

            blood = input("Enter Blood Group : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE blood_group=%s
            """, (blood,))

        elif choice == "6":

            disease = input("Enter Disease : ").strip()

            cursor.execute("""
                SELECT *
                FROM patients
                WHERE disease LIKE %s
            """, ("%" + disease + "%",))

        else:

            print("\nInvalid Choice.")
            return

        patients = cursor.fetchall()

        if len(patients) == 0:

            print("\nNo Matching Patient Found.")
            return

        print("\n========== SEARCH RESULT ==========\n")

        for patient in patients:
            display_patient(patient)

        print(f"\nTotal Records Found : {len(patients)}")

        log_info("Patient Search Performed")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)
        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        log_error(str(e))

    finally:

        cursor.close()
        connection.close()

def update_patient():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== UPDATE PATIENT ==========")

        patient_id = input("Enter Patient ID : ").strip()

        validate_patient_id(patient_id)

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:

            print("\nPatient Not Found.")
            return

        print("\nCurrent Patient Details")
        display_patient(patient)

        print("\nEnter New Details")

        patient_name = input("Patient Name : ").strip()
        validate_name(patient_name)

        age = int(input("Age : "))
        validate_age(age)

        gender = input("Gender (Male/Female/Other) : ").strip()
        validate_gender(gender)

        contact_number = input("Contact Number : ").strip()
        validate_contact_number(contact_number)

        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE contact_number=%s
            AND patient_id<>%s
            """,
            (contact_number, patient_id)
        )

        if cursor.fetchone():

            print("\nContact Number already exists.")
            return

        city = input("City : ").strip()
        validate_city(city)

        blood_group = input("Blood Group : ").strip()
        validate_blood_group(blood_group)

        disease = input("Disease : ").strip()
        validate_disease(disease)

        sql = """
        UPDATE patients
        SET
            patient_name=%s,
            age=%s,
            gender=%s,
            contact_number=%s,
            city=%s,
            blood_group=%s,
            disease=%s
        WHERE patient_id=%s
        """

        values = (
            patient_name,
            age,
            gender,
            contact_number,
            city,
            blood_group,
            disease,
            patient_id
        )

        cursor.execute(sql, values)

        connection.commit()

        print("\nPatient Updated Successfully.")

        log_info(f"Patient Updated : {patient_id}")

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




def delete_patient():

    connection = get_connection()

    if connection is None:
        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== DELETE PATIENT ==========")

        patient_id = input("Enter Patient ID : ").strip()

        validate_patient_id(patient_id)

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:

            print("\nPatient Not Found.")
            return

        display_patient(patient)

    

        cursor.execute(
            """
            SELECT appointment_id
            FROM appointments
            WHERE patient_id=%s
            AND status='Scheduled'
            """,
            (patient_id,)
        )

        if cursor.fetchone():

            print("\nCannot Delete Patient.")
            print("Scheduled Appointment Exists.")

            log_error(
                f"Delete Failed : Scheduled Appointment Exists ({patient_id})"
            )

            return

        confirm = input("\nAre you sure? (Y/N) : ").strip().upper()

        if confirm != "Y":

            print("\nDeletion Cancelled.")
            return

        cursor.execute(
            "DELETE FROM patients WHERE patient_id=%s",
            (patient_id,)
        )

        connection.commit()

        print("\nPatient Deleted Successfully.")

        log_info(f"Patient Deleted : {patient_id}")

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

