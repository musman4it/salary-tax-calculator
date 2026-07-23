"""
Unit tests for tax_calculator module
"""
import pytest
from tax_calculator import calculate_pakistan_tax


class TestCalculatePakistanTax:
    """Test cases for calculate_pakistan_tax function"""

    def test_calculate_tax_returns_dict(self):
        """Test that calculate_pakistan_tax returns a dictionary"""
        result = calculate_pakistan_tax(100000)
        assert isinstance(result, dict)

    def test_calculate_tax_has_required_keys(self):
        """Test that result has all required keys"""
        result = calculate_pakistan_tax(100000)
        required_keys = {
            'annual_gross', 'monthly_gross', 'annual_tax', 
            'monthly_tax', 'annual_net', 'monthly_net', 'surcharge_applied'
        }
        assert all(key in result for key in required_keys)

    def test_calculate_tax_non_negative(self):
        """Test that tax calculation returns non-negative values"""
        result = calculate_pakistan_tax(100000)
        assert result['annual_tax'] >= 0
        assert result['monthly_tax'] >= 0
        assert result['annual_net'] >= 0
        assert result['monthly_net'] >= 0

    def test_calculate_tax_zero_salary(self):
        """Test calculate_pakistan_tax with zero salary"""
        result = calculate_pakistan_tax(0)
        assert result['annual_tax'] == 0
        assert result['monthly_tax'] == 0

    def test_calculate_tax_below_threshold(self):
        """Test calculate_pakistan_tax with income below tax threshold"""
        result = calculate_pakistan_tax(50000, mode="annual")
        assert result['annual_tax'] == 0

    def test_calculate_tax_low_slab(self):
        """Test calculate_pakistan_tax in first tax slab"""
        result = calculate_pakistan_tax(700000, mode="annual")
        assert result['annual_tax'] > 0
        assert isinstance(result['annual_tax'], (int, float))

    def test_calculate_tax_monthly_mode(self):
        """Test calculate_pakistan_tax with monthly mode"""
        monthly_result = calculate_pakistan_tax(50000, mode="monthly")
        annual_result = calculate_pakistan_tax(600000, mode="annual")
        
        assert abs(monthly_result['annual_gross'] - annual_result['annual_gross']) < 0.01

    def test_calculate_tax_high_income_surcharge(self):
        """Test surcharge calculation for high income"""
        result = calculate_pakistan_tax(1000000, mode="annual")
        # Income over 10M should have surcharge
        assert isinstance(result['surcharge_applied'], bool)

    def test_calculate_tax_valid_returns(self):
        """Test that all returned values are numeric"""
        result = calculate_pakistan_tax(500000)
        assert isinstance(result['annual_gross'], (int, float))
        assert isinstance(result['monthly_gross'], (int, float))
        assert isinstance(result['annual_tax'], (int, float))
        assert isinstance(result['monthly_tax'], (int, float))
        assert isinstance(result['annual_net'], (int, float))
        assert isinstance(result['monthly_net'], (int, float))

    def test_calculate_tax_net_equals_gross_minus_tax(self):
        """Test that net salary equals gross minus tax"""
        result = calculate_pakistan_tax(1000000, mode="annual")
        expected_net = result['annual_gross'] - result['annual_tax']
        assert abs(result['annual_net'] - expected_net) < 0.01
