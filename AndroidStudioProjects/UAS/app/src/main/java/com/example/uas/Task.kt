package com.example.uas.model

import com.google.gson.annotations.SerializedName

data class Task(
    val id: Int,
    val title: String,
    val description: String?,
    val category: String, // 'N', 'U', 'I'
    val status: String,   // 'New', 'In Progress', 'Done'

    @SerializedName("created_time")
    val createdTime: String?,

    @SerializedName("finished_time")
    val finishedTime: String?,

    val duration: Int?,
    val deleted: String // 'False', 'True'
)

data class TaskRequest(
    val title: String,
    val description: String?,
    val category: String, // 'N', 'U', 'I'
    val status: String,   // 'New', 'In Progress', 'Done'
)
// Response SEDERHANA tanpa data
data class ApiResponse(
    val success: Boolean,
    val message: String
)