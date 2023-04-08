from datetime import datetime, date

from models import AccountModel, TransactionModel, ClientModel
from database import Session
from domain import IAccountRepository, Transaction, Client


class AccountRepository(IAccountRepository):

    def add(self, account_name: str) -> None:
        with Session() as session:
            self.get_current_client().accounts.append(
                AccountModel(name=account_name)
            )
            session.commit()

    def delete(self, account_name: str) -> None:
        with Session() as session:
            m = session.query(TransactionModel).filter_by(
                client_name=self.get_current_client().name, name=account_name
            ).first()
            session.delete(m)
            session.commit()

    def make_transaction(self, account_name: str, value: float) -> None:
        with Session() as session:
            account = session.query(AccountModel).filter_by(
                client_name=self.get_current_client().name, name=account_name
            ).first()
            account.transactions.append(TransactionModel(value=value))
            session.commit()

    def get_transactions(self, account_name: str,
                         start_date: date = datetime.now().date(),
                         end_date: date = datetime.now().date()) -> list[Transaction]:
        with Session() as session:
            models = session.query(TransactionModel).filter_by(
                client_name=self.get_current_client().name,
                account_name=account_name
            ).filter(start_date <= TransactionModel.date <= end_date).all()
            return [Transaction(m.id, m.date, m.value, m.source_of_income)
                    for m in models]

    def get_current_client(self) -> Client:
        with Session() as session:
            with open('current_client.txt', 'r') as f:
                model = session.query(ClientModel).get(f.readlines()[0])
                return Client(model.name, model.password)
