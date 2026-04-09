package com.example.taskinventory.api


// import Allneeded
import com.example.taskinventory.model.Task
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.POST

interface ApiService {
    @GET("api/tasks") // Sesuaikan dengan route di Flask kamu (misal: @app.route('/tasks'))
    fun getAllTasks(): Call<List<Task>>

    @FormUrlEncoded
    @PUT("api/tasks/{id}")
    fun updateTaskStatus(
        @Path("id") id: Int,
        @Field("status") status: String
    ): Call<Void>

    @FormUrlEncoded
    @POST("api/tasks")
    fun createTask(
        @Field("title") title: String,
        @Field("description") description: String,
        @Field("category") category: String
    ): Call<Void>
}