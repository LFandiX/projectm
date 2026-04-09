package com.example.myapplication

import android.os.Bundle
import android.widget.ArrayAdapter
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.ListView
import android.content.Intent
import android.widget.Toast
class MainActivity : AppCompatActivity() {

    private val data = listOf<String>("Start New Quizz","About","Close App")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        //1.
        val listView = findViewById<ListView>(R.id.listView)

        val adapter = ArrayAdapter(
            this,
            R.layout.list_item,
            R.id.itemText,
            data
        )

        listView.adapter = adapter

        listView.setOnItemClickListener { _, _, position, _ ->
            when (position) {
                0 -> { // "Start"
                    val intent = Intent(this, QuestionActivity::class.java)
                    startActivity(intent)
                }

                1 -> { // "About"
                    val intent = Intent(this, AboutActivity::class.java)
                    startActivity(intent)
                }

                2 -> { // "Close App"
                    finishAffinity()
                }

                else -> {
                    Toast.makeText(this, "Unknown item clicked", Toast.LENGTH_SHORT).show()
                }
            }
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

    }
}