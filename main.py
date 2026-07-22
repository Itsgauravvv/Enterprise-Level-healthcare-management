from patient_module import (
    register_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient
)

from doctor_module import (
    add_doctor,
    view_all_doctors,
    search_doctor
)

from appointment_module import (
    book_appointment,
    view_all_appointments,
    cancel_appointment,
    complete_appointment
)

from billing_module import (
    generate_bill,
    view_all_bills,
    search_patient_bills,
    update_payment_status
)

from report_module import (
    generate_patient_reports,
    generate_doctor_reports,
    generate_appointment_reports,
    generate_billing_reports
)


# ----------------------------------------
# Display Reports Menu
# ----------------------------------------

def display_reports():

    while True:

        print("\n========== Healthcare Reports ==========")
        print("1. Patient Reports")
        print("2. Doctor Reports")
        print("3. Appointment Reports")
        print("4. Billing Reports")
        print("5. Back")

        choice = input("Enter your choice : ").strip()

        if choice == "1":
            generate_patient_reports()

        elif choice == "2":
            generate_doctor_reports()

        elif choice == "3":
            generate_appointment_reports()

        elif choice == "4":
            generate_billing_reports()

        elif choice == "5":
            break

        else:
            print("Invalid Choice.")


# ----------------------------------------
# Main Menu
# ----------------------------------------

def main():

    while True:

        print("\n")
        print("=" * 60)
        print("        HEALTHCARE MANAGEMENT SYSTEM")
        print("=" * 60)

        print("1. Register Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")

        print("6. Add Doctor")
        print("7. View All Doctors")
        print("8. Search Doctor")

        print("9. Book Appointment")
        print("10. View All Appointments")
        print("11. Cancel Appointment")
        print("12. Complete Appointment")

        print("13. Generate Patient Bill")
        print("14. View All Bills")
        print("15. Search Patient Bills")
        print("16. Update Payment Status")

        print("17. Healthcare Reports")

        print("18. Exit")

        choice = input("\nEnter your choice : ").strip()

        try:

            if choice == "1":
                register_patient()

            elif choice == "2":
                view_all_patients()

            elif choice == "3":
                search_patient()

            elif choice == "4":
                update_patient()

            elif choice == "5":
                delete_patient()

            elif choice == "6":
                add_doctor()

            elif choice == "7":
                view_all_doctors()

            elif choice == "8":
                search_doctor()

            elif choice == "9":
                book_appointment()

            elif choice == "10":
                view_all_appointments()

            elif choice == "11":
                cancel_appointment()

            elif choice == "12":
                complete_appointment()

            elif choice == "13":
                generate_bill()

            elif choice == "14":
                view_all_bills()

            elif choice == "15":
                search_patient_bills()

            elif choice == "16":
                update_payment_status()

            elif choice == "17":
                display_reports()

            elif choice == "18":
                print("\nThank You for Using Healthcare Management System")
                break

            else:
                raise ValueError("Invalid Menu Choice.")

        except ValueError as e:
            print("\nError :", e)

        except KeyboardInterrupt:
            print("\nProgram Interrupted.")
            break

        except Exception as e:
            print("\nUnexpected Error :", e)


# ----------------------------------------
# Driver Code
# ----------------------------------------

if __name__ == "__main__":
    main()