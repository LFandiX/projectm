package com.example.mtic.ui

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController // PERLU IMPORT INI
import androidx.navigation.fragment.navArgs
import com.bumptech.glide.Glide
import com.example.mtic.R
import com.example.mtic.data.model.BookingRequest // Ini mungkin tidak terpakai lagi di sini
// import retrofit... (Hapus import retrofit karena kita tidak booking di sini)

class DetailFragment : Fragment(R.layout.activity_detail) { // Pastikan nama layout sesuai

    private val args: DetailFragmentArgs by navArgs()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val movie = args.movieData

        // --- SETUP TAMPILAN (Sama seperti sebelumnya) ---
        view.findViewById<TextView>(R.id.tvDetailTitle).text = movie.title
        view.findViewById<TextView>(R.id.tvDetailDesc).text = movie.description
        val imgPoster = view.findViewById<ImageView>(R.id.imgDetailPoster)
        Glide.with(this).load(movie.poster_url).into(imgPoster)

        // Tombol Back (Jika Anda menambahkannya di XML)
        view.findViewById<ImageView>(R.id.btnBack)?.setOnClickListener {
            findNavController().popBackStack()
        }


        // --- PERUBAHAN PENTING DI SINI ---
        val btnBook = view.findViewById<Button>(R.id.btnBook)
        // Ubah teks tombol jadi "Select Seat" biar lebih pas
        btnBook.text = "SELECT SEAT"

        btnBook.setOnClickListener {
            // DULU: Langsung performBooking(request) -> HAPUS INI

            // SEKARANG: Pindah ke Fragment Pilih Kursi (SeatSelectionFragment)
            // Kita perlu membuat Fragment ini dulu di langkah selanjutnya.
            // Untuk sementara, kita kasih Toast dulu sebagai penanda.
            Toast.makeText(context, "Menuju Halaman Pilih Kursi...", Toast.LENGTH_SHORT).show()

            // NANTI KODENYA AKAN SEPERTI INI (Setelah Fragment Kursi dibuat):
            // val action = DetailFragmentDirections.actionDetailToSeatSelection(movie)
            // findNavController().navigate(action)
        }
    }

    // HAPUS FUNGSI performBooking() dari sini.
    // Fungsi itu akan dipindah ke Fragment Pilih Kursi nanti.
}