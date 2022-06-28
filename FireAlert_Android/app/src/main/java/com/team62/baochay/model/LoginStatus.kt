package com.team62.baochay.model

enum class LoginStatus(i: Int) {
    Unknown(-1),
    LoggingIn(0),
    LoggedIn(1),
    NotLoggedIn(2),
}