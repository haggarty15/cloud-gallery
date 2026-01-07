package com.cloudgallery.portfolio.ui.coloring

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.cloudgallery.portfolio.databinding.ActivityColoringBinding
import com.cloudgallery.portfolio.data.models.ColorInfo
import dagger.hilt.android.AndroidEntryPoint

/**
 * Coloring Activity - Main interactive coloring screen
 * 
 * Features:
 * - Interactive canvas for tap-to-fill coloring
 * - Color picker bar at bottom
 * - Progress indicator
 * - Undo/Save/Complete actions
 */
@AndroidEntryPoint
class ColoringActivity : AppCompatActivity() {

    private lateinit var binding: ActivityColoringBinding
    private val viewModel: ColoringViewModel by viewModels()
    private lateinit var colorPickerAdapter: ColorPickerAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityColoringBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val projectId = intent.getStringExtra(EXTRA_PROJECT_ID) ?: run {
            Toast.makeText(this, "Invalid project", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        setupUI()
        setupColorPicker()
        observeViewModel()
        
        viewModel.loadProject(projectId)
    }

    private fun setupUI() {
        // Setup toolbar
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            setDisplayShowHomeEnabled(true)
        }

        // Setup canvas listeners
        binding.coloringCanvas.onRegionTappedListener = { region ->
            viewModel.fillRegion(region.id, binding.coloringCanvas.getFilledRegions())
        }

        binding.coloringCanvas.onProgressChanged = { progress ->
            binding.progressBar.progress = progress
            binding.tvProgress.text = "$progress% Complete"
        }

        // Setup action buttons
        binding.btnUndo.setOnClickListener {
            viewModel.undo()
        }

        binding.btnClear.setOnClickListener {
            showClearConfirmation()
        }

        binding.btnSave.setOnClickListener {
            viewModel.saveProgress(binding.coloringCanvas.getFilledRegions())
        }

        binding.btnComplete.setOnClickListener {
            viewModel.completeProject(binding.coloringCanvas.getFilledRegions())
        }

        binding.btnZoomIn.setOnClickListener {
            // Zoom handled by canvas gestures
            Toast.makeText(this, "Pinch to zoom", Toast.LENGTH_SHORT).show()
        }

        binding.btnZoomOut.setOnClickListener {
            // Double tap to reset zoom
            Toast.makeText(this, "Double tap to reset zoom", Toast.LENGTH_SHORT).show()
        }
    }

    private fun setupColorPicker() {
        colorPickerAdapter = ColorPickerAdapter { colorInfo ->
            binding.coloringCanvas.setSelectedColor(colorInfo.num)
            viewModel.selectColor(colorInfo.num)
        }

        binding.rvColorPicker.apply {
            layoutManager = LinearLayoutManager(
                this@ColoringActivity,
                LinearLayoutManager.HORIZONTAL,
                false
            )
            adapter = colorPickerAdapter
        }
    }

    private fun observeViewModel() {
        viewModel.project.observe(this) { project ->
            if (project != null) {
                binding.toolbar.title = project.title ?: "Coloring"
                binding.tvDifficulty.text = "Difficulty: ${project.difficulty.capitalize()}"
                binding.tvColors.text = "${project.numColors} colors"
            }
        }

        viewModel.canvasData.observe(this) { canvasData ->
            if (canvasData != null) {
                binding.coloringCanvas.setCanvasData(canvasData)
                colorPickerAdapter.submitList(canvasData.colors)
                
                // Select first color by default
                if (canvasData.colors.isNotEmpty()) {
                    binding.coloringCanvas.setSelectedColor(canvasData.colors.first().num)
                }
            }
        }

        viewModel.session.observe(this) { session ->
            if (session != null) {
                // Load saved progress
                binding.coloringCanvas.loadSession(session.filledRegions)
                binding.progressBar.progress = session.completionPercent
                binding.tvProgress.text = "${session.completionPercent}% Complete"
            }
        }

        viewModel.loading.observe(this) { isLoading ->
            binding.progressLoading.visibility = if (isLoading) View.VISIBLE else View.GONE
            binding.coloringCanvas.isEnabled = !isLoading
        }

        viewModel.error.observe(this) { error ->
            error?.let {
                Toast.makeText(this, it, Toast.LENGTH_LONG).show()
            }
        }

        viewModel.saveSuccess.observe(this) { success ->
            if (success) {
                Toast.makeText(this, "Progress saved!", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.completedSuccess.observe(this) { success ->
            if (success) {
                Toast.makeText(this, "Project completed! 🎉", Toast.LENGTH_LONG).show()
                // TODO: Navigate to gallery or show completion dialog
                finish()
            }
        }

        viewModel.selectedColor.observe(this) { colorNum ->
            colorPickerAdapter.setSelectedColor(colorNum)
        }
    }

    private fun showClearConfirmation() {
        androidx.appcompat.app.AlertDialog.Builder(this)
            .setTitle("Clear Canvas")
            .setMessage("Are you sure you want to clear all your progress?")
            .setPositiveButton("Clear") { _, _ ->
                binding.coloringCanvas.clearCanvas()
                viewModel.clearProgress()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }

    override fun onPause() {
        super.onPause()
        // Auto-save on pause
        viewModel.autoSave(binding.coloringCanvas.getFilledRegions())
    }

    companion object {
        const val EXTRA_PROJECT_ID = "project_id"
    }
}
