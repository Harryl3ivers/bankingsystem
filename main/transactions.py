from decimal import Decimal
from main.validator import Validator
import sqlite3


class Transaction:
    def __init__(self, db_path="bank.db"):
        self.validator = Validator()
        self.db_path = db_path

    def deposit(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)

        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=?",
                (account_number,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("Account not found")

            old_balance = Decimal(str(row[0]))
            new_balance = old_balance + amount

            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_number=?",
                (float(new_balance), account_number)
            )

            conn.commit()
            return new_balance

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def withdraw(self, account_number, amount):
        account_number = self.validator.account_number_validation(account_number)
        amount = self.validator.amount_validation(amount)

        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=?",
                (account_number,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("Account not found")

            old_balance = Decimal(str(row[0]))

            if old_balance < amount:
                raise ValueError("Insufficient funds")

            new_balance = old_balance - amount

            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_number=?",
                (float(new_balance), account_number)
            )

            conn.commit()
            return new_balance

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def transfer(self, from_account, to_account, amount):
        from_account = self.validator.account_number_validation(from_account)
        to_account = self.validator.account_number_validation(to_account)
        amount = self.validator.amount_validation(amount)

        if from_account == to_account:
            raise ValueError("Cannot transfer to the same account")

        conn = sqlite3.connect(self.db_path, isolation_level='IMMEDIATE')
        try:
            cursor = conn.cursor()

            # Get source account
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=?",
                (from_account,)
            )
            from_row = cursor.fetchone()

            # Get destination account
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=?",
                (to_account,)
            )
            to_row = cursor.fetchone()

            if not from_row or not to_row:
                raise ValueError("One or both accounts not found")

            from_balance = Decimal(str(from_row[0]))
            to_balance = Decimal(str(to_row[0]))

            if from_balance < amount:
                raise ValueError("Insufficient funds in the source account")

            new_from_balance = from_balance - amount
            new_to_balance = to_balance + amount

            # Update both accounts
            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_number=?",
                (float(new_from_balance), from_account)
            )

            cursor.execute(
                "UPDATE accounts SET balance=? WHERE account_number=?",
                (float(new_to_balance), to_account)
            )

            conn.commit()

            return {
                'from_account': from_account,
                'to_account': to_account,
                'amount': amount,
                'from_new_balance': new_from_balance,
                'to_new_balance': new_to_balance
            }

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()