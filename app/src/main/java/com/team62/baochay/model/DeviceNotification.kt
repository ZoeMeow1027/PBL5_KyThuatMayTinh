package com.team62.baochay.model

import java.io.Serializable

data class DeviceNotification(
    var date: Long = 0,
    var image_url: String = "",
    var physcal_info: PhysicalInfo = PhysicalInfo()
): Serializable
