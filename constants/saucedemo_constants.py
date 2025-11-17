from enum import Enum


class HeaderTexts(Enum):
    MainText = "Swag Labs"


class SauceDemoErrors(Enum):
    LockedOutUser = "Epic sadface: Sorry, this user has been locked out."
    UsernamePasswordDoNotMatch = "Epic sadface: Username and password do not match any user in this service"
