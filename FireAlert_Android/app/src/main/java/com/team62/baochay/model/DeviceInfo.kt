package com.team62.baochay.model

data class DeviceInfo(
    var user_uid: ArrayList<String> = ArrayList(),
    var name: String = "",
    var token: String = "",
    var notifications: ArrayList<DeviceNotification> = ArrayList()
)

