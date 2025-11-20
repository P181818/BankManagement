import yyyyy as st
from pathlib import Path
import json
import random
import string
import os

# -------------------------- CONFIG --------------------------
st.set_page_config(page_title="MyBank", page_icon="🏦", layout="centered")
DATA_FILE = "DataBase.json"

# -------------------------- DATA HANDLING --------------------------
def load_data():
    if Path(DATA_FILE).exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

bank_data = load_data()

# -------------------------- HELPER FUNCTIONS --------------------------
def generate_account_no():
    alpha = random.choices(string.ascii_letters, k=5)
    digits = random.choices(string.digits, k=4)
    id_list = alpha + digits
    random.shuffle(id_list)
    return "".join(id_list)

def find_account(acc_no, pin):
    for acc in bank_data:
        if acc["Account No."] == acc_no and str(acc["Pin"]) == str(pin):
            return acc
    return None

# -------------------------- STREAMLIT APP --------------------------
st.title("🏦 MyBank - Simple Banking System")
st.markdown("Secure • Fast • Easy")

menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "Create Account", "Deposit Money", "Withdraw Money", "Check Balance & Details", "Update Details", "Delete Account"]
)

# ============================= HOME =============================
if menu == "Home":
    st.image("https://source.unsplash.com/random/800x400/?bank", use_column_width=True)
    st.markdown("""
    Welcome to **MyBank** – A simple and secure banking system built with ❤️ using Python and Streamlit.
    
    Features:
    - Create new account
    - Deposit & Withdraw money (max ₹10,000 per transaction)
    - View balance & details
    - Update personal information
    - Delete account when needed
    """)
    st.info(f"Total registered accounts: {len(bank_data)}")

# ============================= CREATE ACCOUNT =============================
elif menu == "Create Account":
    st.subheader("Create New Bank Account")
    
    with st.form("create_account_form"):
        name = st.text_input("Full Name *")
        email = st.text_input("Email *")
        phone = st.text_input("Phone Number * (10 digits)")
        pin = st.text_input("Set 4-digit PIN *", type="password", max_chars=4)
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if not all([name, email, phone, pin]):
                st.error("All fields are required!")
            elif len(phone) != 10 or not phone.isdigit():
                st.error("Phone number must be exactly 10 digits.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email.")
            else:
                account_no = generate_account_no()
                new_acc = {
                    "Name": name.strip(),
                    "Email": email.strip(),
                    "Phone No.": phone,
                    "Pin": int(pin),
                    "Account No.": account_no,
                    "Balance": 0
                }
                bank_data.append(new_acc)
                save_data(bank_data)
                st.success(f"Account created successfully!")
                st.balloons()
                st.code(f"Your Account Number: {account_no}\nPlease save it securely!", language=None)
                st.info("Never share your PIN or Account Number with anyone.")

# ============================= DEPOSIT =============================
elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    
    with st.form("deposit_form"):
        acc_no = st.text_input("Account Number *")
        pin = st.text_input("PIN *", type="password", max_chars=4)
        amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=10000, step=100)
        
        deposit_btn = st.form_submit_button("Deposit")
        
        if deposit_btn:
            user = find_account(acc_no, pin)
            if not user:
                st.error("Invalid Account Number or PIN.")
            elif amount <= 0 or amount > 10000:
                st.error("Amount must be between ₹1 and ₹10,000.")
            else:
                user["Balance"] += amount
                save_data(bank_data)
                st.success(f"₹{amount} deposited successfully!")
                st.write(f"New Balance: ₹{user['Balance']}")

# ============================= WITHDRAW =============================
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    
    with st.form("withdraw_form"):
        acc_no = st.text_input("Account Number *")
        pin = st.text_input("PIN *", type="password", max_chars=4)
        amount = st.number_input("Amount to Withdraw (₹)", min_value=1, max_value=10000, step=100)
        
        withdraw_btn = st.form_submit_button("Withdraw")
        
        if withdraw_btn:
            user = find_account(acc_no, pin)
            if not user:
                st.error("Invalid Account Number or PIN.")
            elif amount > user["Balance"]:
                st.error(f"Insufficient balance! Available: ₹{user['Balance']}")
            elif amount > 10000:
                st.error("Maximum withdrawal limit is ₹10,000 per transaction.")
            else:
                user["Balance"] -= amount
                save_data(bank_data)
                st.success(f"₹{amount} withdrawn successfully!")
                st.write(f"Remaining Balance: ₹{user['Balance']}")

# ============================= CHECK DETAILS =============================
elif menu == "Check Balance & Details":
    st.subheader("Account Details & Balance")
    
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    
    if st.button("Show Details"):
        user = find_account(acc_no, pin)
        if not user:
            st.error("Account not found or wrong PIN.")
        else:
            st.success("Account verified!")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {user['Name']}")
                st.info(f"**Account No.:** {user['Account No.']}")
                st.info(f"**Email:** {user['Email']}")
            with col2:
                st.info(f"**Phone:** {user['Phone No.']}")
                st.info(f"**Balance:** ₹{user['Balance']}")

# ============================= UPDATE DETAILS =============================
elif menu == "Update Details":
    st.subheader("Update Account Details")
    
    acc_no = st.text_input("Account Number (to verify)")
    pin = st.text_input("Current PIN", type="password", max_chars=4)
    
    user = find_account(acc_no, pin) if acc_no and pin else None
    
    if user:
        st.success("Account verified! Now update your details (leave blank to keep current):")
        
        with st.form("update_form"):
            new_name = st.text_input("New Name", value=user["Name"])
            new_email = st.text_input("New Email", value=user["Email"])
            new_phone = st.text_input("New Phone (10 digits)", value=user["Phone No."])
            new_pin = st.text_input("New PIN (4 digits)", type="password", max_chars=4, value="")
            change_pin = st.checkbox("Change PIN")
            
            if not change_pin:
                new_pin = str(user["Pin"])
            
            update_btn = st.form_submit_button("Update Details")
            
            if update_btn:
                if new_phone and (len(new_phone) != 10 or not new_phone.isdigit()):
                    st.error("Phone must be 10 digits.")
                elif change_pin and (len(new_pin) != 4 or not new_pin.isdigit()):
                    st.error("New PIN must be 4 digits.")
                else:
                    user["Name"] = new_name if new_name else user["Name"]
                    user["Email"] = new_email if new_email else user["Email"]
                    user["Phone No."] = new_phone if new_phone else user["Phone No."]
                    if change_pin and new_pin:
                        user["Pin"] = int(new_pin)
                    
                    save_data(bank_data)
                    st.success("Details updated successfully!")
                    st.balloons()
    else:
        if acc_no and pin:
            st.error("Invalid credentials.")

# ============================= DELETE ACCOUNT =============================
elif menu == "Delete Account":
    st.subheader("Delete Account (Permanent Action)")
    st.warning("This action cannot be undone!")
    
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will delete my account permanently")
    
    if st.button("Delete Account") and confirm:
        user = find_account(acc_no, pin)
        if not user:
            st.error("Invalid Account Number or PIN.")
        else:
            bank_data.remove(user)
            save_data(bank_data)
            st.error("Account deleted permanently.")
            st.info("Thank you for banking with us.")

# ============================= FOOTER =============================
st.markdown("---")
st.caption("MyBank App © 2025 | Built with Streamlit")