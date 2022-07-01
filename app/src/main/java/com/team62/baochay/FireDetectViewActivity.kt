package com.team62.baochay

import android.annotation.SuppressLint
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.compose.runtime.Composable
import androidx.activity.ComponentActivity
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import coil.compose.rememberAsyncImagePainter
import com.team62.baochay.model.DeviceNotification
import com.team62.baochay.ui.theme.PBL5BaoChayTheme
import java.text.SimpleDateFormat
import java.util.*

class FireDetectViewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            // A surface container using the 'background' color from the theme
            PBL5BaoChayTheme {
                val item: DeviceNotification? = intent.extras?.get("object") as DeviceNotification
                if (item != null)
                    Screen_FireAlert(item)
            }
        }
    }
}

@SuppressLint("SimpleDateFormat")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Screen_FireAlert(item: DeviceNotification) {
    Scaffold(
        topBar = {
            SmallTopAppBar(
                title = {
                    Text(stringResource(id = R.string.app_name) + " - Details")
                },
            )
        },
        content = { padding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
            ) {
                Column(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.Top,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    val sdf = SimpleDateFormat("dd/MM/yyyy HH:mm:ss")
                    val netDate = Date(if (item.date.toString().length < 13) item.date * 1000 else item.date)
                    Text(
                        text = "Detected on:",
                        style = MaterialTheme.typography.headlineMedium
                    )
                    Text(
                        text = sdf.format(netDate),
                        style = MaterialTheme.typography.titleLarge
                    )
                    Spacer(modifier = Modifier.size(5.dp))
                    Text(
                        text = "Temperature: ${item.physcal_info.temperature} C",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Text(
                        text = "Humidity: ${item.physcal_info.humidity}%",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Text(
                        text = "CO Detected: ${item.physcal_info.co_detected}",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    Spacer(modifier = Modifier.size(15.dp))
                    val localWidth = LocalConfiguration.current.screenWidthDp
                    val localHeight = localWidth * 480 / 640
                    Image(
                        painter = rememberAsyncImagePainter(item.image_url),
                        contentDescription = sdf.format(netDate),
                        modifier = Modifier.size(localWidth.dp, localHeight.dp)
                    )
                }
            }
        }
    )
}