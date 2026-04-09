package com.example.recipiefinder.ui

import com.example.recipiefinder.data.remote.response.RecipeItem


sealed class RecipeState {
    object Idle : RecipeState()
    object Loading : RecipeState()
    data class Success(val data: List<RecipeItem>) : RecipeState()
    data class Error(val message: String) : RecipeState()
}