import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

n = 500

data = {
    "Loan_ID": [f"LN{1000+i}" for i in range(n)],
    "Borrower_Name": [fake.name() for _ in range(n)],
    "Loan_Amount": np.random.randint(5000, 50000, n),
    "Interest_Rate": np.round(np.random.uniform(5.0, 20.0, n), 2),
    "Term_Months": np.random.choice([36, 48, 60], n),
    "Grade": np.random.choice(["A", "B", "C", "D", "E", "F"], n, p=[0.2,0.25,0.2,0.15,0.1,0.1]),
    "Employment_Length": np.random.choice(["<1 year", "1-2 years", "3-5 years", "6-10 years", "10+ years"], n),
    "Annual_Income": np.random.randint(30000, 150000, n),
    "Debt_to_Income": np.round(np.random.uniform(5, 40, n), 2),
    "Loan_Status": np.random.choice(["Fully Paid", "Charged Off", "Current"], n, p=[0.5,0.2,0.3]),
}

df = pd.DataFrame(data)

# Add some missing values for testing
for col in ["Interest_Rate", "Term_Months", "Grade", "Employment_Length", "Annual_Income"]:
    idx = random.sample(range(n), k=int(n*0.05))
    df.loc[idx, col] = None  # Use None instead of np.nan for better compatibility

df.to_csv("test_Y3wMUE5_7gLdaTN.csv", index=False)
print("✅ CSV file created successfully!")