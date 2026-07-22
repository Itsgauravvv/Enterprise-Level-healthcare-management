from data_store import patients, appointments
from validation_module import (
    validate_patient_id,
    validate_name,
    validate_age,
    validate_gender,
    validate_contact_number,
    validate_city,
    validate_blood_group,
    validate_disease
)
from logger_module import logger


# ----------------------------------------
# Display Patient Details
# ----------------------------------------

def display_patient(patient):
    print("-" * 50)
    print(f"Patient ID      : {patient['patient_id']}")
    print(f"Name            : {patient['name']}")
    print(f"Age             : {patient['age']}")
    print(f"Gender          : {patient['gender']}")
    print(f"Contact Number  : {patient['contact_number']}")
    print(f"City            : {patient['city']}")
    print(f"Blood Group     : {patient['blood_group']}")
    print(f"Disease         : {patient['disease']}")
    print("-" * 50)


# ----------------------------------------
# Register Patient
# ----------------------------------------

def register_patient():

    try:

        patient_id = input("Enter Patient ID : ").strip()

        validate_patient_id(patient_id)

        for patient in patients:
            if patient["patient_id"] == patient_id:
                logger.warning(f"Duplicate Patient ID {patient_id}")
                raise ValueError("Patient ID already exists.")

        name = input("Enter Patient Name : ").strip()
        validate_name(name)

        age = input("Enter Age : ").strip()
        validate_age(age)

        gender = input("Enter Gender (Male/Female/Other): ").strip()
        validate_gender(gender)

        contact = input("Enter Contact Number : ").strip()
        validate_contact_number(contact)

        city = input("Enter City : ").strip()
        validate_city(city)

        blood_group = input("Enter Blood Group : ").strip().upper()
        validate_blood_group(blood_group)

        disease = input("Enter Disease : ").strip()
        validate_disease(disease)

        patient = {
            "patient_id": patient_id,
            "name": name.title(),
            "age": int(age),
            "gender": gender.title(),
            "contact_number": contact,
            "city": city.title(),
            "blood_group": blood_group,
            "disease": disease.title()
        }

        patients.append(patient)

    except ValueError as e:
        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:
        print("\nUnexpected Error :", e)
        logger.exception("Unexpected error while registering patient.")

    else:
        print("\nPatient Registered Successfully.")
        logger.info(f"Patient {patient_id} registered successfully.")

    finally:
        print()


# ----------------------------------------
# View All Patients
# ----------------------------------------

def view_all_patients():

    try:

        if len(patients) == 0:
            raise ValueError("No patient records found.")

        print("\n========== Patient List ==========\n")

        for patient in patients:
            display_patient(patient)

        print(f"\nTotal Patients : {len(patients)}")

    except ValueError as e:
        print(e)
        logger.warning(str(e))

    except Exception as e:
        print("Unexpected Error :", e)
        logger.exception("Error while viewing patients.")

    finally:
        print()
# ----------------------------------------
# Search Patient
# ----------------------------------------

def search_patient():

    try:

        if not patients:
            raise ValueError("No patient records found.")

        print("\nSearch Patient By")
        print("1. Patient ID")
        print("2. Patient Name")
        print("3. Contact Number")
        print("4. City")
        print("5. Disease")
        print("6. Blood Group")

        choice = input("Enter your choice : ").strip()

        found = []

        if choice == "1":
            key = input("Enter Patient ID : ").strip()

            for patient in patients:
                if patient["patient_id"] == key:
                    found.append(patient)

        elif choice == "2":
            key = input("Enter Patient Name : ").strip().lower()

            for patient in patients:
                if patient["name"].lower() == key:
                    found.append(patient)

        elif choice == "3":
            key = input("Enter Contact Number : ").strip()

            for patient in patients:
                if patient["contact_number"] == key:
                    found.append(patient)

        elif choice == "4":
            key = input("Enter City : ").strip().lower()

            for patient in patients:
                if patient["city"].lower() == key:
                    found.append(patient)

        elif choice == "5":
            key = input("Enter Disease : ").strip().lower()

            for patient in patients:
                if patient["disease"].lower() == key:
                    found.append(patient)

        elif choice == "6":
            key = input("Enter Blood Group : ").strip().upper()

            for patient in patients:
                if patient["blood_group"].upper() == key:
                    found.append(patient)

        else:
            raise ValueError("Invalid Search Option.")

        if not found:
            print("\nNo matching patient found.")
            logger.warning("Patient search returned no records.")
        else:
            print(f"\n{len(found)} Record(s) Found\n")

            for patient in found:
                display_patient(patient)

            logger.info("Patient search completed successfully.")

    except Exception as e:
        print("Error :", e)
        logger.exception("Error while searching patient.")

    finally:
        print()


