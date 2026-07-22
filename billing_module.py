from data_store import patients, appointments, bills
from validation_module import (
    validate_bill_id,
    validate_amount,
    validate_discount,
    validate_payment_status
)
from logger_module import logger


# ----------------------------------------
# Generate Patient Bill
# ----------------------------------------

def generate_bill():

    try:

        bill_id = input("Enter Bill ID : ").strip()
        validate_bill_id(bill_id)

        # Duplicate Bill ID
        for bill in bills:
            if bill["bill_id"] == bill_id:
                logger.warning(f"Duplicate Bill ID {bill_id}")
                raise ValueError("Bill ID already exists.")

        patient_id = input("Enter Patient ID : ").strip()

        patient_found = False

        for patient in patients:
            if patient["patient_id"] == patient_id:
                patient_found = True
                break

        if not patient_found:
            raise ValueError("Patient ID does not exist.")

        appointment_id = input("Enter Appointment ID : ").strip()

        appointment = None

        for app in appointments:
            if app["appointment_id"] == appointment_id:
                appointment = app
                break

        if appointment is None:
            raise ValueError("Appointment ID does not exist.")

        if appointment["patient_id"] != patient_id:
            raise ValueError(
                "Appointment does not belong to this patient."
            )

        if appointment["status"] != "Completed":
            raise ValueError(
                "Bill can be generated only for completed appointments."
            )

        # Only one bill per appointment
        for bill in bills:
            if bill["appointment_id"] == appointment_id:
                raise ValueError(
                    "Bill already generated for this appointment."
                )

        consultation_fee = float(
            input("Consultation Fee : ").strip()
        )
        validate_amount(consultation_fee)

        medicine_charges = float(
            input("Medicine Charges : ").strip()
        )
        validate_amount(medicine_charges)

        laboratory_charges = float(
            input("Laboratory Charges : ").strip()
        )
        validate_amount(laboratory_charges)

        room_charges = float(
            input("Room Charges : ").strip()
        )
        validate_amount(room_charges)

        gross_amount = (
            consultation_fee
            + medicine_charges
            + laboratory_charges
            + room_charges
        )

        discount = float(
            input("Discount : ").strip()
        )

        validate_discount(discount, gross_amount)

        total_amount = gross_amount - discount

        if total_amount < 0:
            raise ValueError(
                "Total amount cannot be negative."
            )

        payment_status = input(
            "Payment Status (Paid/Pending): "
        ).strip().title()

        validate_payment_status(payment_status)

        bill = {

            "bill_id": bill_id,
            "patient_id": patient_id,
            "appointment_id": appointment_id,
            "consultation_fee": consultation_fee,
            "medicine_charges": medicine_charges,
            "laboratory_charges": laboratory_charges,
            "room_charges": room_charges,
            "gross_amount": gross_amount,
            "discount": discount,
            "total_amount": total_amount,
            "payment_status": payment_status

        }

        bills.append(bill)

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while generating bill."
        )

    else:

        print("\nBill Generated Successfully.")

        print("\n----------- BILL -----------")
        print(f"Bill ID           : {bill_id}")
        print(f"Patient ID        : {patient_id}")
        print(f"Appointment ID    : {appointment_id}")
        print(f"Gross Amount      : {gross_amount}")
        print(f"Discount          : {discount}")
        print(f"Total Amount      : {total_amount}")
        print(f"Payment Status    : {payment_status}")
        print("-----------------------------")

        logger.info(
            f"Bill {bill_id} generated successfully."
        )

    finally:

        print()

# ----------------------------------------
# Display Bill Details
# ----------------------------------------

def display_bill(bill):

    patient_name = "Unknown"

    for patient in patients:
        if patient["patient_id"] == bill["patient_id"]:
            patient_name = patient["name"]
            break

    print("-" * 60)
    print(f"Bill ID          : {bill['bill_id']}")
    print(f"Patient ID       : {bill['patient_id']}")
    print(f"Patient Name     : {patient_name}")
    print(f"Appointment ID   : {bill['appointment_id']}")
    print(f"Gross Amount     : {bill['gross_amount']}")
    print(f"Discount         : {bill['discount']}")
    print(f"Total Amount     : {bill['total_amount']}")
    print(f"Payment Status   : {bill['payment_status']}")
    print("-" * 60)


