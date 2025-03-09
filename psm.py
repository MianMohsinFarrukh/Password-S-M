import re
import streamlit as st

# Streamlit UI
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="\U0001F510",  # You can use an emoji or a URL to an image for the favicon
    layout="centered"
)

def password_strength(password):
    """Evaluate the strength of a password."""
    strength = 0
    feedback = []
    max_length = 10  # Set the maximum password length

    if len(password) > max_length:
        feedback.append(f"Password should not exceed {max_length} characters.")
        return "Invalid", feedback, {}

    rules = {
        "length": len(password) >= 8,  # Ensure minimum length is 8 characters
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    # If length is not valid, force strength to "Weak"
    if not rules["length"]:
        feedback.append("Password should be at least 8 characters long.")
        return "Weak", feedback, rules

    # Calculate strength based on rules
    for rule, passed in rules.items():
        if passed:
            strength += 1
        else:
            if rule == "uppercase":
                feedback.append("Add at least one uppercase letter.")
            elif rule == "lowercase":
                feedback.append("Add at least one lowercase letter.")
            elif rule == "digit":
                feedback.append("Add at least one digit.")
            elif rule == "special":
                feedback.append("Add at least one special character.")

    # Assign strength levels
    if strength <= 2:
        level = "Weak"
    elif strength == 3:
        level = "Moderate"
    elif strength >= 4:
        level = "Strong"

    return level, feedback, rules

# Title and Description
st.title("\U0001F510 Password Strength Meter")
st.markdown(
    """
    **Check your password strength and get suggestions to improve it!**  
    Your password's security matters. Follow the guidelines below for a strong password.
    """
)

# Sidebar for Tips
st.sidebar.title("💡 Tips for a Strong Password")
st.sidebar.markdown(
    """
    - Use at least 8 characters.
    - Include both uppercase and lowercase letters.
    - Add at least one digit.
    - Use special characters like !, @, #, $, etc.
    - Avoid using easily guessable information like your name or birthdate.
    - Regularly update your passwords.
    """
)

# Password Input
password = st.text_input("Enter your Password:", type="password", help="Type your password to check its strength.")
check_password = st.button("Check Password")

if check_password and password:
    # Evaluate password strength after clicking the button
    level, feedback, rules = password_strength(password)

    if level == "Invalid":
        st.error("Your password is invalid:")
        for suggestion in feedback:
            st.write(f"- {suggestion}")
    else:
        # Color-coded progress bar
        strength_levels = {"Weak": (33, "red"), "Moderate": (66, "yellow"), "Strong": (100, "green")}
        strength_percent, color = strength_levels[level]

        st.markdown(
            f"""
            <style>
            .stProgress > div > div > div > div {{
                background-color: {color};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.progress(strength_percent)

        # Display password strength level
        st.subheader(f"Password Strength: **{level}**")

        # Show password validation criteria
        st.markdown("### Validation Rules:")
        st.write("✅ **Passed** | ❌ **Not Met**")
        st.markdown(
            f"""
            - {"✅" if rules["length"] else "❌"} Minimum 8 characters  
            - {"✅" if rules["uppercase"] else "❌"} At least one uppercase letter  
            - {"✅" if rules["lowercase"] else "❌"} At least one lowercase letter  
            - {"✅" if rules["digit"] else "❌"} At least one digit  
            - {"✅" if rules["special"] else "❌"} At least one special character  
            """
        )

        # Feedback for improvement
        if feedback:
            st.warning("### Suggestions to improve your password:")
            for suggestion in feedback:
                st.write(f"- {suggestion}")
        else:
            st.success("Your password is strong! \U0001F389")

else:
    if not password:
        st.info("Please enter a password to check its strength.")
    elif not check_password:
        st.info("Click the 'Check Password' button to evaluate your password.")

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ to empower you in creating strong, secure passwords and safeguarding your online world!"
)
