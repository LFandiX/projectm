package com.example.smartplate.network

import com.example.smartplate.model.RecipeDetailResponse
import com.example.smartplate.model.RecipeResponse
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface SpoonacularService {
    @GET("recipes/complexSearch")
    suspend fun searchRecipes(
        @Query("apiKey") apiKey: String,
        @Query("query") query: String,
        @Query("maxCalories") maxCalories: Int?,
        @Query("number") number: Int = 10,
        @Query("addRecipeNutrition") addNutrition: Boolean = true
    ): RecipeResponse
    @GET("recipes/{id}/information")
    suspend fun getRecipeInformation(
        @Path("id") id: Int,
        @Query("apiKey") apiKey: String,
        @Query("includeNutrition") includeNutrition: Boolean = true
    ): RecipeDetailResponse
}