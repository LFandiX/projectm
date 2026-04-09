package com.example.smartplate

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.lifecycle.lifecycleScope
import com.bumptech.glide.Glide
import com.example.smartplate.network.RetrofitInstance
import kotlinx.coroutines.launch

class RecipeDetailFragment : Fragment(R.layout.fragment_recipie_detail) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {

        }
    }
    private val API_KEY = "bc4e4efab33545c4b1222c11d9ab8c82"

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val recipeId = arguments?.getInt("recipeId") ?: return

        lifecycleScope.launch {
            try {
                val detail = RetrofitInstance.api.getRecipeInformation(recipeId, API_KEY)

                // Binding Data ke UI
                view.findViewById<TextView>(R.id.tvTitleDetail).text = detail.title
                view.findViewById<TextView>(R.id.tvHealthSummary).text = "Health Score: ${detail.healthScore}"

                // Gabungkan List Bahan jadi satu string teks
                val ingredientText = detail.extendedIngredients.joinToString("\n") { "• ${it.original}" }
                view.findViewById<TextView>(R.id.tvIngredients).text = ingredientText

                // Tampilkan instruksi (Hapus tag HTML jika ada)
                view.findViewById<TextView>(R.id.tvInstructions).text =
                    android.text.Html.fromHtml(detail.instructions ?: "No instructions available", 0)

                Glide.with(this@RecipeDetailFragment).load(detail.image).into(view.findViewById(R.id.imgDetail))

            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}