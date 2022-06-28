package com.team62.baochay.navbar

sealed class NavRoutes_Auth(val route: String) {
    object Login : NavRoutes_Auth("login")
    object LoggingIn : NavRoutes_Auth("loggingIn")
    object Register : NavRoutes_Auth("register")
}