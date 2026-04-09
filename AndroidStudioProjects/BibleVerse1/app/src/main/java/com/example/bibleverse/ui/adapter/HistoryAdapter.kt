package com.example.bibleverse.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.bibleverse.data.JournalEntry
import com.example.bibleverse.databinding.ItemJournalHistoryBinding
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class HistoryAdapter(
    private val onDelete: (JournalEntry) -> Unit,
    private val onView: (JournalEntry) -> Unit
) : ListAdapter<JournalEntry, HistoryAdapter.ViewHolder>(DiffCallback) {

    class ViewHolder(val binding: ItemJournalHistoryBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemJournalHistoryBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val entry = getItem(position)
        holder.binding.entryTitle.text = "${entry.book} ${entry.chapter}"
        
        val sdf = SimpleDateFormat("MMM dd, yyyy • h:mm a", Locale.ENGLISH)
        holder.binding.entryDate.text = sdf.format(Date(entry.date))
        
        holder.binding.entryContent.text = entry.content
        
        holder.binding.btnDelete.setOnClickListener { onDelete(entry) }
        holder.binding.btnView.setOnClickListener { onView(entry) }
    }

    object DiffCallback : DiffUtil.ItemCallback<JournalEntry>() {
        override fun areItemsTheSame(oldItem: JournalEntry, newItem: JournalEntry) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: JournalEntry, newItem: JournalEntry) = oldItem == newItem
    }
}
