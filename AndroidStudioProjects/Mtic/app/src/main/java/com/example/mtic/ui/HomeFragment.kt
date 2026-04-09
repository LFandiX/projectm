package com.example.mtic.ui

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.mtic.R
import com.example.mtic.data.api.RetrofitClient
import com.example.mtic.data.model.Movie
import com.example.mtic.ui.adapter.MovieAdapter
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

// Perhatikan: layout harusnya bernama fragment_home atau activity_home (sesuai file xml kamu)
class HomeFragment : Fragment(R.layout.activity_home) {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: MovieAdapter

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        recyclerView = view.findViewById(R.id.rvMovies)
        recyclerView.layoutManager = GridLayoutManager(context, 2)

        adapter = MovieAdapter(emptyList()) { movie ->
                val action = HomeFragmentDirections.actionHomeToDetail(movie)
            findNavController().navigate(action)
        }
        recyclerView.adapter = adapter

        fetchMovies()
    }

    private fun fetchMovies() {
        RetrofitClient.instance.getMovies().enqueue(object : Callback<List<Movie>> {
            override fun onResponse(call: Call<List<Movie>>, response: Response<List<Movie>>) {
                if (response.isSuccessful) {
                    response.body()?.let { adapter.updateData(it) }
                }
            }
            override fun onFailure(call: Call<List<Movie>>, t: Throwable) {
                Toast.makeText(context, "Error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}