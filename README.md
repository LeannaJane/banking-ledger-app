# Mini Banking Ledger (Python)

A command line banking ledger application written in Python, which allows users to record credit and debit transactions, track their balances.

---
## Project Structure

├── tests/
├── transaction_processor/
│   ├── __init__.py
│   ├── errors.py
│   ├── models.py
|   ├── processor.py
|   └── run_ledger_app.py
├── .gitignore
├── ledger.json
├── run.py
├── pyproject.toml
└── README.md

## Features

- Create **CREDIT** and **DEBIT** transactions
- Prevent overdrafts
- Prevent duplication transactions using idempotency keys
- Track balances
- Support multiple accounts in one ledger
- Save and retrieve data using JSON file
- Command Line interface
- Fully unit tested using pytest

## Programs behaviour
- All transactions are stored in a single ledger.json, this is created upon first credit transaction.
- Each transaction belongs to an account with an account_id
- Balances are calculated by filtering transactions per account_id

## Requirements
- Python 3.13+

## How to run

First create a virtual environment, and then install pytest and run the Python run script. The command pytest can be used to run the 17 unit tests.

```bash
python -m venv .venv
source .venv/bin/activate

pip install pytest

python run.py

pytest
```

## Example Usage
Below is an example session showing a credit followed by a debit
transaction for a single account.

```bash 
==================================================
         Welcome to Your Mini Banking Ledger      
==================================================
Options:
1. Start a transaction
2. Check balance
3. Exit

Enter choice (1/2/3): 1

Enter your Account ID: userA
Enter transaction type (CREDIT/DEBIT) or 'exit' to return: credit
Enter amount: 100

Account   Type   Amount    Idempotency                             Balance     
--------------------------------------------------------------------------------
userA     CREDIT 100       0cf29277-8d0e-496a-a5f8-6dd6d56557c3    100         

Do you want to enter another transaction? (y/n): y
Enter transaction type (CREDIT/DEBIT) or 'exit' to return: debit
Enter amount: 10

Account   Type   Amount    Idempotency                             Balance     
--------------------------------------------------------------------------------
userA     CREDIT 100       0cf29277-8d0e-496a-a5f8-6dd6d56557c3    100         
userA     DEBIT  10        a3e31a53-849e-4014-a15c-76452f8ba807    90          

Do you want to enter another transaction? (y/n): n

==================================================
         Welcome to Your Mini Banking Ledger      
==================================================
Options:
1. Start a transaction
2. Check balance
3. Exit

Enter choice (1/2/3): 3

Exiting the ledger. Goodbye!
```


