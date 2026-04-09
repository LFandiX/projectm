package com.example.mtic.data.model

import java.io.Serializable

data class Movie(
    val id: Int,
    val title: String,
    val description: String,
    val poster_url: String,
    val price: Double
) : Serializable