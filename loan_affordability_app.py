import streamlit as st

st.set_page_config(page_title="Loan Affordability Calculator", page_icon="💳", layout="centered")

# ---------------------------------
# Calculator function
# ---------------------------------
def calculate_loan_affordability(monthly_income, monthly_expenses, existing_loan_payments,
                                 loan_amount, interest_rate_annual, loan_term_months):

    monthly_rate = interest_rate_annual / 12 / 100

    if monthly_rate == 0:
        monthly_payment = loan_amount / loan_term_months
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_term_months) / \
                         ((1 + monthly_rate) ** loan_term_months - 1)

    debt_to_income_ratio = ((existing_loan_payments + monthly_payment) / monthly_income) if monthly_income > 0 else 1
    disposable_income = monthly_income - monthly_expenses - existing_loan_payments - monthly_payment

    if debt_to_income_ratio <= 0.25:
        affordability = "Comfortable"
        interpretation = "The loan appears affordable based on the current income and debt profile."
    elif debt_to_income_ratio <= 0.40:
        affordability = "Moderate Risk"
        interpretation = "The loan may be manageable, but affordability should be reviewed carefully."
    elif debt_to_income_ratio <= 0.55:
        affordability = "High Risk"
        interpretation = "The debt burden appears elevated. Additional caution is recommended."
    else:
        affordability = "Not Affordable"
        interpretation = "The loan may place significant pressure on cash flow and repayment ability."

    return {
        "monthly_payment": round(monthly_payment, 2),
        "debt_to_income_ratio": round(debt_to_income_ratio * 100, 2),
        "disposable_income_after_loan": round(disposable_income, 2),
        "affordability": affordability,
        "interpretation": interpretation
    }

# ---------------------------------
# UI
# ---------------------------------
st.title("Loan Affordability Calculator")
st.write(
    "Estimate monthly repayment, debt burden, and affordability using income, expense, and borrowing details."
)

with st.form("loan_affordability_form"):
    monthly_income = st.number_input("Monthly Income", min_value=0.0, step=1000.0)
    monthly_expenses = st.number_input("Monthly Expenses", min_value=0.0, step=1000.0)
    existing_loan_payments = st.number_input("Existing Loan Payments", min_value=0.0, step=1000.0)
    loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
    interest_rate_annual = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.5)
    loan_term_months = st.number_input("Loan Term (Months)", min_value=1, step=1)

    submitted = st.form_submit_button("Calculate Affordability")

if submitted:
    if monthly_income <= 0:
        st.error("Monthly income must be greater than zero.")
    else:
        result = calculate_loan_affordability(
            monthly_income, monthly_expenses, existing_loan_payments,
            loan_amount, interest_rate_annual, loan_term_months
        )

        st.success("Calculation Complete")
        st.metric("Estimated Monthly Payment", f"₦{result['monthly_payment']:,.2f}")
        st.metric("Debt-to-Income Ratio", f"{result['debt_to_income_ratio']}%")
        st.metric("Affordability", result['affordability'])

        st.write(f"**Interpretation:** {result['interpretation']}")
        st.write(f"**Estimated Disposable Income After Loan Payment:** ₦{result['disposable_income_after_loan']:,.2f}")

        st.info(
            "This tool provides an indicative affordability estimate only. "
            "For a deeper lending review, dashboard, or credit policy support, contact Quant Vision Labs."
        )

        st.markdown("### Need a More Detailed Review?")
        st.markdown("[Request Consultation](https://yourwebsite.com/request-consultation)")
