package com.team62.baochay

import android.app.PendingIntent
import android.app.TaskStackBuilder
import android.content.ContentValues.TAG
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.google.gson.Gson
import com.team62.baochay.model.DeviceNotification


class MyFirebaseService : FirebaseMessagingService() {
    private val CHANNEL_ID = "Notification_BaoChay"

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        Log.d(TAG, "Received")

        val title = remoteMessage.notification!!.title
        val text = remoteMessage.notification!!.body

        val dataFromFirebase: String = remoteMessage.data["data"] ?: "{}"
        val gson = Gson()
        val objectFromJson = gson.fromJson(dataFromFirebase, DeviceNotification::class.java)

        sendNotification(title, text, objectFromJson)
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
    }

    @RequiresApi(Build.VERSION_CODES.M)
    private fun sendNotification(title: String?, text: String?, objectFromJson: DeviceNotification) {
        val resultIntent  = Intent(this, FireDetectViewActivity::class.java)
            .setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK)
            .putExtra("object", objectFromJson)

        val resultPendingIntent: PendingIntent? = TaskStackBuilder.create(this).run {
            // Add the intent, which inflates the back stack
            addNextIntentWithParentStack(resultIntent)
            // Get the PendingIntent containing the entire back stack
            getPendingIntent(0,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
        }

        val nc = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentIntent(resultPendingIntent)
            .setAutoCancel(true)
            .setContentTitle(title)
            .setContentText(text)

        with(NotificationManagerCompat.from(this)) {
            // notificationId is a unique int for each notification that you must define
            notify(3, nc.build())
        }
    }
}