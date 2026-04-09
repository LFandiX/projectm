package com.example.smartplate

import android.os.Bundle
import android.view.View
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.smartplate.adapter.RecipeAdapter
import com.example.smartplate.network.RetrofitInstance
import kotlinx.coroutines.launch
import com.example.smartplate.R

class HomeFragment : Fragment(R.layout.fragment_home) {

    private lateinit var recipeAdapter: RecipeAdapter
    private val API_KEY = "bc4e4efab33545c4b1222c11d9ab8c82"

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val rvRecipes: RecyclerView = view.findViewById(R.id.rvRecipes)
        val etSearch: EditText = view.findViewById(R.id.etSearch)

        // Setup RecyclerView
        recipeAdapter = RecipeAdapter(listOf())
        rvRecipes.layoutManager = LinearLayoutManager(context)
        rvRecipes.adapter = recipeAdapter

        // Contoh: Panggil API saat pertama kali buka (rekomendasi sehat)
        fetchRecipes("healthy")
        recipeAdapter.onItemClick = { recipe ->
            val bundle = Bundle().apply {
                putInt("recipeId", recipe.id) // Kirim ID untuk ambil detail nanti
            }
            findNavController().navigate(R.id.action_homeFragment2_to_recipeDetailFragment, bundle)
        }
    }

    private fun fetchRecipes(query: String) {
        lifecycleScope.launch {
            try {
                val response = RetrofitInstance.api.searchRecipes(API_KEY, query, 500)
                recipeAdapter.setData(response.results)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}