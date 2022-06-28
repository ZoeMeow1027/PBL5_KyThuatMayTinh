package com.team62.baochay.view

import androidx.compose.foundation.Image
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.ui.layout.ContentScale
import com.skydoves.landscapist.glide.GlideImage

@Composable
fun Screen_ViewImage(urlList: ArrayList<String>) {
    LazyColumn() {
        items(urlList) {
            GlideImage(
                imageModel = it,
                // Crop, Fit, Inside, FillHeight, FillWidth, None
                contentScale = ContentScale.Crop,
            )
        }
    }
}