# ----------------------------------------
# Update Patient
# ----------------------------------------

def update_patient():

    try:

        if not patients:
            raise ValueError("No patient records found.")

        patient_id = input("Enter Patient ID to Update : ").strip()

        patient = None

        for record in patients:
            if record["patient_id"] == patient_id:
                patient = record
                break

        if patient is None:
            raise ValueError("Patient ID does not exist.")

        print("\nLeave a field blank to keep the old value.\n")

        name = input(f"Name ({patient['name']}) : ").strip()

        if name:
            validate_name(name)
            patient["name"] = name.title()

        age = input(f"Age ({patient['age']}) : ").strip()

        if age:
            validate_age(age)
            patient["age"] = int(age)

        gender = input(f"Gender ({patient['gender']}) : ").strip()

        if gender:
            validate_gender(gender)
            patient["gender"] = gender.title()

        contact = input(
            f"Contact Number ({patient['contact_number']}) : "
        ).strip()

        if contact:
            validate_contact_number(contact)
            patient["contact_number"] = contact

        city = input(f"City ({patient['city']}) : ").strip()

        if city:
            validate_city(city)
            patient["city"] = city.title()

        blood = input(
            f"Blood Group ({patient['blood_group']}) : "
        ).strip()

        if blood:
            validate_blood_group(blood)
            patient["blood_group"] = blood.upper()

        disease = input(
            f"Disease ({patient['disease']}) : "
        ).strip()

        if disease:
            validate_disease(disease)
            patient["disease"] = disease.title()

    except ValueError as e:
        print("Error :", e)
        logger.error(str(e))

    except Exception as e:
        print("Unexpected Error :", e)
        logger.exception("Unexpected error while updating patient.")

    else:
        print("\nPatient Updated Successfully.")
        logger.info(f"Patient {patient_id} updated successfully.")

    finally:
        print()

# ----------------------------------------
# Delete Patient
# ----------------------------------------

def delete_patient():

    try:

        if not patients:
            raise ValueError("No patient records found.")

        patient_id = input("Enter Patient ID to Delete : ").strip()

        patient = None

        for record in patients:
            if record["patient_id"] == patient_id:
                patient = record
                break

        if patient is None:
            raise ValueError("Patient ID does not exist.")

        # Check for scheduled appointments
        for appointment in appointments:
            if (
                appointment["patient_id"] == patient_id
                and appointment["status"] == "Scheduled"
            ):
                raise ValueError(
                    "Patient has a scheduled appointment. "
                    "Deletion is not allowed."
                )

        print("\nPatient Details")
        display_patient(patient)

        confirm = input(
            "\nAre you sure you want to delete this patient? (Y/N): "
        ).strip().upper()

        if confirm != "Y":
            print("\nDeletion Cancelled.")
            logger.info(f"Deletion cancelled for Patient {patient_id}")
            return

        patients.remove(patient)

    except ValueError as e:
        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:
        print("\nUnexpected Error :", e)
        logger.exception("Unexpected error while deleting patient.")

    else:
        print("\nPatient Deleted Successfully.")
        logger.info(f"Patient {patient_id} deleted successfully.")

    finally:
        print()