package com.team62.baochay

import android.app.NotificationManager
import android.app.PendingIntent
import android.app.TaskStackBuilder
import android.content.ContentValues.TAG
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.unit.dp
import androidx.core.app.NotificationCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import com.google.android.gms.tasks.OnCompleteListener
import com.google.firebase.messaging.FirebaseMessaging
import com.google.gson.Gson
import com.team62.baochay.model.DeviceNotification
import com.team62.baochay.model.LoginStatus
import com.team62.baochay.ui.theme.PBL5BaoChayTheme
import com.team62.baochay.view.Screen_Auth
import com.team62.baochay.view.Screen_LoggingIn
import com.team62.baochay.view.Screen_Main
import com.team62.baochay.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            // A surface container using the 'background' color from the theme
            PBL5BaoChayTheme {
                MainScreen()

                FirebaseMessaging.getInstance().token.addOnCompleteListener(OnCompleteListener { task ->
                    if (!task.isSuccessful) {
                        Log.w(TAG, "Fetching FCM registration token failed", task.exception)
                        return@OnCompleteListener
                    }

                    // Get new FCM registration token
                    val token = task.result

                    // Log and toast
                    val msg = token
                    Log.d(TAG, msg)
                    Toast.makeText(baseContext, msg, Toast.LENGTH_SHORT).show()
                })
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen() {
    val mainViewModel: MainViewModel = viewModel()
    val snackBarHostState = remember { SnackbarHostState() }

    mainViewModel.mainActivitySnackBar = snackBarHostState

    Scaffold(
        snackbarHost = { SnackbarHost(snackBarHostState) },
        topBar = {
            SmallTopAppBar(
                title = {
                    Text(stringResource(id = R.string.app_name))
                },
                actions = {
                    if (mainViewModel.loginStatus.value == LoginStatus.LoggedIn) {
                        Box(
                            modifier = Modifier.clickable {
                                    mainViewModel.signOut(taskDone = {})
                                }
                        ) {
                            Icon(
                                modifier = Modifier.padding(10.dp),
                                imageVector = ImageVector.vectorResource(id = R.drawable.ic_baseline_logout_24),
                                contentDescription = "Logout",
                            )
                        }
                    }
                },
            )
        },
        floatingActionButton = {
            if (mainViewModel.loginStatus.value == LoginStatus.LoggedIn &&
                    mainViewModel.deviceUidChosen.value == null) {
                FloatingActionButton(
                    onClick = {
                        // TODO: Add device by uid here!
                    },
                    content = {
                        Icon(ImageVector.vectorResource(id = R.drawable.ic_baseline_add_24), contentDescription = "Add device by UID")
                    },
                )
            }
        },
        content = { contentPadding ->
            Box(modifier = Modifier.padding(contentPadding)) {
                when (mainViewModel.loginStatus.value) {
                    LoginStatus.NotLoggedIn -> Screen_Auth(mainViewModel = mainViewModel)
                    LoginStatus.LoggingIn -> Screen_LoggingIn()
                    LoginStatus.LoggedIn -> {
                        Screen_Main(mainViewModel)
                        mainViewModel.readDataFromRealtimeDatabase()
                    }
                    LoginStatus.Unknown -> {
                        // TODO: Here
                    }
                }
            }
        }
    )
}