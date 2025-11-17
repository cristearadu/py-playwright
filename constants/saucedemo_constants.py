from enum import Enum


class HeaderTexts(Enum):
    MainText = "Swag Labs"


class SauceDemoErrors(Enum):
    LockedOutUser = "Epic sadface: Sorry, this user has been locked out."
    UsernamePasswordDoNotMatch = "Epic sadface: Username and password do not match any user in this service"
    PasswordRequired = "Epic sadface: Password is required"
    UsernameRequired = "Epic sadface: Username is required"


class ColorSchemes(Enum):
    LoginButtonGreenRGB = "rgb(61, 220, 145)"
    LoginErrorRedRGB = "rgb(226, 35, 26)"
