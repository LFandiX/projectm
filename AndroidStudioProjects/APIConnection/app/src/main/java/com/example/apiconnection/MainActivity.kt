package com.example.apiconnection

import android.icu.number.Scale
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.converter.scalars.ScalarsConverterFactory
import retrofit2.create

class MainActivity : AppCompatActivity() {
    private val retrofit by lazy {
//        Retrofit.Builder()
//            .baseUrl("https://api.thecatapi.com/v1/")
//            .addConverterFactory(ScalarsConverterFactory.create())
//            .build()
//    }
        Retrofit.Builder()
            .baseUrl("https://dogapi.dog/api/v2/")
            .addConverterFactory(ScalarsConverterFactory.create())
            .build()
    }

    //    private val theCatApiService by lazy {
//        retrofit.create(TheCatApiService::class.java)
//    }
    private val theDogFactData by lazy {
        retrofit.create(TheDogFactData::class.java)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
//        this.getCatImage()
        this.getDogFact()
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    //    private fun getCatImage(){
//        val call = theCatApiService.searchImage(1)
//        call.enqueue(object : Callback<String> {
//            override fun onResponse(call: Call<String>, response: Response<String>) {
//                if (response.isSuccessful) {
//                    val valrespTextview = findViewById<TextView>(R.id.catResponse)
//                    val hasilResponse = response.body()
//
//                    // 3. Masukkan ke TextView
//                    valrespTextview.text = hasilResponse
//
//                } else {
//                    Log.e("CatAPI", "Gagal memuat: ${response.code()}")
//                }
//            }
//
//            override fun onFailure(call: Call<String>, t: Throwable) {
//                Log.e("CatAPI", "Error Koneksi: ${t.message}")
//            }
//        })
//    }
    private fun getDogFact() {
        val call = theDogFactData.searchImage(3)
        call.enqueue(object:Callback<DogData>{
            override fun onFailure(call: Call<DogData>, t: Throwable) {
                Log.e("MainActivity", "Failed to get data")
            }

            override fun onResponse(
                call: Call<DogData>,
                response: Response<DogData>
            ) {
                if(response.isSuccessful) {
                    val facts = response.body()
                    facts?.data?.forEach {
                        Log.e("MainActivity", "ID:${it.id} type:${it.Type}")
                    }
                }else{
                    Log.e("MainActivity", "Failed: ${response.errorBody()}")
                }
            }
        })
    }
}






