# test_controller_v2.py
import unittest
from unittest.mock import Mock
from controller import ControllerV2
from dbmodel import IDataRepository
from ollamamodel import IAIAdvisor
from dbmodel import SecurityData


class TestControllerV2(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock(spec=IDataRepository)
        self.mock_ai = Mock(spec=IAIAdvisor)
        self.controller = ControllerV2('Medium', db_repo=self.mock_db, ai_advisor=self.mock_ai)

    def test_get_available_securities(self):
        self.mock_db.get_available_securities.return_value = ['Security1', 'Security2']
        result = self.controller.get_available_securities()
        self.assertEqual(result, ['Security1', 'Security2'])
        self.mock_db.get_available_securities.assert_called_once()

    def test_buy_success(self):
        self.mock_db.get_portfolio_data.return_value = []
        self.controller.portfolio.calculate_total_risk = Mock(return_value=1.0)
        self.controller.portfolio.calculate_projected_risk_with_new_security = Mock(return_value=3.0)
        self.mock_db.insert_or_update.return_value = None

        success, msg = self.controller.buy('StockA', 'Tech', 'Medium', 'stock', 'regular', 10, 100.0)
        self.assertTrue(success)
        self.assertIn('bought successfully', msg)

    def test_buy_fail_due_to_risk(self):
        self.controller.portfolio.calculate_total_risk = Mock(return_value=4.0)
        self.controller.portfolio.calculate_projected_risk_with_new_security = Mock(return_value=5.0)

        success, msg = self.controller.buy('StockB', 'Finance', 'High', 'stock', 'growth', 5, 200.0)
        self.assertFalse(success)
        self.assertIn('exceeds acceptable range', msg)

    def test_sell_success(self):
        self.mock_db.get_portfolio_data.return_value = [
            SecurityData(1, 'StockA', 100.0, 20, 'Tech', 'Medium', 'stock', 'regular')
        ]
        self.mock_db.sell.return_value = None

        success, msg = self.controller.sell('StockA', 'stock', 'Tech', 'regular', 10)
        self.assertTrue(success)
        self.assertIn('sold successfully', msg)

    def test_sell_fail_not_found(self):
        self.mock_db.get_portfolio_data.return_value = []

        success, msg = self.controller.sell('StockX', 'stock', 'Tech', 'regular', 5)
        self.assertFalse(success)
        self.assertIn('not found', msg)

    def test_get_portfolio_data(self):
        self.mock_db.get_portfolio_data.return_value = ['StockA', 'BondB']
        result = self.controller.get_portfolio_data()
        self.assertEqual(result, ['StockA', 'BondB'])

    def test_get_total_risk(self):
        self.controller.portfolio.calculate_total_risk = Mock(return_value=3.2)
        risk = self.controller.get_total_risk()
        self.assertEqual(risk, 3.2)

    def test_calculate_projected_risk(self):
        self.controller.portfolio.calculate_total_risk = Mock(return_value=2.0)
        self.mock_db.get_portfolio_data.return_value = [
            SecurityData(1, 'StockA', 100.0, 50, 'Tech', 'Medium', 'stock', 'regular')
        ]
        projected_risk = self.controller.calculate_projected_risk('StockC', 'Tech', 'Low', 'stock', 'regular', 20)
        self.assertIsInstance(projected_risk, float)

    def test_get_advice(self):
        self.mock_ai.get_advice.return_value = "Diversify your investments."
        advice = self.controller.get_advice('What should I invest in?')
        self.assertEqual(advice, "Diversify your investments.")
        self.mock_ai.get_advice.assert_called_once_with('What should I invest in?')

    def test_get_individual_risk(self):
        mock_security = Mock(security_type='stock', name='StockD', sector='Tech', variance='High', subtype='growth')
        risk = self.controller.get_individual_risk(mock_security)
        self.assertIsInstance(risk, (int, float))

if __name__ == '__main__':
    unittest.main()
