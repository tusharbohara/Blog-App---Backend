from rest_framework.response import Response
from rest_framework import status


def userValidation(error, response_status):
    """User login and registration validations"""
    msg = error
    if error.__contains__("non_field_errors"):
        deActiveMsg = "Your account has been temporarily deactivated."
        if error["non_field_errors"][0] == deActiveMsg:
            msg = deActiveMsg
        else:
            msg = "Invalid username or password."
    elif error.__contains__("full_name") and error.__contains__(
            "email") and error.__contains__("password"):
        emailExist = "user with this email already exists."
        passwordErr = "Ensure this field has at least 8 characters."
        if error["email"][0] == emailExist:
            msg = "Email already exists. Please enter a unique email. Full Name and Password field should not be empty."
        elif error["email"][0] == emailExist and error["password"][0] == passwordErr:
            msg = "Email already exists. Please enter a unique email. Full Name and Password must contain minimum 8 characters."
        else:
            msg = "Full Name, Email and Password field should not be empty."
    elif error.__contains__("full_name") and error.__contains__("password"):
        passwordErr = "Ensure this field has at least 8 characters."
        if error["password"][0] == passwordErr:
            msg = "Password must contain minimum 8 characters and full name field should not empty."
        else:
            msg = "Full Name, Password field should not be empty."
    elif error.__contains__("full_name") and error.__contains__("email"):
        emailExist = "user with this email already exists."
        if error["email"][0] == emailExist:
            msg = "Email already exists. Please enter a unique email and full name field should not be empty."
        else:
            msg = "Full Name, Email field should not be empty."
    elif error.__contains__("email") and error.__contains__("password"):
        emailExist = "user with this email already exists."
        passwordErr = "Ensure this field has at least 8 characters."
        if error["email"][0] == emailExist:
            msg = "Email already exists. Please enter a unique email and password field should not be empty."
        elif error["password"][0] == passwordErr and error["email"][0] == emailExist:
            msg = "Password must contain minimum 8 characters and email field should not empty."
        else:
            msg = "Email and password field should not be empty."
    elif error.__contains__("email"):
        emailExist = "user with this email already exists."
        if error["email"][0] == emailExist:
            msg = "Email already exists. Please enter a unique email."
        else:
            msg = "Email field should not be empty."
    elif error.__contains__("password"):
        passwordErr = "Ensure this field has at least 8 characters."
        if error["password"][0] == passwordErr:
            msg = "Password field must contain minimum 8 characters"
        else:
            msg = "Password field should not be empty."
    elif error.__contains__("full_name"):
        msg = "Fullname field should not be empty."
    else:
        msg = error
    return Response({
        "msg": msg,
        "response_status": response_status,
        "status_code": status.HTTP_406_NOT_ACCEPTABLE
    })
