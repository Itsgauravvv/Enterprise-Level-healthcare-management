"""
---------------------------------------------------------
File Name : report_module.py
Description : Report Management Module
---------------------------------------------------------
"""

from database_connection import get_connection
from logger_module import log_info, log_error

import mysql.connector


# ---------------------------------------------------------
# Patient Report
# ---------------------------------------------------------

def patient_report():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== PATIENT REPORT ==========\n")

        # -----------------------------------------
        # Total Patients
        # -----------------------------------------

        cursor.execute("SELECT COUNT(*) FROM patients")

        total_patients = cursor.fetchone()[0]

        print(f"Total Patients : {total_patients}")

        # -----------------------------------------
        # Gender Wise Count
        # -----------------------------------------

        print("\n----- Gender Wise Patients -----")

        cursor.execute("""
            SELECT gender,
                   COUNT(*)
            FROM patients
            GROUP BY gender
        """)

        gender_data = cursor.fetchall()

        for gender in gender_data:

            print(f"{gender[0]} : {gender[1]}")

        # -----------------------------------------
        # City Wise Count
        # -----------------------------------------

        print("\n----- City Wise Patients -----")

        cursor.execute("""
            SELECT city,
                   COUNT(*)
            FROM patients
            GROUP BY city
            ORDER BY COUNT(*) DESC
        """)

        city_data = cursor.fetchall()

        for city in city_data:

            print(f"{city[0]} : {city[1]}")

        # -----------------------------------------
        # Blood Group Count
        # -----------------------------------------

        print("\n----- Blood Group Statistics -----")

        cursor.execute("""
            SELECT blood_group,
                   COUNT(*)
            FROM patients
            GROUP BY blood_group
            ORDER BY blood_group
        """)

        blood_data = cursor.fetchall()

        for blood in blood_data:

            print(f"{blood[0]} : {blood[1]}")

        # -----------------------------------------
        # Disease Wise Count
        # -----------------------------------------

        print("\n----- Disease Statistics -----")

        cursor.execute("""
            SELECT disease,
                   COUNT(*)
            FROM patients
            GROUP BY disease
            ORDER BY COUNT(*) DESC
        """)

        disease_data = cursor.fetchall()

        for disease in disease_data:

            print(f"{disease[0]} : {disease[1]}")

        # -----------------------------------------
        # Average Age
        # -----------------------------------------

        cursor.execute("""
            SELECT ROUND(AVG(age),2)
            FROM patients
        """)

        average_age = cursor.fetchone()[0]

        print(f"\nAverage Age : {average_age}")

        # -----------------------------------------
        # Youngest Patient
        # -----------------------------------------

        cursor.execute("""
            SELECT patient_name,
                   age
            FROM patients
            ORDER BY age ASC
            LIMIT 1
        """)

        youngest = cursor.fetchone()

        if youngest:

            print(f"\nYoungest Patient : {youngest[0]} ({youngest[1]} Years)")

        # -----------------------------------------
        # Oldest Patient
        # -----------------------------------------

        cursor.execute("""
            SELECT patient_name,
                   age
            FROM patients
            ORDER BY age DESC
            LIMIT 1
        """)

        oldest = cursor.fetchone()

        if oldest:

            print(f"Oldest Patient : {oldest[0]} ({oldest[1]} Years)")

        log_info("Patient Report Generated")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)

        log_error(str(e))

    finally:

        cursor.close()

        connection.close()

# ---------------------------------------------------------
# Doctor Report
# ---------------------------------------------------------

