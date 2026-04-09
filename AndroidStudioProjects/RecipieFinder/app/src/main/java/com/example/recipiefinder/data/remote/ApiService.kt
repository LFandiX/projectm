package com.example.recipiefinder.data.remote
import com.example.recipiefinder.data.remote.response.RecipeResponse
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    // Endpoint untuk mencari resep berdasarkan teks/bahan
    @GET("recipes/complexSearch")
    suspend fun searchRecipes(
        @Query("query") query: String,
        @Query("apiKey") apiKey: String = "bc4e4efab33545c4b1222c11d9ab8c82", // Ambil dari spoonacular.com
        @Query("number") number: Int = 20,
        @Query("addRecipeInformation") addInfo: Boolean = true
    ): RecipeResponse
}