package com.team62.baochay.view

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.team62.baochay.model.LoginInformation
import com.team62.baochay.viewmodel.MainViewModel

@Composable
fun Screen_Auth(mainViewModel: MainViewModel) {
    val isRegisterValue = remember {
        mutableStateOf(false)
    }

    BackHandler(isRegisterValue.value) {
        isRegisterValue.value = false
    }

    if (isRegisterValue.value) Screen_Register(
        loginRequested = {
            isRegisterValue.value = false
        }
    )
    else Screen_Login(
        loginRequested = {
            mainViewModel.signInWithEmailAndPassword(it.user, it.pass) {

            }
        },
        registerRequested = {
            isRegisterValue.value = true
        }
    )
}

@Composable
fun Screen_Login(
    loginRequested: (LoginInformation) -> Unit,
    registerRequested: () -> Unit
) {
    val user = remember { mutableStateOf("") }
    val pass = remember { mutableStateOf("") }
    val passTextFieldFocusRequester = remember { FocusRequester() }
    val focusManager = LocalFocusManager.current

    fun login() {
        focusManager.clearFocus()
        loginRequested(LoginInformation(user.value, pass.value))
        pass.value = ""
    }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Login",
            style = MaterialTheme.typography.headlineMedium
        )
        Spacer(modifier = Modifier.size(20.dp))
        OutlinedTextField(
            value = user.value,
            onValueChange = { user.value = it },
            keyboardOptions = KeyboardOptions(imeAction = androidx.compose.ui.text.input.ImeAction.Next),
            keyboardActions = KeyboardActions(
                onGo = { passTextFieldFocusRequester.requestFocus() }
            ),
            label = { Text("Email") }
        )
        OutlinedTextField(
            modifier = Modifier
                .focusRequester(passTextFieldFocusRequester),
            value = pass.value,
            onValueChange = { pass.value = it },
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = androidx.compose.ui.text.input.ImeAction.Go
            ),
            keyboardActions = KeyboardActions(onGo = { login() }),
            label = { Text("Password") }
        )
        Spacer(modifier = Modifier.size(5.dp))
        Button(
            onClick = { login() },
            content = { Text("Login") }
        )
        Spacer(modifier = Modifier.size(10.dp))
        Text(text = "Not having account?")
        Button(
            onClick = {
                registerRequested()
                pass.value = ""
            },
            content = { Text("Register now") }
        )
    }
}

@Composable
fun Screen_Register(
    loginRequested: () -> Unit
) {
    val user = remember { mutableStateOf("") }
    val pass = remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        OutlinedTextField(
            value = user.value,
            onValueChange = { user.value = it },
            label = { Text("Email") }
        )
        OutlinedTextField(
            value = pass.value,
            onValueChange = { pass.value = it },
            label = { Text("Password") }
        )
        Button(
            onClick = {
                pass.value = ""
            },
            content = { Text("Register") }
        )
        Button(
            onClick = {
                loginRequested()
                pass.value = ""
            },
            content = { Text("Have an account? Login instead") }
        )
    }
}

@Composable
fun Screen_LoggingIn() {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            "Logging you in",
            style = MaterialTheme.typography.headlineSmall
        )
        Text(
            "Please wait...",
            style = MaterialTheme.typography.titleMedium
        )
        Spacer(modifier = Modifier.size(10.dp))
        CircularProgressIndicator()
    }
}