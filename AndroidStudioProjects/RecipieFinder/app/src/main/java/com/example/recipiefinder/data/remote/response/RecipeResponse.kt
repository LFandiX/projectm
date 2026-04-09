package com.example.recipiefinder.data.remote.response

data class RecipeResponse(
    val results: List<RecipeItem>
)

data class RecipeItem(
    val id: Int,
    val title: String,
    val image: String,
    val summary: String? = "No description available"
)
