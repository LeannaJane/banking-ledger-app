from decimal import Decimal
from transaction_processor.models import Transaction
from transaction_processor.errors import UserExit, OverdraftError, DuplicateTransactionError
import os, json, uuid

LEDGER_FILE = "ledger.json"

# ---------- Helper functions ----------- #
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_idempotency_key():
    return str(uuid.uuid4())

def safe_input(prompt: str) -> str:
    """Wrap input() to allow the user to type 'exit' to quit."""
    value = input(prompt).strip()
    if value.lower() == "exit":
        raise UserExit()
    return value

from decimal import Decimal

def validate_amount(amount_input: str) -> Decimal:
    """Convert input string to Decimal and enforce >0."""
    try:
        amount = Decimal(amount_input)
    except:
        raise ValueError("Amount must be a number")

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    return amount

def welcome_screen():
    clear_console()
    print("==================================================")
    print("         Welcome to Your Mini Banking Ledger      ")
    print("==================================================")
    print("Options:")
    print("1. Start a transaction")
    print("2. Check balance")
    print("3. Exit")
    choice = safe_input("\nEnter choice (1/2/3): ")
    return choice.strip()

def input_account_id():
    """Ask user for their account ID"""
    return safe_input("\nEnter your Account ID: ")

def input_transaction():
    """Ask user for a single transaction and return a valid transaction tuple"""

    tx_type = safe_input("Enter transaction type (CREDIT/DEBIT) or 'exit' to return: ").upper()
    if tx_type not in ["CREDIT", "DEBIT"]:
        print("Invalid type! Must be CREDIT or DEBIT.\n")
        return None

    while True:
        amount_input = safe_input("Enter amount: ")
        try:
            amount = validate_amount(amount_input)
        except ValueError as e:
            print(f"{e}\n")
            continue
        break

    idempotency_key = generate_idempotency_key()
    return tx_type, amount, idempotency_key

# ---------- Transaction loop ----------- #
def run_transaction_loop(account_id, ledger):
    while True:
        try:
            tx_data = input_transaction()
        except UserExit:
            print("\nReturning to welcome screen...\n")
            break

        if not tx_data:
            continue

        tx_type, amount, idempotency_key = tx_data
        balance_before = get_balance(account_id, ledger)

        tx = Transaction(
            account_id=account_id,
            type=tx_type,
            amount=amount,
            idempotency_key=idempotency_key
        )

        try:
            process_transaction(tx, ledger)
            save_ledger(ledger)
            balance_after = get_balance(account_id, ledger)
            print("\nTransaction processed successfully!")
            print(f"Balance before: {balance_before}")
            print(f"Balance after : {balance_after}\n")
        except (OverdraftError, DuplicateTransactionError) as e:
            print(f"\nError: {e}\n")
            continue

        print("Your Current Ledger:")
        print_ledger(ledger, account_id=account_id)

        try:
            _continue = safe_input("\nDo you want to enter another transaction? (y/n): ").lower()
        except UserExit:
            print("\nReturning to welcome screen...\n")
            break

        if _continue != "y":
            print("\nReturning to welcome screen...\n")
            break

# ---------- Ledger functions ----------- #
def get_balance(account_id, ledger):
    """Compute balance for a given account"""
    balance = Decimal("0")
    for tx in ledger:
        if tx.account_id == account_id:
            if tx.type == "CREDIT":
                balance += tx.amount
            elif tx.type == "DEBIT":
                balance -= tx.amount
    return balance

def process_transaction(tx: Transaction, ledger: list):
    """Process a single transaction with validation rules"""
    # Check for duplicates
    for entry in ledger:
        if entry.idempotency_key == tx.idempotency_key:
            raise DuplicateTransactionError(f"Transaction {tx.idempotency_key} already exists!")

    # Check for overdraft
    if tx.type == "DEBIT":
        balance = get_balance(tx.account_id, ledger)
        if tx.amount > balance:
            raise OverdraftError(f"Account {tx.account_id} balance is too low!")

    ledger.append(tx)
    return "OK"

def print_ledger(ledger, account_id=None):
    """Print transactions in the ledger, optionally filtered by account_id"""
    clear_console()
    print(f"{'Account':<10}{'Type':<7}{'Amount':<10}{'Idempotency':<40}{'Balance':<12}")
    print("-" * 80)

    balances = {}

    for tx in ledger:
        acct = tx.account_id
        if acct not in balances:
            balances[acct] = Decimal("0")

        if tx.type == "CREDIT":
            balances[acct] += tx.amount
        elif tx.type == "DEBIT":
            balances[acct] -= tx.amount

        if account_id is None or acct == account_id:
            print(f"{tx.account_id:<10}{tx.type:<7}{tx.amount:<10}{tx.idempotency_key:<40}{balances[acct]:<12}")

def check_balance(ledger):
    account_id = safe_input("Enter your Account ID to check balance: ")
    balance = get_balance(account_id, ledger)
    print(f"\nCurrent Balance for account {account_id}: {balance}\n")
    input("Press Enter to return to the main menu...")

# ---------- JSON saving/loading ----------- #
def save_ledger(ledger, filename=LEDGER_FILE):
    data = [
        {
            "account_id": tx.account_id,
            "type": tx.type,
            "amount": str(tx.amount),
            "idempotency_key": tx.idempotency_key
        }
        for tx in ledger
    ]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_ledger(filename=LEDGER_FILE):
    ledger = []
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return ledger
            data = json.loads(content)
            for item in data:
                ledger.append(
                    Transaction(
                        account_id=item["account_id"],
                        type=item["type"],
                        amount=Decimal(item["amount"]),
                        idempotency_key=item["idempotency_key"]
                    )
                )
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Warning: JSON file is corrupt or invalid. Starting with empty ledger.")
        return []
    return ledger

