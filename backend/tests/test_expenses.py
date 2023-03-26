import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_base import Base, User
from models.expenses import (
    ExpenseMeta,
    ExpenseDetails,
    GetExpenses,
    CreateExpenseRequest,
    OweUserDetail,
    create_expenses,
    convert_expense,
    load_expenses_for_trip_id,
    calculate_summary_for_trip_id,
    load_expenses_with_summary_for_trip,
)
from core.db import *

class TestExpenseFunctions(unittest.TestCase):

    def setUp(self):
        self.session = get_db(is_test=True)

        user1 = User(id=1, username="Alice")
        user2 = User(id=2, username="Bob")
        user3 = User(id=3, username="Charlie")

        self.session.add_all([user1, user2, user3])
        self.session.commit()

    def test_create_expenses(self):
        request = CreateExpenseRequest(trip_id=1, description="Dinner", paid_user_id=1)
        detail1 = OweUserDetail(owe_user_id=2, amount=2000)
        detail2 = OweUserDetail(owe_user_id=3, amount=3000)
        request.details = [detail1, detail2]

        response = create_expenses(self.session, request)
        self.assertIsNotNone(response.expense_id)
        self.assertIsInstance(response.expense_id, int)

    def test_convert_expense(self):
        expense_meta = ExpenseMeta(id=1, trip_id=1, paid_user_id=1, description="Dinner")
        self.session.add(expense_meta)
        self.session.commit()

        expense_details = convert_expense(self.session, expense_meta)
        self.assertIsInstance(expense_details, ExpenseDetails)
        self.assertEqual(expense_details.expense_id, 1)

    def test_load_expenses_for_trip_id(self):
        trip_id = 1
        expenses = load_expenses_for_trip_id(self.session, trip_id)
        self.assertIsInstance(expenses, list)

    def test_calculate_summary_for_trip_id(self):
        trip_id = 1
        summary = calculate_summary_for_trip_id(self.session, trip_id)
        self.assertIsInstance(summary, dict)

    def test_load_expenses_with_summary_for_trip(self):
        trip_id = 1
        get_expenses = load_expenses_with_summary_for_trip(self.session, trip_id)
        self.assertIsInstance(get_expenses, GetExpenses)

if __name__ == "__main__":
    unittest.main()
