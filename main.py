"""
---------------------------------------------------------
Project : Healthcare Management System
File    : main.py
---------------------------------------------------------
"""

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
    search_doctor,
    update_doctor,
    delete_doctor
)

from appointment_module import (
    book_appointment,
    view_all_appointments,
    search_appointment,
    update_appointment_status,
    cancel_appointment
)

from billing_module import (
    generate_bill,
    view_all_bills,
    search_bill,
    update_payment_status
)

from report_module import (
    patient_report,
    doctor_report,
    appointment_report,
    billing_report
)

from database_connection import get_connection


# ---------------------------------------------------------
# Report Menu
# ---------------------------------------------------------

def reports_menu():

    while True:

        print("\n========== REPORTS ==========")
        print("1. Patient Report")
        print("2. Doctor Report")
        print("3. Appointment Report")
        print("4. Billing Report")
        print("5. Back")

        choice = input("Enter your choice : ").strip()

        if choice == "1":
            patient_report()

        elif choice == "2":
            doctor_report()

        elif choice == "3":
            appointment_report()

        elif choice == "4":
            billing_report()

        elif choice == "5":
            break

        else:
            print("Invalid Choice.")


# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------

def main():

    connection = get_connection()

    if connection is None:
        print("\nUnable to connect to the database.")
        print("Please check database_connection.py")
        return

    connection.close()

    while True:

        print("\n")
        print("=" * 65)
        print("        HEALTHCARE MANAGEMENT SYSTEM")
        print("=" * 65)

        print("\nPATIENT MANAGEMENT")
        print("1. Register Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")

        print("\nDOCTOR MANAGEMENT")
        print("6. Add Doctor")
        print("7. View All Doctors")
        print("8. Search Doctor")
        print("9. Update Doctor")
        print("10. Delete Doctor")

        print("\nAPPOINTMENT MANAGEMENT")
        print("11. Book Appointment")
        print("12. View All Appointments")
        print("13. Search Appointment")
        print("14. Update Appointment Status")
        print("15. Cancel Appointment")

        print("\nBILLING MANAGEMENT")
        print("16. Generate Bill")
        print("17. View All Bills")
        print("18. Search Bill")
        print("19. Update Payment Status")

        print("\nREPORTS")
        print("20. Reports")

        print("\n21. Exit")

        choice = input("\nEnter Your Choice : ").strip()

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
                update_doctor()

            elif choice == "10":
                delete_doctor()

            elif choice == "11":
                book_appointment()

            elif choice == "12":
                view_all_appointments()

            elif choice == "13":
                search_appointment()

            elif choice == "14":
                update_appointment_status()

            elif choice == "15":
                cancel_appointment()

            elif choice == "16":
                generate_bill()

            elif choice == "17":
                view_all_bills()

            elif choice == "18":
                search_bill()

            elif choice == "19":
                update_payment_status()

            elif choice == "20":
                reports_menu()

            elif choice == "21":
                print("\nThank you for using Healthcare Management System.")
                break

            else:
                print("\nInvalid Choice. Please try again.")

        except KeyboardInterrupt:
            print("\n\nProgram Interrupted by User.")
            break

        except Exception as e:
            print("\nUnexpected Error :", e)


# ---------------------------------------------------------
# Driver Code
# ---------------------------------------------------------

if __name__ == "__main__":
    main()