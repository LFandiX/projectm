package com.example.datapresistensi

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import androidx.annotation.UiThread // Ini mungkin tidak diperlukan untuk MyDBHelper, bisa dihapus

// Gunakan nama konstanta untuk nama database, tabel, dan kolom (disarankan)
private const val DATABASE_NAME = "BookStore.db"
private const val DATABASE_VERSION = 1
private const val TABLE_NAME = "Book"

class MyDBHelper (context: Context) :
    SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    // Gunakan Triple Quoted String untuk SQL agar lebih mudah dibaca dan menghindari masalah spasi
    private val createBook = """
        CREATE TABLE $TABLE_NAME (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL
        )
    """.trimIndent()

    override fun onCreate(db: SQLiteDatabase) {
        // Jalankan perintah untuk membuat tabel
        db.execSQL(createBook)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Hapus tabel lama jika ada, lalu buat yang baru.
        // PERINGATAN: Ini menghapus semua data!
        db.execSQL("DROP TABLE IF EXISTS $TABLE_NAME")
        onCreate(db)
    }
}