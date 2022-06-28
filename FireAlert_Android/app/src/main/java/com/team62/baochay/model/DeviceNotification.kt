package com.team62.baochay.model

data class DeviceNotification(
    var date: Long = 0,
    var image_url: String = "",
    var user_seen: ArrayList<String> = ArrayList()
)
