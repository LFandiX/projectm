package com.example.thesimplequizapp

import android.content.Intent
import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.TextView
import android.widget.Button
import android.widget.Toast




class MainActivity : AppCompatActivity() {
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

//    private val questions = listOf(
//        "Docetism: Kristus hanya tampak seperti manusia?" to true,
//        "Ebionism: Krstus hanyalah Manusia" to false,
//        "Adoptionism: Yesus hanyalah manusia yang diadopsi menjadi Anak saat Baptisan, Kematian dan KenaikanNya" to true,
//        "Sabellianism: Bapa, Anak, Dan Roh Kudus bukan pribadi yang berbeda" to true,
//        "Patripassianism: Bapa turut menderita dan mati di atas kayu salib" to true,
//        "Arianism: Kristus (Ciptaan Bapa yang tertinggi) tidak sehakekat dengan bapa" to true,
//        "Apollinarianisme: Kristus memiliki tubuh, Jiwa manusia, tanpa roh manusia, Natur manusia Kristus tidak komplit" to true,
//        "Nestorianisme: Kristus memiliki dua pribadi: Ilahi dan Manusia. Maria adalah Christotokos" to true,
//        "monophysitism: Kristus memiliki 1 natur" to true,
//        "eutychianism: Natur manusia Kristus melebur ke natur ilahi Kristus" to true,
//        "Monotheletism: Kristus memiliki 1 kehendak" to true
//    )

    private var score = 0
    private var helpCount = 0
    private var currentIndex = 0
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

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