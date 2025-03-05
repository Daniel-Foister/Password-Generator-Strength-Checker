import secrets
import string
import re
import os

# Load common passwords list
def load_common_passwords(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Password list file not found at {filepath}")
        return set()
    
    with open(filepath, 'r', encoding='utf-8') as file:
        return {line.strip().lower() for line in file}

PASSWORD_FILE = "10000passwords.txt"  # Update the path if needed
COMMON_PASSWORDS = load_common_passwords(PASSWORD_FILE)

# Password Strength Checker
def check_password_strength(password):
    strength_score = 0
    feedback = []

    # Check if password is in common list
    password_lower = password.lower()
    if password_lower in COMMON_PASSWORDS:
        return (
            "Very Weak Password ❌",
            [f"Your password '{password}' is too common! Choose something unique."]
        )

    # Length check
    if len(password) >= 16:
        strength_score += 3
    elif len(password) >= 12:
        strength_score += 2
    elif len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("Password is too short (minimum 8 characters).")

    # Uppercase and lowercase check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        strength_score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    # Number check
    if re.search(r"\d", password):
        strength_score += 1
    else:
        feedback.append("Add at least one number.")

    # Special character check
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        strength_score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    # Check for repetitive or sequential characters
    if re.search(r"(.)\1{2,}", password):  
        feedback.append("Avoid repetitive characters (e.g., 'aaa' or '111').")
    if re.search(r"1234|abcd|qwerty|asdf", password, re.IGNORECASE):
        feedback.append("Avoid common sequences (e.g., '1234', 'abcd', 'qwerty').")

    # Evaluate strength
    if strength_score >= 6:
        return "Very Strong Password 💪", []
    elif strength_score >= 4:
        return "Strong Password ✅", feedback
    elif strength_score >= 2:
        return "Moderate Password ⚠️", feedback
    else:
        return "Weak Password ❌", feedback

# Password Generator
def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special_chars=True):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_numbers else ""
    special = string.punctuation if use_special_chars else ""

    if not (lower or upper or digits or special):
        return "Error: No character set selected!"

    # At least one of each selected character type
    password_chars = []
    if use_uppercase:
        password_chars.append(secrets.choice(upper))
    if use_numbers:
        password_chars.append(secrets.choice(digits))
    if use_special_chars:
        password_chars.append(secrets.choice(special))

    # Fill the rest randomly
    all_chars = lower + upper + digits + special
    password_chars.extend(secrets.choice(all_chars) for _ in range(length - len(password_chars)))

    # Shuffle to prevent predictable structure
    secrets.SystemRandom().shuffle(password_chars)

    return ''.join(password_chars)

# Yes/No input
def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        elif user_input == "":
            print("You must enter 'y' or 'n'. Please try again.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

# Main menu loop
def main():
    while True:
        print("\n===================================")
        print("Password Utility Menu")
        print("1 - Generate a Secure Password")
        print("2 - Check Password Strength")
        print("0 - Exit")
        print("===================================")

        choice = input("Enter your choice: ").strip()
        
        if choice == '1':  # Password Generator
            print("\nCustomize Your Password:")
            
            while True:
                try:
                    length = int(input("Enter password length (minimum 8): "))
                    if length < 8:
                        print("Password must be at least 8 characters long.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

            use_upper = get_yes_no_input("Include uppercase letters? (y/n): ")
            use_numbers = get_yes_no_input("Include numbers? (y/n): ")
            use_special = get_yes_no_input("Include special characters? (y/n): ")

            password = generate_password(length, use_upper, use_numbers, use_special)
            print(f"\nGenerated Secure Password: {password}")

        elif choice == '2':  # Password Strength Checker
            password = input("\nEnter a password to check: ")
            strength, suggestions = check_password_strength(password)

            print(f"\nPassword Strength: {strength}")
            if suggestions:
                print("Suggestions to improve:")
                for suggestion in suggestions:
                    print(f"- {suggestion}")

        elif choice == '0':  # Exit
            print("\nGoodbye! Stay secure!")
            break

        else:
            print("\nInvalid choice! Please enter 1, 2, or 0.")

# Run the program
if __name__ == "__main__":
    main()
