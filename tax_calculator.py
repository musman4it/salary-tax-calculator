def calculate_pakistan_tax(income, mode="monthly"):
    # Convert monthly input to annual for slab processing
    if mode == "monthly":
        annual_income = income * 12
    else:
        annual_income = income

    fixed_tax = 0
    percentage = 0
    excess_base = 0

    # Apply FBR Progressive Tax Slabs
    if annual_income <= 600000:
        fixed_tax, percentage, excess_base = 0, 0, 0
    elif annual_income <= 1200000:
        fixed_tax, percentage, excess_base = 0, 0.01, 600000
    elif annual_income <= 2200000:
        fixed_tax, percentage, excess_base = 6000, 0.11, 1200000
    elif annual_income <= 3200000:
        fixed_tax, percentage, excess_base = 116000, 0.23, 2200000
    elif annual_income <= 4100000:
        fixed_tax, percentage, excess_base = 346000, 0.30, 3200000
    else:
        fixed_tax, percentage, excess_base = 616000, 0.35, 4100000

    # Calculate Base Tax
    base_tax = fixed_tax + ((annual_income - excess_base) * percentage)

    # Apply 9% Surcharge on Tax Liability for Income exceeding 10 Million PKR
    surcharge = 0
    if annual_income > 10000000:
        surcharge = base_tax * 0.09

    total_annual_tax = base_tax + surcharge
    total_monthly_tax = total_annual_tax / 12

    net_annual_salary = annual_income - total_annual_tax
    net_monthly_salary = (annual_income / 12) - total_monthly_tax

    return {
        "annual_gross": annual_income,
        "monthly_gross": annual_income / 12,
        "annual_tax": total_annual_tax,
        "monthly_tax": total_monthly_tax,
        "annual_net": net_annual_salary,
        "monthly_net": net_monthly_salary,
        "surcharge_applied": surcharge > 0
    }

# Quick testing interface
if __name__ == "__main__":
    print("--- Pakistan Salary Tax Calculator ---")
    salary_input = float(input("Enter Salary Amount (PKR): "))
    salary_mode = input("Is this 'monthly' or 'annual'? ").strip().lower()

    result = calculate_pakistan_tax(salary_input, salary_mode)

    print("\n================ RESULTS ================")
    print(f"Gross Annual Income:  PKR {result['annual_gross']:,.2f}")
    print(f"Gross Monthly Income: PKR {result['monthly_gross']:,.2f}")
    print("-----------------------------------------")
    print(f"Total Annual Tax:     PKR {result['annual_tax']:,.2f}")
    print(f"Total Monthly Tax:    PKR {result['monthly_tax']:,.2f}")
    print("-----------------------------------------")
    print(f"Net Annual Take-Home: PKR {result['annual_net']:,.2f}")
    print(f"Net Monthly Take-Home:PKR {result['monthly_net']:,.2f}")
    if result['surcharge_applied']:
        print("Note: Includes a 9% high-earner surcharge on total tax liability.")
    print("=========================================\n")
