package com.example.smartplate.model

data class RecipeDetailResponse(
    val id: Int,
    val title: String,
    val image: String,
    val summary: String, // Deskripsi singkat
    val instructions: String?, // Langkah memasak
    val readyInMinutes: Int,
    val healthScore: Double,
    val extendedIngredients: List<Ingredient>
)

data class Ingredient(
    val original: String // Nama bahan lengkap (misal: "2 cups of flour")
)