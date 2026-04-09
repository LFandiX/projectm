package com.example.myapplication

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class HelpActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_help)
        val hintText: TextView = findViewById(R.id.hint)
        val hint = intent.getBooleanExtra("Help",true)
        hintText.text = "$hint"


        val IndexQ = intent.getIntExtra("IndexQ", 0)
        val HelpCount = intent.getIntExtra("HelpCount", 0)
        val Score = intent.getIntExtra("Score", 0)
        val btnBack: Button = findViewById(R.id.btn_back)
        btnBack.setOnClickListener {
            val intent = Intent(this, QuestionActivity::class.java)
            intent.putExtra("IndexQ", IndexQ)
            intent.putExtra("HelpCount", HelpCount)
            intent.putExtra("Score", Score)
            startActivity(intent)
            finish()
        }
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }
}