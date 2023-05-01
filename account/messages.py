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

"""
accounts messages file
"""

SUCCESS_CODE = {
    '2000': 'OTP Generate success.'
}

ERROR_CODE = {
    '4000': 'ERROR.',
    '4001': "Invalid OTP",
    '4002': "User with this email does not exist.",
    '4003': "User is In_Active",
    '4004': "Email is required",
    '4005': "Invalid email",
    '4006': "Password is required",
    '4007': "Invalid password",
    '4008': "A password is required to log in.",
    '4009': "An email address is required to log in.",
    '4010': "An ",
}
