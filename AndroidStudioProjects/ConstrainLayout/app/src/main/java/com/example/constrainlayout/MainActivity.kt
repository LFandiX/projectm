package com.example.constrainlayout

import android.annotation.SuppressLint
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.Toast
class MainActivity : AppCompatActivity() {

    //private val data = listOf<String>("Apple", "Banana", "Grape", "WaterMelon","Pear", "Cherry")
    //
    private val fruitList = arrayListOf<Fruit>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        //1.
//        val adapter = ArrayAdapter<String>(this, android.R.layout.simple_list_item_1,data)
//
//        val listview = findViewById<ListView>(R.id.listView)
//        listview.adapter = adapter
        // 2.
        initFruits()
        val fruitAdapter = FruitAdapter(this,R.layout.fruit_item, fruitList)
        val listView = findViewById<ListView>(R.id.listView)
        listView.adapter = fruitAdapter
        listView.setOnItemClickListener{
            parent,view,position,id ->{
                val fruit = fruitList[position]
            Toast.makeText(this, fruit.name, Toast.LENGTH_LONG).show()
        }
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }
    private fun initFruits(){
        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))

        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))
        fruitList.add(Fruit("Apple", R.drawable.apple))

        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))

        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))
        fruitList.add(Fruit("Apple", R.drawable.apple))

        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))

        fruitList.add(Fruit("Apple", R.drawable.apple))
        fruitList.add(Fruit("Orange", R.drawable.apple))
        fruitList.add(Fruit("Grape", R.drawable.apple))
        fruitList.add(Fruit("WaterMelon", R.drawable.apple))
        fruitList.add(Fruit("Pear", R.drawable.apple))
        fruitList.add(Fruit("Apple", R.drawable.apple))


    }
}

