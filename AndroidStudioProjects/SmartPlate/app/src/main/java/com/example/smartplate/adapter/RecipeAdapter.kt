package com.example.smartplate.adapter


import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.smartplate.R

import com.example.smartplate.model.Recipe

class RecipeAdapter(private var recipes: List<Recipe>) :
    RecyclerView.Adapter<RecipeAdapter.RecipeViewHolder>() {

    class RecipeViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val imgRecipe: ImageView = view.findViewById(R.id.imgRecipe)
        val tvTitle: TextView = view.findViewById(R.id.tvRecipeTitle)
        val tvCalories: TextView = view.findViewById(R.id.tvCalories)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecipeViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_recipe, parent, false)
        return RecipeViewHolder(view)
    }
    var onItemClick: ((Recipe) -> Unit)? = null
    override fun onBindViewHolder(holder: RecipeViewHolder, position: Int) {
        val recipe = recipes[position]
        holder.tvTitle.text = recipe.title

        // Ambil kalori dari data nutrition (jika ada)
        val calories = recipe.nutrition?.nutrients?.find { it.name == "Calories" }
        holder.tvCalories.text = "${calories?.amount?.toInt() ?: 0} Kkal"
        holder.tvCalories.setTextColor(Color.WHITE)
        // Load gambar menggunakan Glide
        Glide.with(holder.itemView.context)
            .load(recipe.image)
            .placeholder(android.R.color.darker_gray)
            .into(holder.imgRecipe)
        holder.itemView.setOnClickListener {
            onItemClick?.invoke(recipe)
        }
    }

    override fun getItemCount(): Int = recipes.size

    // Fungsi untuk update data jika ada hasil pencarian baru
    fun setData(newRecipes: List<Recipe>) {
        recipes = newRecipes
        notifyDataSetChanged()
    }
}