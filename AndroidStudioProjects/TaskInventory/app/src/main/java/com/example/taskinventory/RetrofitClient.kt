package com.example.taskinventory.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    // PENTING: Jika pakai Emulator Android, gunakan 10.0.2.2.
    // Jika pakai HP fisik, gunakan IP Address laptop (misal 192.168.1.x)
    private const val BASE_URL = "http://10.0.2.2:5000/"

    val instance: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}