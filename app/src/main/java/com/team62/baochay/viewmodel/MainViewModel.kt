package com.team62.baochay.viewmodel

import android.content.ContentValues
import android.util.Log
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.ktx.auth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.ValueEventListener
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import com.team62.baochay.model.DeviceInfo
import com.team62.baochay.model.LoginStatus
import kotlinx.coroutines.launch

class MainViewModel: ViewModel() {
    private var mAuth: FirebaseAuth? = null
    private var currentUser: MutableState<FirebaseUser?> = mutableStateOf(null)
    var loginStatus: MutableState<LoginStatus> = mutableStateOf(LoginStatus.NotLoggedIn)
    var mainActivitySnackBar: SnackbarHostState? = null

    var Auth: FirebaseAuth?
        get() = mAuth
        set(value) { mAuth = value }

    private fun showSnackBar(msg: String) {
        viewModelScope.launch {
            mainActivitySnackBar?.currentSnackbarData?.dismiss()
            mainActivitySnackBar?.showSnackbar(msg)
        }
    }

    fun createUserWithEmailAndPassword(
        email: String,
        password: String,
        taskDone: (Boolean) -> Unit
    ) {
        if (mAuth == null)
            return;

        loginStatus.value = LoginStatus.LoggingIn

        mAuth!!.createUserWithEmailAndPassword(email, password)
            .addOnCompleteListener {
                when (it.isSuccessful) {
                    true -> {
                        Log.d(ContentValues.TAG, "createUserWithEmail:success")
                        showSnackBar("Successfully registered!")
                        currentUser.value = mAuth!!.currentUser
                        loginStatus.value = LoginStatus.LoggedIn
                        taskDone(true)
                    }
                    false -> {
                        Log.w(ContentValues.TAG, "createUserWithEmail:failure", it.exception)
                        showSnackBar("Failed while registering your account!")
                        loginStatus.value = LoginStatus.LoggedIn
                        taskDone(false)
                    }
                }
            }
    }

    fun signInWithEmailAndPassword(
        email: String,
        password: String,
        taskDone: (Boolean) -> Unit
    ) {
        loginStatus.value = LoginStatus.LoggingIn

        mAuth!!.signInWithEmailAndPassword(email, password)
            .addOnCompleteListener {
                when (it.isSuccessful) {
                    true -> {
                        Log.d(ContentValues.TAG, "signInWithEmail:success")
                        currentUser.value = mAuth!!.currentUser
                        loginStatus.value = LoginStatus.LoggedIn
                        showSnackBar("Successfully logged in!")
                        taskDone(true)
                    }
                    false -> {
                        Log.w(ContentValues.TAG, "signInWithEmail:failure", it.exception)
                        loginStatus.value = LoginStatus.NotLoggedIn
                        showSnackBar("Failed while logging in your account! Check your information, and try again.")
                        taskDone(false)
                    }
                }
            }
    }

    fun signOut(taskDone: (Boolean) -> Unit) {
        try {
            mAuth!!.signOut()
            currentUser.value = null
            loginStatus.value = LoginStatus.NotLoggedIn
            showSnackBar("Successfully logged out!")
            taskDone(true)
        }
        catch (ex: Exception) {
            Log.w(ContentValues.TAG, "logout:failure", ex)
            showSnackBar("An issue has occurred while logging you out! Try again later.")
            taskDone(false)
        }
    }

    val deviceInfo = mutableStateListOf<DeviceInfo>()
    val loadingDeviceInfo = mutableStateOf(false)

    fun readDataFromRealtimeDatabase() {
        loadingDeviceInfo.value = true

        val database = Firebase.database
        database.reference.child("devices").addValueEventListener(object: ValueEventListener {
                override fun onDataChange(snapshot: DataSnapshot) {
                    deviceInfo.clear()
                    for (userSnapshot in snapshot.children){
                        val data = userSnapshot.getValue(DeviceInfo::class.java)
                        if (data != null &&
                            data.user_uid.size > 0 &&
                            data.user_uid.any { item -> item == currentUser.value?.uid }
                        ) {
                            deviceInfo.add(data)
                        }
                    }
                    loadingDeviceInfo.value = false
                }

                override fun onCancelled(error: DatabaseError) {
                    loadingDeviceInfo.value = false
                }
            })
    }

    val deviceUidChosen: MutableState<String?> = mutableStateOf(null)
    val deviceFireDateChosen: MutableState<String?> = mutableStateOf(null)

    fun canBack_MainScreen(deleteIfDetect: Boolean = false): Boolean {
        if (deviceUidChosen.value != null ||
            deviceFireDateChosen.value != null) {

            if (deleteIfDetect) {
                var deleteOnce = true
                if (deviceFireDateChosen.value != null && deleteOnce) {
                    deviceFireDateChosen.value = null
                    deleteOnce = false
                }

                if (deviceUidChosen.value != null && deleteOnce) {
                    deviceUidChosen.value = null
                }
            }

            return true
        }

        return false
    }

    init {
        // Check if user logged in in startup.
        loginStatus.value = LoginStatus.LoggingIn
        mAuth = Firebase.auth
        currentUser.value = mAuth!!.currentUser

        loginStatus.value = if (currentUser.value != null) LoginStatus.LoggedIn else LoginStatus.NotLoggedIn
    }
}
