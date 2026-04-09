package com.example.myapplication

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class QuestionActivity : AppCompatActivity() {

    private val questions = listOf(
        "2 + 2 = 4 ?" to true,
        "5 * 2 = 15 ?" to false,
        "Bumi itu datar?" to false,
        "Matahari Terbit dari timur?" to true,
        "10 / 2 = 4 ?" to false,
        "Mozart lahir di Austria?" to true,
        "1 + 1 = 3 ?" to false,
        "Albert Einstein main biola?" to true,
        "CIT kepanjangan dari Calvin Institute of Theology?" to false,
        "7 adalah angka prima?" to true
    )

    private var score = 0
    private var helpCount = 0
    private var currentIndex = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_question)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        currentIndex = intent.getIntExtra("IndexQ", 0)
        helpCount = intent.getIntExtra("HelpCount", 0)
        score = intent.getIntExtra("Score", 0)


        val questionText: TextView = findViewById(R.id.question_text)
        questionText.text = questions[currentIndex].first

        val btnTrue: Button = findViewById(R.id.btn_true)
        btnTrue.setOnClickListener {
            if (questions[currentIndex].second) {
                score++

            }
            nextQuestion(questionText)
        }

        val btnFalse: Button = findViewById(R.id.btn_false)
        btnFalse.setOnClickListener {
            if (!questions[currentIndex].second) {
                score++

            }
            nextQuestion(questionText)
        }

        val btnHelp: Button = findViewById(R.id.btn_help)
        btnHelp.setOnClickListener {
            helpCount++
            if (helpCount <= 3) {
                val intent = Intent(this, HelpActivity::class.java)
                intent.putExtra("Help",questions[currentIndex].second)
                intent.putExtra("IndexQ", currentIndex)
                intent.putExtra("HelpCount", helpCount)
                intent.putExtra("Score", score)
                startActivity(intent)
            } else {
                Toast.makeText(this, "Reach Maximum Hint Support", Toast.LENGTH_LONG).show()
            }
        }


    }
    private fun nextQuestion(questionText: TextView) {
        currentIndex++

        if (currentIndex < questions.size) {
            // update soal berikutnya
            questionText.text = questions[currentIndex].first
        } else {
            // sudah selesai
            val intent = Intent(this, ResultActivity::class.java)
            intent.putExtra("Score",score)

            startActivity(intent)

        }
    }
}