def doctor_report():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== DOCTOR REPORT ==========\n")

        # -----------------------------------------
        # Total Doctors
        # -----------------------------------------

        cursor.execute("SELECT COUNT(*) FROM doctors")

        total_doctors = cursor.fetchone()[0]

        print(f"Total Doctors : {total_doctors}")

        # -----------------------------------------
        # Department Wise Count
        # -----------------------------------------

        print("\n----- Department Wise Doctors -----")

        cursor.execute("""
            SELECT department,
                   COUNT(*)
            FROM doctors
            GROUP BY department
            ORDER BY department
        """)

        departments = cursor.fetchall()

        for department in departments:

            print(f"{department[0]} : {department[1]}")

        # -----------------------------------------
        # Availability Status
        # -----------------------------------------

        print("\n----- Availability Status -----")

        cursor.execute("""
            SELECT availability_status,
                   COUNT(*)
            FROM doctors
            GROUP BY availability_status
        """)

        availability = cursor.fetchall()

        for status in availability:

            print(f"{status[0]} : {status[1]}")

        # -----------------------------------------
        # Average Consultation Fee
        # -----------------------------------------

        cursor.execute("""
            SELECT ROUND(AVG(consultation_fee),2)
            FROM doctors
        """)

        average_fee = cursor.fetchone()[0]

        print(f"\nAverage Consultation Fee : ₹{average_fee}")

        # -----------------------------------------
        # Highest Consultation Fee
        # -----------------------------------------

        cursor.execute("""
            SELECT
                doctor_name,
                consultation_fee
            FROM doctors
            ORDER BY consultation_fee DESC
            LIMIT 1
        """)

        highest_fee = cursor.fetchone()

        if highest_fee:

            print(
                f"Highest Consultation Fee : "
                f"{highest_fee[0]} (₹{highest_fee[1]})"
            )

        # -----------------------------------------
        # Lowest Consultation Fee
        # -----------------------------------------

        cursor.execute("""
            SELECT
                doctor_name,
                consultation_fee
            FROM doctors
            ORDER BY consultation_fee ASC
            LIMIT 1
        """)

        lowest_fee = cursor.fetchone()

        if lowest_fee:

            print(
                f"Lowest Consultation Fee : "
                f"{lowest_fee[0]} (₹{lowest_fee[1]})"
            )

        # -----------------------------------------
        # Doctors with Highest Number of Appointments
        # -----------------------------------------

        print("\n----- Appointment Statistics -----")

        cursor.execute("""
            SELECT
                d.doctor_name,
                COUNT(a.appointment_id) AS total_appointments
            FROM doctors d
            LEFT JOIN appointments a
            ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id, d.doctor_name
            ORDER BY total_appointments DESC
        """)

        appointment_stats = cursor.fetchall()

        if appointment_stats:

            for doctor in appointment_stats:

                print(
                    f"{doctor[0]} : "
                    f"{doctor[1]} Appointment(s)"
                )

        log_info("Doctor Report Generated")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)

        log_error(str(e))

    finally:

        cursor.close()

        connection.close()

# ---------------------------------------------------------
# Appointment Report
# ---------------------------------------------------------

