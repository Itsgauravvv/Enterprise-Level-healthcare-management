from data_store import patients, doctors, appointments, bills
from logger_module import logger
# ----------------------------------------
# Generate Patient Reports
# ----------------------------------------

def generate_patient_reports():

    try:

        if not patients:
            raise ValueError("No patient records found.")

        print("\n========== PATIENT REPORT ==========\n")

        print(f"Total Registered Patients : {len(patients)}")

        # -----------------------------
        # City Wise
        # -----------------------------
        city_count = {}

        for patient in patients:
            city = patient["city"]
            city_count[city] = city_count.get(city, 0) + 1

        print("\nPatients City-wise")
        for city, count in city_count.items():
            print(f"{city:<20} : {count}")

        # -----------------------------
        # Disease Wise
        # -----------------------------
        disease_count = {}

        for patient in patients:
            disease = patient["disease"]
            disease_count[disease] = disease_count.get(disease, 0) + 1

        print("\nPatients Disease-wise")
        for disease, count in disease_count.items():
            print(f"{disease:<20} : {count}")

        # -----------------------------
        # Blood Group Wise
        # -----------------------------
        blood_count = {}

        for patient in patients:
            blood = patient["blood_group"]
            blood_count[blood] = blood_count.get(blood, 0) + 1

        print("\nBlood Group-wise")
        for blood, count in blood_count.items():
            print(f"{blood:<5} : {count}")

        # -----------------------------
        # Gender Wise
        # -----------------------------
        gender_count = {}

        for patient in patients:
            gender = patient["gender"]
            gender_count[gender] = gender_count.get(gender, 0) + 1

        print("\nGender-wise")
        for gender, count in gender_count.items():
            print(f"{gender:<10} : {count}")

        # -----------------------------
        # Older than 60
        # -----------------------------
        print("\nPatients Older Than 60 Years")

        found = False

        for patient in patients:
            if patient["age"] > 60:
                print(
                    patient["patient_id"],
                    patient["name"],
                    patient["age"]
                )
                found = True

        if not found:
            print("None")

        # -----------------------------
        # Youngest Patient
        # -----------------------------
        youngest = min(
            patients,
            key=lambda x: x["age"]
        )

        print("\nYoungest Patient")
        print(
            youngest["patient_id"],
            youngest["name"],
            youngest["age"]
        )

        # -----------------------------
        # Oldest Patient
        # -----------------------------
        oldest = max(
            patients,
            key=lambda x: x["age"]
        )

        print("\nOldest Patient")
        print(
            oldest["patient_id"],
            oldest["name"],
            oldest["age"]
        )

        logger.info("Patient report generated.")

    except ValueError as e:
        print(e)
        logger.error(str(e))

    except Exception as e:
        print(e)
        logger.exception("Patient report error.")

    finally:
        print()


# ----------------------------------------
# Generate Doctor Reports
# ----------------------------------------

def generate_doctor_reports():

    try:

        if not doctors:
            raise ValueError("No doctor records found.")

        print("\n========== DOCTOR REPORT ==========\n")

        print(f"Total Doctors : {len(doctors)}")

        # -----------------------------
        # Department Wise
        # -----------------------------
        department_count = {}

        for doctor in doctors:

            department = doctor["department"]

            department_count[department] = (
                department_count.get(department, 0) + 1
            )

        print("\nDoctors Department-wise")

        for department, count in department_count.items():
            print(f"{department:<20} : {count}")

        # -----------------------------
        # Availability
        # -----------------------------
        available = 0
        unavailable = 0
        on_leave = 0

        for doctor in doctors:

            status = doctor["availability_status"]

            if status == "Available":
                available += 1

            elif status == "Unavailable":
                unavailable += 1

            elif status == "On Leave":
                on_leave += 1

        print("\nAvailability Report")
        print(f"Available     : {available}")
        print(f"Unavailable   : {unavailable}")
        print(f"On Leave      : {on_leave}")

        # -----------------------------
        # Highest Fee
        # -----------------------------
        highest = max(
            doctors,
            key=lambda x: x["consultation_fee"]
        )

        print("\nHighest Consultation Fee")
        print(
            highest["doctor_name"],
            highest["consultation_fee"]
        )

        # -----------------------------
        # Lowest Fee
        # -----------------------------
        lowest = min(
            doctors,
            key=lambda x: x["consultation_fee"]
        )

        print("\nLowest Consultation Fee")
        print(
            lowest["doctor_name"],
            lowest["consultation_fee"]
        )

        logger.info("Doctor report generated.")

    except ValueError as e:
        print(e)
        logger.error(str(e))

    except Exception as e:
        print(e)
        logger.exception("Doctor report error.")

    finally:
        print()

