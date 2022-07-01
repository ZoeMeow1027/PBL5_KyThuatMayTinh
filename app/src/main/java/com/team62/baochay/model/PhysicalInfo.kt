package com.team62.baochay.model

import java.io.Serializable

data class PhysicalInfo(
    var temperature: Double = 0.0,
    var humidity: Double = 0.0,
    var co_detected: Boolean = false,
    var flame_detected: Boolean = false,
): Serializable