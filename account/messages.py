SIGNUP_VALIDATION_ERROR = {
    'first_name': {
        "invalid": "Invalid First name. Only Alphabets are allowed.",
        "required": "First Name should contain at least one alphabet.",
    },
    'last_name': {
        "invalid": "Invalid last name. Only Alphabets are allowed.",
        "required": "Last Name should contain at least one alphabet.",
    },

    'password': {
        "invalid": "Password must contain at least one special character, one capital "
                   "letter, one small letter, and one number, with a length of at least 8 "
                   "and no spaces.",
    },
    'confirm_password': {
        "invalid": "Password and confirm password does not match!",
    },
    'email': {
        "exits": "Email already exists!"
    }

}

OTP_VALIDATION_ERROR = {
    "invalid": "Invalid OTP",
    "expired": "OTP expired",
}

VIEWS_MESSAGES = {
    'signup': {
        "success": "User created successfully and Otp is Sent to the Email",
        "invalid": "Invalid request body",
        "unauthorized": "Unauthorized access",
    },
    'otp_verification': {
        "verified": "OTP verified successfully and account activated!",
        "invalid": "Invalid request body",
        "unauthorized": "Unauthorized access",
    }
}

