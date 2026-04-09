package com.example.activitytest

import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.EditText


class CommonUI : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_common_ui)
//
//        val btnsave : Button = findViewById(R.id.btn_save)
//        btnsave.setOnClickListener {
//            val desET = findViewById(R.id.description)
//            val _des = desET.Text.toString()
//            Toast.makeText(this,_des, Toast.LENGTH_LONG).show()
//
//        }
        val btnsave: Button = findViewById(R.id.btn_save)

        btnsave.setOnClickListener {
            val desET = findViewById<EditText>(R.id.description)
            val des_ = desET.text.toString()

            Toast.makeText(this, des_, Toast.LENGTH_LONG).show()
        }
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }
}