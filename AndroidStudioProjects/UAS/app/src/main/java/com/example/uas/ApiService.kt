package com.example.uas.api

import com.example.uas.model.Task
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.Response
import com.example.uas.model.ApiResponse
import com.example.uas.model.TaskRequest

interface ApiService {
    @GET("api/tasks") // Sesuaikan dengan route di Flask kamu (misal: @app.route('/tasks'))
    fun getAllTasks(): Call<List<Task>>

    @FormUrlEncoded
    @PUT("api/tasks/{id}")
    fun updateTaskStatus(
        @Path("id") id: Int,
        @Field("status") status: String
    ): Call<Void>

    @POST("api/tasks/add")
    suspend fun createTask(@Body task: TaskRequest): Response<ApiResponse>
}