# ----------------------------------------
# View All Bills
# ----------------------------------------

def view_all_bills():

    try:

        if len(bills) == 0:
            raise ValueError("No bills found.")

        print("\n========== BILL LIST ==========\n")

        total_revenue = 0
        total_paid = 0
        total_pending = 0

        for bill in bills:

            display_bill(bill)

            total_revenue += bill["total_amount"]

            if bill["payment_status"] == "Paid":
                total_paid += bill["total_amount"]
            else:
                total_pending += bill["total_amount"]

        print("\n========== BILL SUMMARY ==========")
        print(f"Total Bills        : {len(bills)}")
        print(f"Total Revenue      : {total_revenue}")
        print(f"Total Paid Amount  : {total_paid}")
        print(f"Total Pending      : {total_pending}")

        if len(bills) > 0:
            print(
                f"Average Bill Amount : "
                f"{total_revenue / len(bills):.2f}"
            )

    except ValueError as e:

        print("\nError :", e)
        logger.warning(str(e))

    except ZeroDivisionError:

        print("\nAverage cannot be calculated.")
        logger.exception("Division by zero.")

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while viewing bills."
        )

    finally:

        print()

# ----------------------------------------
# Search Patient Bills
# ----------------------------------------

def search_patient_bills():

    try:

        if not bills:
            raise ValueError("No bills found.")

        patient_id = input("Enter Patient ID : ").strip()

        patient_found = False

        for patient in patients:
            if patient["patient_id"] == patient_id:
                patient_found = True
                patient_name = patient["name"]
                break

        if not patient_found:
            raise ValueError("Patient ID does not exist.")

        patient_bills = []

        total_billed = 0
        total_paid = 0
        total_pending = 0

        for bill in bills:

            if bill["patient_id"] == patient_id:

                patient_bills.append(bill)

                total_billed += bill["total_amount"]

                if bill["payment_status"] == "Paid":
                    total_paid += bill["total_amount"]
                else:
                    total_pending += bill["total_amount"]

        if not patient_bills:
            raise ValueError(
                "No bills found for this patient."
            )

        print("\n========== PATIENT BILL DETAILS ==========\n")
        print(f"Patient ID   : {patient_id}")
        print(f"Patient Name : {patient_name}\n")

        for bill in patient_bills:
            display_bill(bill)

        print("\n========== BILL SUMMARY ==========")
        print(f"Total Bills        : {len(patient_bills)}")
        print(f"Total Billed       : {total_billed}")
        print(f"Total Paid         : {total_paid}")
        print(f"Total Pending      : {total_pending}")

        logger.info(
            f"Displayed bills for Patient {patient_id}"
        )

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while searching patient bills."
        )

    finally:

        print()


# ----------------------------------------
# Update Payment Status
# ----------------------------------------

def update_payment_status():

    try:

        if not bills:
            raise ValueError("No bills found.")

        bill_id = input(
            "Enter Bill ID : "
        ).strip()

        bill = None

        for record in bills:
            if record["bill_id"] == bill_id:
                bill = record
                break

        if bill is None:
            raise ValueError("Bill ID does not exist.")

        if bill["payment_status"] == "Paid":
            raise ValueError(
                "Payment is already completed."
            )

        print("\nCurrent Payment Status :",
              bill["payment_status"])

        confirm = input(
            "Mark this bill as Paid? (Y/N): "
        ).strip().upper()

        if confirm != "Y":

            print("\nPayment update cancelled.")
            logger.info(
                f"Payment update cancelled for Bill {bill_id}"
            )
            return

        bill["payment_status"] = "Paid"

        logger.info(
            f"Payment updated for Bill {bill_id}"
        )

    except ValueError as e:

        print("\nError :", e)
        logger.error(str(e))

    except Exception as e:

        print("\nUnexpected Error :", e)
        logger.exception(
            "Unexpected error while updating payment."
        )

    else:

        print("\nPayment Status Updated Successfully.")

    finally:

        print()