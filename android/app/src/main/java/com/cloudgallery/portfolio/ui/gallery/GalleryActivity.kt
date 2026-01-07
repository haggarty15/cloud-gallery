package com.cloudgallery.portfolio.ui.gallery

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import com.cloudgallery.portfolio.databinding.ActivityGalleryBinding
import com.cloudgallery.portfolio.ui.coloring.ColoringActivity
import dagger.hilt.android.AndroidEntryPoint

/**
 * Gallery Activity - Display user's coloring projects and completed works
 */
@AndroidEntryPoint
class GalleryActivity : AppCompatActivity() {

    private lateinit var binding: ActivityGalleryBinding
    private val viewModel: GalleryViewModel by viewModels()
    private lateinit var projectsAdapter: ProjectsAdapter
    private lateinit var completedAdapter: CompletedColoringsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityGalleryBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupToolbar()
        setupProjects()
        setupCompleted()
        observeViewModel()

        viewModel.loadProjects()
        viewModel.loadCompletedColorings()
    }

    private fun setupToolbar() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            title = "My Coloring Gallery"
        }
    }

    private fun setupProjects() {
        projectsAdapter = ProjectsAdapter(
            onProjectClick = { project ->
                val intent = Intent(this, ColoringActivity::class.java).apply {
                    putExtra(ColoringActivity.EXTRA_PROJECT_ID, project.id)
                }
                startActivity(intent)
            },
            onDeleteClick = { project ->
                showDeleteConfirmation(project.id, project.title ?: "this project")
            }
        )

        binding.rvProjects.apply {
            layoutManager = GridLayoutManager(this@GalleryActivity, 2)
            adapter = projectsAdapter
        }
    }

    private fun setupCompleted() {
        completedAdapter = CompletedColoringsAdapter(
            onColoringClick = { session ->
                // TODO: Show completed coloring detail/share dialog
                Toast.makeText(this, "Completed: ${session.completionPercent}%", Toast.LENGTH_SHORT).show()
            }
        )

        binding.rvCompleted.apply {
            layoutManager = GridLayoutManager(this@GalleryActivity, 2)
            adapter = completedAdapter
        }
    }

    private fun observeViewModel() {
        viewModel.projects.observe(this) { projects ->
            projectsAdapter.submitList(projects)
            binding.tvNoProjects.visibility = if (projects.isEmpty()) View.VISIBLE else View.GONE
        }

        viewModel.completedColorings.observe(this) { completed ->
            completedAdapter.submitList(completed)
            binding.tvNoCompleted.visibility = if (completed.isEmpty()) View.VISIBLE else View.GONE
        }

        viewModel.loading.observe(this) { isLoading ->
            binding.progressLoading.visibility = if (isLoading) View.VISIBLE else View.GONE
        }

        viewModel.error.observe(this) { error ->
            error?.let {
                Toast.makeText(this, it, Toast.LENGTH_LONG).show()
            }
        }

        // Tab switching
        binding.chipProjects.setOnClickListener {
            binding.rvProjects.visibility = View.VISIBLE
            binding.rvCompleted.visibility = View.GONE
            binding.tvNoProjects.visibility = if (projectsAdapter.itemCount == 0) View.VISIBLE else View.GONE
            binding.tvNoCompleted.visibility = View.GONE
        }

        binding.chipCompleted.setOnClickListener {
            binding.rvProjects.visibility = View.GONE
            binding.rvCompleted.visibility = View.VISIBLE
            binding.tvNoProjects.visibility = View.GONE
            binding.tvNoCompleted.visibility = if (completedAdapter.itemCount == 0) View.VISIBLE else View.GONE
        }
    }

    private fun showDeleteConfirmation(projectId: String, title: String) {
        androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("Delete Project")
            .setMessage("Are you sure you want to delete \"$title\"?")
            .setPositiveButton("Delete") { _, _ ->
                viewModel.deleteProject(projectId)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }

    override fun onResume() {
        super.onResume()
        // Refresh when returning from coloring activity
        viewModel.loadProjects()
        viewModel.loadCompletedColorings()
    }
}
