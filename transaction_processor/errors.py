
class OverdraftError(Exception):
    """Raised when a debit transaction would make the balance negative."""
    pass

class DuplicateTransactionError(Exception):
    """Raised when a transaction with the same idempotency key is already in the ledger. """
    pass    

class UserExit(Exception):
    """Raise this when the user wants to exit a transaction or the app."""
    pass