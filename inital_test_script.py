from decimal import Decimal
from transaction_processor.models import Transaction
from transaction_processor.processor import process_transaction, print_ledger
from transaction_processor.errors import OverdraftError, DuplicateTransactionError

ledger = []

print("Welcome to your mini banking ledger!")
print("Enter Transactions or type 'exit' to quit.\n")

while True:
    account_id = input("Account ID: ")
    if account_id.lower() == "exit":
        break

    tx_type = input("Type (CREDIT/DEBIT): ").upper()
    if tx_type.lower() == "exit":
        break
    if tx_type not in ["CREDIT", "DEBIT"]:
        print("Invalid type! Must be CREDIT or DEBIT.\n")
        continue

    amount_input = input("Amount: ")
    if amount_input.lower() == "exit":
        break
    try:
        amount = Decimal(amount_input)
    except:
        print("Invalid amount!\n")
        continue

    idempotency_key = input("Idempotency Key: ")
    if idempotency_key.lower() == "exit":
        break
    
    tx = Transaction(account_id=account_id, amount=amount, type=tx_type, idempotency_key=idempotency_key)

    try: 
        process_transaction(tx, ledger)
        print("Transaction Processed sucessfully!\n")
    except(OverdraftError, DuplicateTransactionError) as e:
        print (f"Error: {e}\n")

    print("Current Ledger:")
    print_ledger(ledger)
    print("\n" + "-"*60 + "\n")

print("Exiting. Final Ledger:")
print_ledger(ledger)

    