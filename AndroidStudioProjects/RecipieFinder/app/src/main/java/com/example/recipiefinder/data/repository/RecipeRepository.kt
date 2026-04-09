package com.example.recipiefinder.data.repository

import com.example.recipiefinder.data.remote.ApiService
import javax.inject.Inject

class RecipeRepository @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun searchRecipes(query: String) = apiService.searchRecipes(query = query)
}