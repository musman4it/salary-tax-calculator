import sys

TAX_SLABS = [
    (600_000, 0.00, 0),
    (1_200_000, 0.01, 6_000),
    (2_200_000, 0.11, 116_000),
    (3_200_000, 0.23, 346_000),
    (4_100_000, 0.30, 616_000),
]

HIGHEST_RATE = 0.35
HIGHEST_THRESHOLD = 4_100_000
HIGHEST_FIXED = 616_000

SURCHARGE_THRESHOLD = 10_000_000
SURCHARGE_RATE = 0.09


def calculate_tax(annual_income):
    if annual_income <= 600_000:
        return 0

    tax = 0
    previous_threshold = 0

    for threshold, rate, _ in TAX_SLABS:
        if annual_income > previous_threshold:
            taxable_in_slab = min(annual_income, threshold) - previous_threshold
            if taxable_in_slab > 0:
                tax += taxable_in_slab * rate
        previous_threshold = threshold

    if annual_income > HIGHEST_THRESHOLD:
        tax += (annual_income - HIGHEST_THRESHOLD) * HIGHEST_RATE

    if annual_income > SURCHARGE_THRESHOLD:
        tax += tax * SURCHARGE_RATE

    return round(tax, 2)


def format_currency(amount):
    return f"Rs. {amount:,.2f}"


def show_breakdown(label, gross_annual, tax_annual):
    gross_monthly = gross_annual / 12
    tax_monthly = tax_annual / 12
    net_annual = gross_annual - tax_annual
    net_monthly = net_annual / 12

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  {'Item':<30} {'Monthly':>14} {'Annually':>14}")
    print(f"  {'-'*58}")
    print(f"  {'Gross Income':<30} {format_currency(gross_monthly):>14} {format_currency(gross_annual):>14}")
    print(f"  {'Tax Deducted':<30} {format_currency(tax_monthly):>14} {format_currency(tax_annual):>14}")
    print(f"  {'Net Take-Home':<30} {format_currency(net_monthly):>14} {format_currency(net_annual):>14}")
    print(f"{'='*60}\n")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Amount cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_period_input():
    while True:
        period = input("Is this amount monthly or annually? (M/A): ").strip().lower()
        if period in ('m', 'monthly'):
            return 'monthly'
        if period in ('a', 'annually', 'annual'):
            return 'annually'
        print("Invalid choice. Enter 'M' for monthly or 'A' for annually.")


def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ('y', 'yes'):
            return True
        if choice in ('n', 'no'):
            return False
        print("Please enter 'Y' or 'N'.")


def main():
    print("\n" + "=" * 60)
    print("  Pakistan Salary Tax Calculator (FBR Slabs)")
    print("  Based on Finance Act 2024/2025 — Salaried Individuals")
    print("=" * 60)

    while True:
        print("\n--- New Calculation ---")

        amount = get_float_input("Enter salary amount: ")
        period = get_period_input()

        annual_income = amount if period == 'annually' else amount * 12

        tax = calculate_tax(annual_income)

        show_breakdown("Tax Breakdown", annual_income, tax)

        if not get_yes_no("\nCalculate another? (Y/N): "):
            break

    print("Goodbye!\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
