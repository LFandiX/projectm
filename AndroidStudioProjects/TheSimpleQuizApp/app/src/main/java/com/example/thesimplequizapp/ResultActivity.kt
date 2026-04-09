package com.example.thesimplequizapp

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.TextView
import android.widget.Button
import android.content.Intent
class ResultActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_result)

        val scoreText: TextView = findViewById(R.id.score)
        val score = intent.getIntExtra("Score", 0)
        scoreText.text = "$score/10"

        val congratsText: TextView = findViewById(R.id.congrats)
        if (score > 7) {
            congratsText.text = "You Win!"
        } else {
            congratsText.text = "Try Again!"
        }

        val btnPlayAgain: Button = findViewById(R.id.btn_playagain)
        btnPlayAgain.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
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