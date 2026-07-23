"""
Unit tests for tax_calculator module
"""
import pytest
from tax_calculator import calculate_tax, TaxCalculator


class TestCalculateTax:
    """Test cases for calculate_tax function"""

    def test_calculate_tax_returns_number(self):
        """Test that calculate_tax returns a numeric value"""
        result = calculate_tax(100000)
        assert isinstance(result, (int, float))

    def test_calculate_tax_non_negative(self):
        """Test that tax calculation returns non-negative values"""
        result = calculate_tax(100000)
        assert result >= 0

    def test_calculate_tax_zero_salary(self):
        """Test calculate_tax with zero salary"""
        result = calculate_tax(0)
        assert result == 0

    def test_calculate_tax_low_income(self):
        """Test calculate_tax with low income below tax threshold"""
        # Assuming tax threshold exists - adjust based on actual rules
        result = calculate_tax(50000)
        assert isinstance(result, (int, float))


class TestTaxCalculator:
    """Test cases for TaxCalculator class"""

    def test_tax_calculator_initialization(self):
        """Test TaxCalculator can be instantiated"""
        calc = TaxCalculator()
        assert calc is not None

    def test_tax_calculator_has_calculate_method(self):
        """Test TaxCalculator has calculate method"""
        calc = TaxCalculator()
        assert hasattr(calc, 'calculate')
