from data_store import doctors
from validation_module import (
    validate_doctor_id,
    validate_name,
    validate_department,
    validate_consultation_fee,
    validate_availability_status
)
from logger_module import logger


# ----------------------------------------
# Display Doctor Details
# ----------------------------------------

def display_doctor(doctor):

    print("-" * 50)
    print(f"Doctor ID           : {doctor['doctor_id']}")
    print(f"Doctor Name         : {doctor['doctor_name']}")
    print(f"Department          : {doctor['department']}")
    print(f"Consultation Fee    : {doctor['consultation_fee']}")
    print(f"Availability Status : {doctor['availability_status']}")
    print("-" * 50)


# ----------------------------------------
# Add Doctor
# ----------------------------------------

def add_doctor():

    try:

        doctor_id = input("Enter Doctor ID : ").strip()
        validate_doctor_id(doctor_id)

        # Check duplicate Doctor ID
        for doctor in doctors:
            if doctor["doctor_id"] == doctor_id:
                logger.warning(f"Duplicate Doctor ID {doctor_id}")
                raise ValueError("Doctor ID already exists.")

        doctor_name = input("Enter Doctor Name : ").strip()
        validate_name(doctor_name)

        department = input("Enter Department : ").strip()
        validate_department(department)

        consultation_fee = input("Enter Consultation Fee : ").strip()
        validate_consultation_fee(consultation_fee)

        print("\nAvailability Status")
        print("1. Available")
        print("2. Unavailable")
        print("3. On Leave")

        choice = input("Choose Status : ").strip()

        if choice == "1":
            availability_status = "Available"
        elif choice == "2":
            availability_status = "Unavailable"
        elif choice == "3":
            availability_status = "On Leave"
        else:
            raise ValueError("Invalid availability status.")

        validate_availability_status(availability_status)

        doctor = {
            "doctor_id": doctor_id,
            "doctor_name": doctor_name.title(),
            "department": department.title(),
            "consultation_fee": float(consultation_fee),
            "availability_status": availability_status
        }

        doctors.append(doctor)

    except ValueError as e:
        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:
        print("\nUnexpected Error :", e)
        logger.exception("Unexpected error while adding doctor.")

    else:
        print("\nDoctor Added Successfully.")
        logger.info(f"Doctor {doctor_id} added successfully.")

    finally:
        print()


# ----------------------------------------
# View All Doctors
# ----------------------------------------

def view_all_doctors():

    try:

        if len(doctors) == 0:
            raise ValueError("No doctor records found.")

        print("\n========== Doctor List ==========\n")

        for doctor in doctors:
            display_doctor(doctor)

        print(f"\nTotal Doctors : {len(doctors)}")

    except ValueError as e:
        print(e)
        logger.warning(str(e))

    except Exception as e:
        print("Unexpected Error :", e)
        logger.exception("Error while viewing doctors.")

    finally:
        print()

# ----------------------------------------
# Search Doctor
# ----------------------------------------

def search_doctor():

    try:

        if not doctors:
            raise ValueError("No doctor records found.")

        print("\nSearch Doctor By")
        print("1. Doctor ID")
        print("2. Doctor Name")
        print("3. Department")
        print("4. Availability Status")

        choice = input("Enter your choice : ").strip()

        found = []

        if choice == "1":

            doctor_id = input("Enter Doctor ID : ").strip()

            for doctor in doctors:
                if doctor["doctor_id"] == doctor_id:
                    found.append(doctor)

        elif choice == "2":

            doctor_name = input("Enter Doctor Name : ").strip().lower()

            for doctor in doctors:
                if doctor["doctor_name"].lower() == doctor_name:
                    found.append(doctor)

        elif choice == "3":

            department = input("Enter Department : ").strip().lower()

            for doctor in doctors:
                if doctor["department"].lower() == department:
                    found.append(doctor)

        elif choice == "4":

            print("\nAvailability Status")
            print("1. Available")
            print("2. Unavailable")
            print("3. On Leave")

            status_choice = input("Choose Status : ").strip()

            if status_choice == "1":
                status = "Available"
            elif status_choice == "2":
                status = "Unavailable"
            elif status_choice == "3":
                status = "On Leave"
            else:
                raise ValueError("Invalid Availability Status.")

            for doctor in doctors:
                if doctor["availability_status"].lower() == status.lower():
                    found.append(doctor)

        else:
            raise ValueError("Invalid Search Option.")

        if not found:

            print("\nNo matching doctor found.")
            logger.warning("Doctor search returned no matching records.")

        else:

            print(f"\n{len(found)} Record(s) Found\n")

            for doctor in found:
                display_doctor(doctor)

            logger.info("Doctor search completed successfully.")

    except ValueError as e:
        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:
        print("\nUnexpected Error :", e)
        logger.exception("Unexpected error while searching doctor.")

    finally:
        print()