def appointment_report():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== APPOINTMENT REPORT ==========\n")

        # -----------------------------------------
        # Total Appointments
        # -----------------------------------------

        cursor.execute("SELECT COUNT(*) FROM appointments")

        total_appointments = cursor.fetchone()[0]

        print(f"Total Appointments : {total_appointments}")

        # -----------------------------------------
        # Status Wise Count
        # -----------------------------------------

        print("\n----- Appointment Status -----")

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM appointments
            GROUP BY status
        """)

        status_data = cursor.fetchall()

        for status in status_data:

            print(f"{status[0]} : {status[1]}")

        # -----------------------------------------
        # Date Wise Appointment Count
        # -----------------------------------------

        print("\n----- Date Wise Appointments -----")

        cursor.execute("""
            SELECT
                appointment_date,
                COUNT(*)
            FROM appointments
            GROUP BY appointment_date
            ORDER BY appointment_date
        """)

        date_data = cursor.fetchall()

        if date_data:

            for row in date_data:

                print(f"{row[0]} : {row[1]} Appointment(s)")

        # -----------------------------------------
        # Doctor Wise Appointments
        # -----------------------------------------

        print("\n----- Doctor Wise Appointments -----")

        cursor.execute("""
            SELECT
                d.doctor_name,
                COUNT(a.appointment_id)
            FROM doctors d
            LEFT JOIN appointments a
            ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id,
                     d.doctor_name
            ORDER BY COUNT(a.appointment_id) DESC
        """)

        doctor_data = cursor.fetchall()

        for doctor in doctor_data:

            print(f"{doctor[0]} : {doctor[1]} Appointment(s)")

        # -----------------------------------------
        # Patient Wise Appointments
        # -----------------------------------------

        print("\n----- Patient Wise Appointments -----")

        cursor.execute("""
            SELECT
                p.patient_name,
                COUNT(a.appointment_id)
            FROM patients p
            LEFT JOIN appointments a
            ON p.patient_id = a.patient_id
            GROUP BY p.patient_id,
                     p.patient_name
            ORDER BY COUNT(a.appointment_id) DESC
        """)

        patient_data = cursor.fetchall()

        for patient in patient_data:

            print(f"{patient[0]} : {patient[1]} Appointment(s)")

        # -----------------------------------------
        # Most Busy Doctor
        # -----------------------------------------

        cursor.execute("""
            SELECT
                d.doctor_name,
                COUNT(a.appointment_id) AS total
            FROM doctors d
            INNER JOIN appointments a
            ON d.doctor_id = a.doctor_id
            GROUP BY d.doctor_id,
                     d.doctor_name
            ORDER BY total DESC
            LIMIT 1
        """)

        busy_doctor = cursor.fetchone()

        if busy_doctor:

            print("\n----- Most Busy Doctor -----")
            print(f"{busy_doctor[0]} ({busy_doctor[1]} Appointments)")

        # -----------------------------------------
        # Most Frequent Patient
        # -----------------------------------------

        cursor.execute("""
            SELECT
                p.patient_name,
                COUNT(a.appointment_id) AS total
            FROM patients p
            INNER JOIN appointments a
            ON p.patient_id = a.patient_id
            GROUP BY p.patient_id,
                     p.patient_name
            ORDER BY total DESC
            LIMIT 1
        """)

        frequent_patient = cursor.fetchone()

        if frequent_patient:

            print("\n----- Most Frequent Patient -----")
            print(f"{frequent_patient[0]} ({frequent_patient[1]} Appointments)")

        log_info("Appointment Report Generated")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)

        log_error(str(e))

    finally:

        cursor.close()

        connection.close()

# ---------------------------------------------------------
# Billing Report
# ---------------------------------------------------------

def billing_report():

    connection = get_connection()

    if connection is None:

        print("\nDatabase Connection Failed.")
        return

    cursor = connection.cursor()

    try:

        print("\n========== BILLING REPORT ==========\n")

        # -----------------------------------------
        # Total Bills
        # -----------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM bills
        """)

        total_bills = cursor.fetchone()[0]

        print(f"Total Bills : {total_bills}")

        # -----------------------------------------
        # Total Revenue
        # -----------------------------------------

        cursor.execute("""
            SELECT IFNULL(SUM(total_amount),0)
            FROM bills
        """)

        total_revenue = float(cursor.fetchone()[0])

        print(f"Total Revenue : ₹{total_revenue:.2f}")

        # -----------------------------------------
        # Total Paid Amount
        # -----------------------------------------

        cursor.execute("""
            SELECT IFNULL(SUM(total_amount),0)
            FROM bills
            WHERE payment_status='Paid'
        """)

        paid_amount = float(cursor.fetchone()[0])

        print(f"Paid Amount : ₹{paid_amount:.2f}")

        # -----------------------------------------
        # Total Pending Amount
        # -----------------------------------------

        cursor.execute("""
            SELECT IFNULL(SUM(total_amount),0)
            FROM bills
            WHERE payment_status='Pending'
        """)

        pending_amount = float(cursor.fetchone()[0])

        print(f"Pending Amount : ₹{pending_amount:.2f}")

        # -----------------------------------------
        # Payment Status Statistics
        # -----------------------------------------

        print("\n----- Payment Status -----")

        cursor.execute("""
            SELECT
                payment_status,
                COUNT(*)
            FROM bills
            GROUP BY payment_status
        """)

        payment_data = cursor.fetchall()

        for row in payment_data:

            print(f"{row[0]} : {row[1]}")

        # -----------------------------------------
        # Highest Bill
        # -----------------------------------------

        cursor.execute("""
            SELECT
                bill_id,
                total_amount
            FROM bills
            ORDER BY total_amount DESC
            LIMIT 1
        """)

        highest_bill = cursor.fetchone()

        if highest_bill:

            print(
                f"\nHighest Bill : "
                f"{highest_bill[0]} (₹{highest_bill[1]:.2f})"
            )

        # -----------------------------------------
        # Lowest Bill
        # -----------------------------------------

        cursor.execute("""
            SELECT
                bill_id,
                total_amount
            FROM bills
            ORDER BY total_amount ASC
            LIMIT 1
        """)

        lowest_bill = cursor.fetchone()

        if lowest_bill:

            print(
                f"Lowest Bill : "
                f"{lowest_bill[0]} (₹{lowest_bill[1]:.2f})"
            )

        # -----------------------------------------
        # Average Bill Amount
        # -----------------------------------------

        cursor.execute("""
            SELECT ROUND(AVG(total_amount),2)
            FROM bills
        """)

        average_bill = cursor.fetchone()[0]

        if average_bill is None:
            average_bill = 0

        print(f"Average Bill Amount : ₹{average_bill}")

        # -----------------------------------------
        # Patient-wise Revenue
        # -----------------------------------------

        print("\n----- Patient-wise Revenue -----")

        cursor.execute("""
            SELECT
                p.patient_name,
                IFNULL(SUM(b.total_amount),0)
            FROM patients p
            LEFT JOIN bills b
            ON p.patient_id = b.patient_id
            GROUP BY
                p.patient_id,
                p.patient_name
            ORDER BY
                SUM(b.total_amount) DESC
        """)

        patient_revenue = cursor.fetchall()

        for patient in patient_revenue:

            revenue = patient[1]

            if revenue is None:
                revenue = 0

            print(f"{patient[0]} : ₹{float(revenue):.2f}")

        # -----------------------------------------
        # Top Revenue Patient
        # -----------------------------------------

        cursor.execute("""
            SELECT
                p.patient_name,
                SUM(b.total_amount) AS revenue
            FROM patients p
            INNER JOIN bills b
            ON p.patient_id = b.patient_id
            GROUP BY
                p.patient_id,
                p.patient_name
            ORDER BY revenue DESC
            LIMIT 1
        """)

        top_patient = cursor.fetchone()

        if top_patient:

            print(
                f"\nTop Revenue Patient : "
                f"{top_patient[0]} "
                f"(₹{float(top_patient[1]):.2f})"
            )

        log_info("Billing Report Generated")

    except mysql.connector.Error as e:

        print("\nDatabase Error :", e)

        log_error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)

        log_error(str(e))

    finally:

        cursor.close()

        connection.close()