# ----------------------------------------
# Generate Appointment Reports
# ----------------------------------------

def generate_appointment_reports():

    try:

        if not appointments:
            raise ValueError("No appointment records found.")

        print("\n========== APPOINTMENT REPORT ==========\n")

        print(f"Total Appointments : {len(appointments)}")

        scheduled = 0
        completed = 0
        cancelled = 0

        doctor_count = {}
        department_count = {}
        patient_count = {}

        for appointment in appointments:

            if appointment["status"] == "Scheduled":
                scheduled += 1

            elif appointment["status"] == "Completed":
                completed += 1

            elif appointment["status"] == "Cancelled":
                cancelled += 1

            doctor_id = appointment["doctor_id"]
            doctor_count[doctor_id] = doctor_count.get(doctor_id, 0) + 1

            patient_id = appointment["patient_id"]
            patient_count[patient_id] = patient_count.get(patient_id, 0) + 1

            for doctor in doctors:
                if doctor["doctor_id"] == doctor_id:
                    department = doctor["department"]
                    department_count[department] = (
                        department_count.get(department, 0) + 1
                    )
                    break

        print(f"Scheduled Appointments : {scheduled}")
        print(f"Completed Appointments : {completed}")
        print(f"Cancelled Appointments : {cancelled}")

        print("\nAppointments Doctor-wise")

        for doctor_id, count in doctor_count.items():
            print(f"{doctor_id:<10} : {count}")

        print("\nAppointments Department-wise")

        for department, count in department_count.items():
            print(f"{department:<20} : {count}")

        highest_doctor = max(
            doctor_count,
            key=doctor_count.get
        )

        highest_patient = max(
            patient_count,
            key=patient_count.get
        )

        print("\nDoctor with Highest Appointments")
        print(highest_doctor,
              doctor_count[highest_doctor])

        print("\nPatient with Highest Appointments")
        print(highest_patient,
              patient_count[highest_patient])

        logger.info("Appointment report generated.")

    except ValueError as e:
        print(e)
        logger.error(str(e))

    except Exception as e:
        print(e)
        logger.exception("Appointment report error.")

    finally:
        print()


# ----------------------------------------
# Generate Billing Reports
# ----------------------------------------

def generate_billing_reports():

    try:

        if not bills:
            raise ValueError("No billing records found.")

        print("\n========== BILLING REPORT ==========\n")

        print(f"Total Bills : {len(bills)}")

        total_revenue = sum(
            bill["total_amount"] for bill in bills
        )

        total_paid = sum(
            bill["total_amount"]
            for bill in bills
            if bill["payment_status"] == "Paid"
        )

        total_pending = sum(
            bill["total_amount"]
            for bill in bills
            if bill["payment_status"] == "Pending"
        )

        average_bill = total_revenue / len(bills)

        highest_bill = max(
            bills,
            key=lambda x: x["total_amount"]
        )

        lowest_bill = min(
            bills,
            key=lambda x: x["total_amount"]
        )

        print(f"Total Revenue       : {total_revenue}")
        print(f"Total Paid Amount   : {total_paid}")
        print(f"Total Pending Amount: {total_pending}")
        print(f"Average Bill Amount : {average_bill:.2f}")

        print("\nHighest Bill")
        print(
            highest_bill["bill_id"],
            highest_bill["total_amount"]
        )

        print("\nLowest Bill")
        print(
            lowest_bill["bill_id"],
            lowest_bill["total_amount"]
        )

        # -----------------------------
        # Patient with Highest Bill
        # -----------------------------
        patient_bill = {}

        for bill in bills:

            patient_bill[bill["patient_id"]] = (
                patient_bill.get(
                    bill["patient_id"], 0
                )
                + bill["total_amount"]
            )

        highest_patient = max(
            patient_bill,
            key=patient_bill.get
        )

        print("\nPatient with Highest Total Bill")
        print(
            highest_patient,
            patient_bill[highest_patient]
        )

        # -----------------------------
        # Pending Payments
        # -----------------------------
        print("\nPatients with Pending Payments")

        found = False

        for bill in bills:

            if bill["payment_status"] == "Pending":

                print(
                    bill["patient_id"],
                    bill["bill_id"],
                    bill["total_amount"]
                )

                found = True

        if not found:
            print("No Pending Payments")

        logger.info("Billing report generated.")

    except ValueError as e:
        print(e)
        logger.error(str(e))

    except ZeroDivisionError:
        print("Average cannot be calculated.")
        logger.exception("Division by zero.")

    except Exception as e:
        print(e)
        logger.exception("Billing report error.")

    finally:
        print()