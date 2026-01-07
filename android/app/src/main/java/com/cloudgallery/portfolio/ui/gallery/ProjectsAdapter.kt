package com.cloudgallery.portfolio.ui.gallery

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.cloudgallery.portfolio.R
import com.cloudgallery.portfolio.databinding.ItemProjectCardBinding
import com.cloudgallery.portfolio.data.models.ColoringProject

class ProjectsAdapter(
    private val onProjectClick: (ColoringProject) -> Unit,
    private val onDeleteClick: (ColoringProject) -> Unit
) : ListAdapter<ColoringProject, ProjectsAdapter.ViewHolder>(ProjectDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemProjectCardBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ViewHolder(
        private val binding: ItemProjectCardBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(project: ColoringProject) {
            binding.apply {
                tvTitle.text = project.title ?: "Untitled"
                tvDifficulty.text = "${project.difficulty.capitalize()} • ${project.numColors} colors"
                tvStatus.text = project.status.capitalize()

                // Load thumbnail
                ivThumbnail.load(project.originalImageUrl) {
                    crossfade(true)
                    placeholder(R.drawable.placeholder_image)
                    error(R.drawable.error_image)
                }

                root.setOnClickListener {
                    onProjectClick(project)
                }

                btnDelete.setOnClickListener {
                    onDeleteClick(project)
                }
            }
        }
    }

    private class ProjectDiffCallback : DiffUtil.ItemCallback<ColoringProject>() {
        override fun areItemsTheSame(oldItem: ColoringProject, newItem: ColoringProject) =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: ColoringProject, newItem: ColoringProject) =
            oldItem == newItem
    }
}
