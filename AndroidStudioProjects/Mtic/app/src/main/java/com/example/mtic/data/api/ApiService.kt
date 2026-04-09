package com.example.mtic.data.api

import com.example.mtic.data.model.BookingRequest
import com.example.mtic.data.model.Movie
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("api/movies")
    fun getMovies(): Call<List<Movie>>

    @POST("api/book")
    fun bookTicket(@Body request: BookingRequest): Call<Map<String, Any>>
}