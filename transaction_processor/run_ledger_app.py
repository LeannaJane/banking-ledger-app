from transaction_processor.processor import (
    welcome_screen,
    input_account_id,
    run_transaction_loop,
    load_ledger,
    get_balance,
    print_ledger,
    safe_input
)
from transaction_processor.errors import UserExit

def run_app():
    """Main app entry point"""
    ledger = load_ledger()

    try:
        while True:
            try:
                choice = welcome_screen()
            except UserExit:
                print("\nExiting the app. Goodbye!\n")
                break

            if choice == "3":
                print("\nExiting the ledger. Goodbye!\n")
                break
            elif choice == "2":
                try:
                    account_id = safe_input("\nEnter your Account ID to check balance/ledger: ")
                except UserExit:
                    continue

                balance = get_balance(account_id, ledger)
                print(f"\nCurrent balance for account {account_id}: {balance}\n")

                print("Ledger for this account:")
                print_ledger(ledger, account_id=account_id)

                input("\nPress Enter to return to main menu...")
                continue
            elif choice != "1":
                print("Invalid choice, try again.")
                continue

            try:
                account_id = input_account_id()
            except UserExit:
                print("\nReturning to welcome screen...\n")
                continue

            run_transaction_loop(account_id, ledger)
    
    except KeyboardInterrupt:
        print("\nReturning to main menu...\n")


