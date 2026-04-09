package com.example.recipiefinder.ui.viewmodel

import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.recipiefinder.data.repository.RecipeRepository
import com.example.recipiefinder.ui.RecipeState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class RecipeViewModel @Inject constructor(
    private val repository: RecipeRepository
) : ViewModel() {

    private val _state = mutableStateOf<RecipeState>(RecipeState.Idle)
    val state: State<RecipeState> = _state

    fun searchRecipes(query: String) {
        viewModelScope.launch {
            _state.value = RecipeState.Loading
            try {
                val response = repository.searchRecipes(query)
                _state.value = RecipeState.Success(response.results)
            } catch (e: Exception) {
                _state.value = RecipeState.Error(e.localizedMessage ?: "Terjadi kesalahan")
            }
        }
    }
}