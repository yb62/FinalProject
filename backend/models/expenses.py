from typing import List, Dict
from models.user_base import *
from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel

class ExpenseMeta(Base):
    """
        This table / model contains metadata of different
        expenses created.
    """
    __tablename__ = "expenses_meta"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    paid_user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)

class Expense(Base):
    """
        This table / model is responsible for storing
        all the expenses relevant to a specific trip between
        its users. Note, if the user leaves the trip after having an expense
        they would still have the expense record to their name. Note, though,
        an expense can only be created between users that are part of the trip
        at the moment the expense is created.
    """
    __tablename__ = "expenses"
    owe_user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer) # We are storing numbers multiplied by 100 (i.e. 100$ -> 10000, 100.23$ -> 10023)
    expense_id = Column(Integer, ForeignKey("expenses_meta.id"))

class OweUserDetail(BaseModel):
    owe_user_id: int
    amount: int

class OweUserDetailWithName(BaseModel):
    owe_user_name: str
    amount: int

class CreateExpenseRequest(BaseModel):
    trip_id: int
    description: str
    paid_user_id: int
    details: List[OweUserDetail]

class CreateExpenseResponse(BaseModel):
    expense_id: int

class ExpenseDetails(BaseModel):
    expense_id: int
    paid_user_name: int
    total_paid: int
    details: List[OweUserDetailWithName]

class GetExpenses(BaseModel):
    expenses: List[ExpenseDetails]
    summary: Dict[str, Dict[str, int]]

def create_expenses(session, request: CreateExpenseRequest) -> CreateExpenseResponse:
    """
        This function creates an expense and adds its details to the database using the SQLAlchemy ORM.
        
        Args:
        - session: A SQLAlchemy session object that connects to a database.
        - request: An object of type CreateExpenseRequest that contains the details of the expense to be created.

        Returns:
        - A CreateExpenseResponse object that contains the id of the expense that was created.

        Example Usage:
        request = CreateExpenseRequest(trip_id=1, paid_user_id=1, description='Dinner with friends')
        detail1 = ExpenseDetail(owe_user_id=2, amount=20)
        detail2 = ExpenseDetail(owe_user_id=3, amount=30)
        request.details = [detail1, detail2]

        response = create_expenses(session, request)
        print(response.expense_id)
    """
    meta = ExpenseMeta(trip_id=request.trip_id, paid_user_id=request.paid_user_id, description=request.description)
    session.add(meta)
    session.commit()

    created_meta = session.query(ExpenseMeta).filter(ExpenseMeta.trip_id == meta.trip_id).last()

    for detail in request.details:
        session.add(Expense(
            owe_user_id=detail.owe_user_id,
            amount=detail.amount,
            expense_id=created_meta.id,
        ))
    session.commit()

    return CreateExpenseResponse(expense_id=created_meta.id)


def convert_expense(session, e: ExpenseMeta) -> ExpenseDetails:
    """
        Convert ExpenseMeta object into ExpenseDetails object.

        This function retrieves the relevant data from the ExpenseMeta object and queries the database to get the corresponding Expense and User objects. The retrieved data is then used to create an ExpenseDetails object that represents the expense in a user-friendly way.

        Args:
        - session: A SQLAlchemy session object that connects to a database.
        - e: An object of type ExpenseMeta that represents the expense to be converted.

        Returns:
        - An ExpenseDetails object that represents the expense in a user-friendly way.

        Raises:
        SQLAlchemyError: If an error occurs while querying the database.

        Example:
        expense_meta = session.query(ExpenseMeta).first()
        expense_details = convert_expense(session, expense_meta)
    """
    relevant_expenses: List[Expense] = session.query(Expense).filter(Expense.expense_id == e.id).all()
    paid_user: User = session.query(User).filter(User.id == e.paid_user_id).first()
    owe_users: List[User] = session.query(User).join(Expense).filter(Expense.id == e.id and User.id == Expense.owe_user_id).all()
    user_id_to_name = {}
    for user_detail in owe_users:
        user_id_to_name[user_detail.id] = user_detail.username
    owed_amounts = [exp.amount for exp in relevant_expenses]
    return ExpenseDetails(
        expense_id=e.id,
        paid_user_name=paid_user.username,
        total_paid=sum(owed_amounts),
        details=[
            OweUserDetailWithName(
                owe_user_name=user_id_to_name[exp.owe_user_id],
                amount=exp.amount,
            ) for exp in relevant_expenses
        ]
    )

def load_expenses_for_trip_id(session, trip_id: int) -> List[ExpenseDetails]:
    """
        Load expenses for a given trip_id and return a list of ExpenseDetails objects.

        This function queries the database to retrieve all ExpenseMeta objects that are associated with the given trip_id. It then converts each ExpenseMeta object into an ExpenseDetails object by calling the convert_expense() function. The resulting ExpenseDetails objects are then returned as a list.

        Args:
        - session: A SQLAlchemy session object that connects to a database.
        - trip_id: An integer representing the trip_id for which expenses should be retrieved.

        Returns:
        - A list of ExpenseDetails objects representing the expenses for the given trip_id.

        Raises:
        SQLAlchemyError: If an error occurs while querying the database.

        Example:
        trip_id = 1
        expenses = load_expenses_for_trip_id(session, trip_id)
        print(expenses)
    """
    expenses_meta = session.query(ExpenseMeta).filter(ExpenseMeta.trip_id == trip_id).all()
    return [
        convert_expense(exp_meta) for exp_meta in expenses_meta
    ]

def calculate_summary_for_trip_id(session, trip_id: int) -> Dict[str, Dict[str, int]]:
    """
        Calculate the summary for a given trip_id and return it as a dictionary.

        This function calculates a summary of the expenses for the given trip_id by generating a matrix BALANCES[UserNameA][UserNameB], where each cell UserNameA, UserNameB represents how much UserNameB owes to the user UserNameA. The resulting balances are returned as a dictionary.

        Args:
        - session: A SQLAlchemy session object that connects to a database.
        - trip_id: An integer representing the trip_id for which the summary should be calculated.

        Returns:
        - A dictionary where each key represents a user name and the value is another dictionary where each key represents another user name and the value represents the amount owed from the second user to the first user.

        Raises:
        SQLAlchemyError: If an error occurs while querying the database.

        Example:
        trip_id = 1
        summary = calculate_summary_for_trip_id(session, trip_id)
    """
    expenses = load_expenses_for_trip_id(session, trip_id)
    balances = {}
    for expense in expenses:
        paid_name = expense.paid_user_name
        if paid_name not in balances:
            balances[paid_name] = {}
        for detail in expense.details:
            if detail.owe_user_name not in balances[paid_name]:
                balances[paid_name][detail.owe_user_name] = 0
            balances[paid_name][detail.owe_user_name] += detail.amount
    return balances

def load_expenses_with_summary_for_trip(session, trip_id: int):
    """
        Loads expenses and their summary for a given trip_id and returns it as a GetExpenses object.

        Args:
        - session: A SQLAlchemy session object that connects to a database.
        - trip_id: An integer representing the trip_id for which the expenses should be loaded.

        Returns:
        - A GetExpenses object containing a list of expenses loaded by calling load_expenses_for_trip_id and a summary of expenses loaded by calling calculate_summary_for_trip_id.

        Raises:
        - SQLAlchemyError: If an error occurs while querying the database.

        Example:
        trip_id = 1
        get_expenses = load_expenses_with_summary_for_trip(session, trip_id)
    """
    return GetExpenses(
        expenses=load_expenses_for_trip_id(session, trip_id),
        summary=calculate_summary_for_trip_id(session, trip_id),
    )