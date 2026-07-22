from data_store import patients, doctors, appointments
from validation_module import (
    validate_appointment_id,
    validate_date,
    validate_time
)
from logger_module import logger


# ----------------------------------------
# Display Appointment Details
# ----------------------------------------

def display_appointment(appointment):

    patient_name = "Unknown"
    doctor_name = "Unknown"
    department = "Unknown"

    for patient in patients:
        if patient["patient_id"] == appointment["patient_id"]:
            patient_name = patient["name"]
            break

    for doctor in doctors:
        if doctor["doctor_id"] == appointment["doctor_id"]:
            doctor_name = doctor["doctor_name"]
            department = doctor["department"]
            break

    print("-" * 60)
    print(f"Appointment ID   : {appointment['appointment_id']}")
    print(f"Patient ID       : {appointment['patient_id']}")
    print(f"Patient Name     : {patient_name}")
    print(f"Doctor ID        : {appointment['doctor_id']}")
    print(f"Doctor Name      : {doctor_name}")
    print(f"Department       : {department}")
    print(f"Appointment Date : {appointment['appointment_date']}")
    print(f"Appointment Time : {appointment['appointment_time']}")
    print(f"Status           : {appointment['status']}")
    print("-" * 60)


# ----------------------------------------
# Book Appointment
# ----------------------------------------

def book_appointment():

    try:

        appointment_id = input("Enter Appointment ID : ").strip()
        validate_appointment_id(appointment_id)

        # Duplicate Appointment ID
        for appointment in appointments:
            if appointment["appointment_id"] == appointment_id:
                logger.warning(
                    f"Duplicate Appointment ID {appointment_id}"
                )
                raise ValueError(
                    "Appointment ID already exists."
                )

        patient_id = input("Enter Patient ID : ").strip()

        patient_exists = False

        for patient in patients:
            if patient["patient_id"] == patient_id:
                patient_exists = True
                break

        if not patient_exists:
            raise ValueError("Patient ID does not exist.")

        doctor_id = input("Enter Doctor ID : ").strip()

        doctor_found = False
        doctor_available = False

        for doctor in doctors:

            if doctor["doctor_id"] == doctor_id:

                doctor_found = True

                if doctor["availability_status"] != "Available":
                    logger.warning(
                        f"Doctor {doctor_id} is unavailable."
                    )
                    raise ValueError(
                        "Doctor is currently unavailable."
                    )

                doctor_available = True
                break

        if not doctor_found:
            raise ValueError("Doctor ID does not exist.")

        if not doctor_available:
            raise ValueError("Doctor is unavailable.")

        appointment_date = input(
            "Enter Appointment Date (DD-MM-YYYY): "
        ).strip()

        validate_date(appointment_date)

        appointment_time = input(
            "Enter Appointment Time (HH:MM AM/PM): "
        ).strip()

        validate_time(appointment_time)

        # Check Slot Availability
        for appointment in appointments:

            if (
                appointment["doctor_id"] == doctor_id
                and appointment["appointment_date"] == appointment_date
                and appointment["appointment_time"] == appointment_time
                and appointment["status"] == "Scheduled"
            ):

                raise ValueError(
                    "Appointment slot is already booked."
                )

        appointment = {

            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "status": "Scheduled"

        }

        appointments.append(appointment)

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while booking appointment."
        )

    else:

        print("\nAppointment Booked Successfully.")
        logger.info(
            f"Appointment {appointment_id} booked successfully."
        )

    finally:

        print()

# ----------------------------------------
# View All Appointments
# ----------------------------------------

def view_all_appointments():

    try:

        if len(appointments) == 0:
            raise ValueError("No appointments found.")

        print("\n========== Appointment List ==========\n")

        for appointment in appointments:
            display_appointment(appointment)

        print(f"\nTotal Appointments : {len(appointments)}")

        scheduled = 0
        completed = 0
        cancelled = 0

        for appointment in appointments:

            if appointment["status"] == "Scheduled":
                scheduled += 1

            elif appointment["status"] == "Completed":
                completed += 1

            elif appointment["status"] == "Cancelled":
                cancelled += 1

        print("\nAppointment Summary")
        print("--------------------------")
        print(f"Scheduled : {scheduled}")
        print(f"Completed : {completed}")
        print(f"Cancelled : {cancelled}")

    except ValueError as e:

        print("\nError :", e)
        logger.warning(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while viewing appointments."
        )

    finally:

        print()

# ----------------------------------------
# Cancel Appointment
# ----------------------------------------

def cancel_appointment():

    try:

        if not appointments:
            raise ValueError("No appointments found.")

        appointment_id = input(
            "Enter Appointment ID to Cancel : "
        ).strip()

        appointment = None

        for record in appointments:
            if record["appointment_id"] == appointment_id:
                appointment = record
                break

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        if appointment["status"] == "Completed":
            raise ValueError(
                "Completed appointment cannot be cancelled."
            )

        if appointment["status"] == "Cancelled":
            raise ValueError(
                "Appointment is already cancelled."
            )

        confirm = input(
            "Are you sure you want to cancel? (Y/N): "
        ).strip().upper()

        if confirm != "Y":
            print("\nCancellation aborted.")
            logger.info(
                f"Cancellation aborted for Appointment {appointment_id}"
            )
            return

        appointment["status"] = "Cancelled"

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while cancelling appointment."
        )

    else:

        print("\nAppointment Cancelled Successfully.")
        logger.info(
            f"Appointment {appointment_id} cancelled successfully."
        )

    finally:

        print()


# ----------------------------------------
# Complete Appointment
# ----------------------------------------

def complete_appointment():

    try:

        if not appointments:
            raise ValueError("No appointments found.")

        appointment_id = input(
            "Enter Appointment ID to Complete : "
        ).strip()

        appointment = None

        for record in appointments:
            if record["appointment_id"] == appointment_id:
                appointment = record
                break

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        if appointment["status"] == "Cancelled":
            raise ValueError(
                "Cancelled appointment cannot be completed."
            )

        if appointment["status"] == "Completed":
            raise ValueError(
                "Appointment is already completed."
            )

        appointment["status"] = "Completed"

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while completing appointment."
        )

    else:

        print("\nAppointment Completed Successfully.")
        logger.info(
            f"Appointment {appointment_id} completed successfully."
        )

    finally:

        print()