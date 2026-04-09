package com.example.recipiefinder.ui.screen

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.example.recipiefinder.ui.viewmodel.RecipeViewModel

@Composable
fun HomeScreen(viewModel: RecipeViewModel) {
    var query by remember { mutableStateOf("") }
    val state by viewModel.state

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        // Search Bar
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            label = { Text("Cari Bahan (misal: Chicken)") },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { viewModel.searchRecipes(query) },
            modifier = Modifier.padding(top = 8.dp)
        ) {
            Text("Cari Resep")
        }

        Spacer(modifier = Modifier.height(16.dp))

        // UI berdasarkan State
        when (state) {
            is RecipeState.Loading -> CircularProgressIndicator()
            is RecipeState.Success -> {
                LazyColumn {
                    items((state as RecipeState.Success).data) { recipe ->
                        RecipeCard(recipe.title, recipe.image)
                    }
                }
            }
            is RecipeState.Error -> Text("Error: ${(state as RecipeState.Error).message}")
            else -> Text("Silahkan cari resep!")
        }
    }
}

@Composable
fun RecipeCard(title: String, imageUrl: String) {
    Card(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
        Row(modifier = Modifier.padding(8.dp)) {
            AsyncImage(
                model = imageUrl,
                contentDescription = null,
                modifier = Modifier.size(80.dp)
            )
            Text(text = title, modifier = Modifier.padding(start = 16.dp))
        }
    }
}