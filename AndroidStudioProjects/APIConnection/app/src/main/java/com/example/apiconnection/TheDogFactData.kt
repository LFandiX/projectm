package com.example.apiconnection

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

interface TheDogFactData {
    @GET("facts")
    fun searchImage(
        @Query("limit") limit: Int
    ) : Call<DogData>

}