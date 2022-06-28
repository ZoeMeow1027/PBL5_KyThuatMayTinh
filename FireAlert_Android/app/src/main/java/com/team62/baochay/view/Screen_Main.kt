package com.team62.baochay.view

import android.annotation.SuppressLint
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.team62.baochay.viewmodel.MainViewModel
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun Screen_Main(mainViewModel: MainViewModel) {
    BackHandler(enabled = mainViewModel.canBack_MainScreen(false)) {
        mainViewModel.canBack_MainScreen(true)
    }

    if (mainViewModel.deviceUidChosen.value == null) {
        mainViewModel.readDataFromRealtimeDatabase()
        Screen_DeviceList(
                mainViewModel,
                deviceUidClicked = {item ->
                    mainViewModel.deviceUidChosen.value = item
                }
            )
    }
    else
    {
        mainViewModel.readDataFromRealtimeDatabase()
        Screen_DeviceHistory(
            mainViewModel = mainViewModel,
            uid = mainViewModel.deviceUidChosen.value
        )
    }
}

@Composable
fun Screen_DeviceList(
    mainViewModel: MainViewModel,
    deviceUidClicked: (String) -> Unit
) {
    if (mainViewModel.loadingDeviceInfo.value) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            CircularProgressIndicator()
        }
    }
    else {
        LazyColumn(
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.fillMaxSize()
        ) {
            item {
                Column() {
                    Text(
                        text = "Your own device list",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Spacer(modifier = Modifier.size(10.dp))
                }
            }
            items(mainViewModel.deviceInfo) {
                Box(
                    modifier = Modifier
                        .padding(top = 5.dp, bottom = 5.dp, start = 10.dp, end = 10.dp)
                        .fillMaxWidth()
                        .wrapContentHeight()
                        .clip(RoundedCornerShape(15.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer)
                        .clickable {
                            deviceUidClicked(it.token)
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = it.name,
                        modifier = Modifier.padding(15.dp),
                        fontSize = 20.sp
                    )
                }
            }
        }
    }
}

@SuppressLint("SimpleDateFormat")
@Composable
fun Screen_DeviceHistory(
    mainViewModel: MainViewModel,
    uid: String?,
) {
    if (mainViewModel.loadingDeviceInfo.value) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            CircularProgressIndicator()
        }
    }
    else {
        LazyColumn(
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.fillMaxSize()
        ) {
            try {
                item {
                    Column() {
                        Text(
                            text = "Your fire detected history",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Spacer(modifier = Modifier.size(5.dp))
                        Text(
                            text = "Device: ${mainViewModel.deviceInfo.filter { it.token == uid }[0].name}",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Spacer(modifier = Modifier.size(10.dp))
                    }
                }
                items(mainViewModel.deviceInfo.filter { it.token == uid }[0].notifications) {
                    item ->
                    Box(
                        modifier = Modifier
                            .padding(top = 5.dp, bottom = 5.dp, start = 10.dp, end = 10.dp)
                            .fillMaxWidth()
                            .wrapContentHeight()
                            .clip(RoundedCornerShape(15.dp))
                            .background(MaterialTheme.colorScheme.primaryContainer)
                            .clickable {

                            },
                        contentAlignment = Alignment.Center
                    ) {
                        val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
                        val netDate = Date(if (item.date.toString().length < 13) item.date * 1000 else item.date)
                        Text(
                            text = sdf.format(netDate),
                            modifier = Modifier.padding(15.dp),
                            fontSize = 20.sp
                        )
                    }
                }
            }
            catch (ex: Exception) {
                item {
                    Column(
                        verticalArrangement = Arrangement.Top,
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.fillMaxSize()
                    ) {

                    }
                }
            }
        }
    }
}