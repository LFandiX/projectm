package com.example.mtic.data.model

data class BookingRequest(
    val movie_id: Int,
    val user_name: String,
    val total_tickets: Int,
    val total_price: Double
)