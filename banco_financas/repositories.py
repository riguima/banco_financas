from datetime import datetime, date

from models import AccountModel, TransactionModel, ClientModel
from database import Session
from domain import IAccountRepository, Transaction, Client, Account


class AccountRepository(IAccountRepository):

    def all(self) -> list[Account]:
        with Session() as session:
            client = self.get_current_client(session)
            return [Account(a.name) for a in client.accounts]

    def add(self, account_name: str) -> None:
        with Session() as session:
            client = self.get_current_client(session)
            client.accounts.append(
                AccountModel(name=account_name)
            )
            session.commit()

    def delete(self, account_name: str) -> None:
        with Session() as session:
            client = self.get_current_client(session)
            m = session.query(AccountModel).filter_by(
                client_name=client.name, name=account_name
            ).first()
            session.delete(m)
            session.commit()

    def delete_transaction(self, transaction_id: int) -> None:
        with Session() as session:
            transaction = session.query(TransactionModel).get(transaction_id)
            if transaction:
                session.delete(transaction)
                session.commit()

    def make_transaction(self, account_name: str, value: float) -> None:
        with Session() as session:
            client = self.get_current_client(session)
            account = session.query(AccountModel).filter_by(
                client_name=client.name, name=account_name
            ).first()
            transaction = TransactionModel(
                value=value, account=account, client=client)
            session.add(transaction)
            session.commit()

    def get_transactions(self, account_name: str,
                         start_date: date = datetime.now().date(),
                         final_date: date = datetime.now().date()) -> list[Transaction]:
        with Session() as session:
            client = self.get_current_client(session)
            account = session.query(AccountModel).filter_by(
                client_name=client.name, name=account_name
            ).first()
            result = []
            for m in account.transactions:
                if start_date <= m.date <= final_date:
                    result.append(
                        Transaction(
                            id=m.id, date=m.date, value=m.value,
                            source_of_income=m.source_of_income)
                    )
            return result

    def get_current_client(self, session: Session) -> Client:
        with open('current_client.txt', 'r') as f:
            return session.query(ClientModel).get(f.readlines()[0])
