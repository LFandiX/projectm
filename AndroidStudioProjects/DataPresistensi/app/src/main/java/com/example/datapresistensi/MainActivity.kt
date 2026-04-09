package com.example.datapresistensi

import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.ContactsContract
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.IOException
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.util.jar.Manifest


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)


        // # 1 FIle
        val saveBtn = findViewById<Button>(R.id.save_btn)

        val msgEt = findViewById<EditText>(R.id.message_edit)


        msgEt.setText(loadMessage())


        saveBtn.setOnClickListener {
            this.save(msgEt.text.toString())
        }

        // # 2 Shared
        val saveShared = findViewById<Button>(R.id.save_btn_shared)
        saveShared.setOnClickListener {
            val spEditor = getSharedPreferences("MessageSp", Context.MODE_PRIVATE).edit()

            spEditor.putInt("number", 1)
            spEditor.putString("msg", msgEt.text.toString())

            spEditor.apply()

            Toast.makeText(this,"save Into shared pregerance", Toast.LENGTH_LONG)
        }

        val storeShareButton = findViewById<Button>(R.id.StoreSP)
        storeShareButton.setOnClickListener {
            val spEditor = getSharedPreferences("MessageSp", Context.MODE_PRIVATE)
            val message = spEditor.getString("msg", "[ Blank ]")
            msgEt.setText(message)
        }

        // # 2 Shared

//        val dbHelper = MyDbHelper(this, "BookStore.db",11)
//        val createDbBtn = findViewById<Button>(R.id.bookPstore)
//        createDbBtn.setOnClickListener {
//            dbHelper.writetableDatabase
//
//                Toast.makeText(this,"db created", Toast.LENGTH_LONG)
//
//        }
//
//        //add book
//
//        val addbBookBtn = findViewById<Button>(R.id.adddb)
//        addbBookBtn.setOnClickListener {
//            val db = dbHelper.writetableDatabase
//            val value1 = ContentValues().apply{
//                put("title", "android Programming book")
//                put("price", 200000)
//            }
//            db.insert("Book",null,value1)
//
//        }

        // Inisialisasi MyDBHelper (di luar event listener, misalnya di onCreate Activity)
// Nama dan Versi sudah ada di dalam class MyDBHelper
        val dbHelper = MyDBHelper(this)

// --- /create db ---
        val createDbBtn = findViewById<Button>(R.id.bookPstore) // Pastikan ID dan tipe View benar

        createDbBtn.setOnClickListener {
            // Akses properti writableDatabase untuk memicu onCreate/onUpgrade
            val db = dbHelper.writableDatabase

            Toast.makeText(this, "db created", Toast.LENGTH_LONG).show()
        }

// --- /add book ---
        val addBookBtn = findViewById<Button>(R.id.adddb) // Pastikan ID dan tipe View benar

        addBookBtn.setOnClickListener {
            // 1. Dapatkan referensi database
            val db = dbHelper.writableDatabase

            // 2. Buat objek ContentValues
            val value1 = ContentValues().apply {
                put("title", "Android Programming book")
                // Pastikan nama kolom "price" sama persis dengan yang ada di SQL: price REAL
                put("price", 200000.0) // Pastikan tipe data REAL/Double, bukan Integer (200000)
            }

            // 3. Masukkan data ke tabel "Book"
            // Parameter kedua ('nullColumnHack') di set 'null'
            db.insert("Book", null, value1)

            Toast.makeText(this, "Book added!", Toast.LENGTH_SHORT).show()
        }




        // # PERTEMUAN BARU

        // Make a call runtime Permission
        val makeCallBtn = findViewById<Button>(R.id.makecall)
        makeCallBtn.setOnClickListener {

            if(ContextCompat.checkSelfPermission(this, android.Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED){
                ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.CALL_PHONE),1)
            } else{
            this.makecall()
            }
        }

        val readcontact = findViewById<Button>(R.id.readcontact)
        readcontact.setOnClickListener {




            if(ContextCompat.checkSelfPermission(this, android.Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED){
                ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.READ_CONTACTS),2)
            } else{
                this.readCondtact()
            }
        }



        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }


    }

    // #. 1 Data Presistence Using File
    private fun save(message: String){
        try{
            val fileOutput = openFileOutput("message", Context.MODE_PRIVATE)
            val writer = BufferedWriter(OutputStreamWriter(fileOutput))

            writer.use {
                it.write(message)
            }
        } catch (e: IOException){
            e.printStackTrace()
        }
    }
    private fun loadMessage() : String{
        val content = StringBuilder()
        try {
            val fileInput = openFileInput("message")
            val read = BufferedReader(InputStreamReader(fileInput))

            read.use{
                read.forEachLine{
                    content.append(it)
                }
            }
            return content.toString()
        } catch (e: IOException){
            e.printStackTrace()
        }
        return ""
    }

    private fun makecall(){

        try {
            val intent = Intent(Intent.ACTION_CALL)
            intent.data = Uri.parse("tel: +6289507013965")
            startActivity(intent)
        } catch (e: SecurityException){
            e.printStackTrace()
        }
    }

    // #. 2 Data Presistence Using Shared Preferences
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String?>,
        grantResults: IntArray,
        deviceId: Int
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults, deviceId)

        when(requestCode) {
            1 -> {
                if(grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    try {
                        val intent = Intent(Intent.ACTION_CALL)
                        intent.data = Uri.parse("tel: +6289507013965")
                        startActivity(intent)
                    } catch (e: SecurityException){
                        e.printStackTrace()
                    }
                } else {
                    Toast.makeText(this, "You deneid perpissio", Toast.LENGTH_LONG).show()
                }
            }
            2 ->{
                if(grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    try {
                       this.readCondtact()
                    } catch (e: SecurityException){
                        e.printStackTrace()
                    }
                } else {
                    Toast.makeText(this, "You deneid perpissio", Toast.LENGTH_LONG).show()
                }
            }
        }
    }
    //contact
    private fun readCondtact() {
        // Query ke content provider
        contentResolver.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            null, null, null, null
        )?.apply { // 'this' di dalam blok ini adalah Cursor

            try {
                // 1. Ambil indeks kolom HANYA SEKALI sebelum loop (lebih efisien)
                //    Gunakan getColumnIndexOrThrow agar aman jika kolom tidak ada
                val numberColumnIndex = getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER)
                // val nameColumnIndex = getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME) // -> Jika butuh nama juga

                // 2. Loop setiap baris data
                while (moveToNext()) {

                    // 3. Panggil getString milik CURSOR (this) menggunakan indeks
                    //    Ini adalah perbaikan utamanya
                    val phoneNumber = this.getString(numberColumnIndex)
                    // val contactName = this.getString(nameColumnIndex) // -> Jika butuh nama

                    Log.d("MainActivity", "Phonenum: $phoneNumber")
                }
            } catch (e: IllegalArgumentException) {
                // Handle error jika kolom tidak ditemukan
                Log.e("MainActivity", "Column not found", e)
            } finally {
                // 4. Selalu tutup cursor
                close()
            }
        }
    }

//
//    private fun readCondtact (){
//        //uri of share data
//        //content ://[com.example.datapresistensi]/[tablename]
////        var cursor = contentResolver.query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI,null,null,null,null)
////        if(cursor != null){
////            while (cursor.moveToNext()){
////
////            }
////        }
//        contentResolver.query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI,null,null,null,null)?.apply {
//            while (moveToNext()){
//                val contactname = getString(getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER),null,null)
//                Log.d("MainActivity","Phonenum: " + contactname)
//            }
//            close()
//        }
//
//    }
}