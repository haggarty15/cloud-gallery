package com.cloudgallery.portfolio.ui.coloring

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.cloudgallery.portfolio.data.models.*
import com.cloudgallery.portfolio.data.repository.ColoringRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * ViewModel for ColoringActivity
 */
@HiltViewModel
class ColoringViewModel @Inject constructor(
    private val repository: ColoringRepository
) : ViewModel() {

    private val _project = MutableLiveData<ColoringProject?>()
    val project: LiveData<ColoringProject?> = _project

    private val _canvasData = MutableLiveData<CanvasData?>()
    val canvasData: LiveData<CanvasData?> = _canvasData

    private val _session = MutableLiveData<ColoringSession?>()
    val session: LiveData<ColoringSession?> = _session

    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    private val _saveSuccess = MutableLiveData<Boolean>()
    val saveSuccess: LiveData<Boolean> = _saveSuccess

    private val _completedSuccess = MutableLiveData<Boolean>()
    val completedSuccess: LiveData<Boolean> = _completedSuccess

    private val _selectedColor = MutableLiveData<Int>()
    val selectedColor: LiveData<Int> = _selectedColor

    private var currentProjectId: String? = null
    private var currentSessionId: String? = null
    private val actionHistory = mutableListOf<Map<String, Int>>()

    fun loadProject(projectId: String) {
        currentProjectId = projectId
        _loading.value = true

        viewModelScope.launch {
            try {
                // Load project details
                val projectResult = repository.getProject(projectId)
                if (projectResult.isSuccess) {
                    val project = projectResult.getOrNull()
                    _project.value = project
                    _canvasData.value = project?.templateData

                    // Load or create session
                    loadOrCreateSession(projectId)
                } else {
                    _error.value = projectResult.exceptionOrNull()?.message ?: "Failed to load project"
                }
            } catch (e: Exception) {
                _error.value = e.message ?: "Unknown error"
            } finally {
                _loading.value = false
            }
        }
    }

    private suspend fun loadOrCreateSession(projectId: String) {
        try {
            val sessionResult = repository.getOrCreateSession(projectId)
            if (sessionResult.isSuccess) {
                val session = sessionResult.getOrNull()
                _session.value = session
                currentSessionId = session?.id
            }
        } catch (e: Exception) {
            _error.value = "Failed to load session: ${e.message}"
        }
    }

    fun selectColor(colorNum: Int) {
        _selectedColor.value = colorNum
    }

    fun fillRegion(regionId: String, currentFilledRegions: Map<String, Int>) {
        // Save current state for undo
        actionHistory.add(currentFilledRegions.toMap())
        if (actionHistory.size > 50) {
            actionHistory.removeAt(0) // Keep last 50 actions
        }
    }

    fun undo() {
        if (actionHistory.isNotEmpty()) {
            val previousState = actionHistory.removeAt(actionHistory.lastIndex)
            // Restore previous state - handled by Activity calling canvas.loadSession()
            _session.value = _session.value?.copy(filledRegions = previousState)
        }
    }

    fun clearProgress() {
        actionHistory.clear()
    }

    fun saveProgress(filledRegions: Map<String, Int>) {
        val sessionId = currentSessionId ?: return
        _loading.value = true

        viewModelScope.launch {
            try {
                val completionPercent = calculateCompletionPercent(filledRegions)
                val request = SaveSessionRequest(filledRegions, completionPercent)
                
                val result = repository.saveSession(sessionId, request)
                if (result.isSuccess) {
                    _saveSuccess.value = true
                    _session.value = _session.value?.copy(
                        filledRegions = filledRegions,
                        completionPercent = completionPercent
                    )
                } else {
                    _error.value = "Failed to save progress"
                }
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _loading.value = false
            }
        }
    }

    fun autoSave(filledRegions: Map<String, Int>) {
        // Silent auto-save (no loading indicator)
        val sessionId = currentSessionId ?: return

        viewModelScope.launch {
            try {
                val completionPercent = calculateCompletionPercent(filledRegions)
                val request = SaveSessionRequest(filledRegions, completionPercent)
                repository.saveSession(sessionId, request)
            } catch (e: Exception) {
                // Silently fail for auto-save
            }
        }
    }

    fun completeProject(filledRegions: Map<String, Int>) {
        val sessionId = currentSessionId ?: return
        _loading.value = true

        viewModelScope.launch {
            try {
                // First save current progress
                val completionPercent = calculateCompletionPercent(filledRegions)
                repository.saveSession(
                    sessionId,
                    SaveSessionRequest(filledRegions, completionPercent)
                )

                // Then mark as complete
                val request = CompleteProjectRequest(sessionId)
                val result = repository.completeProject(request)
                
                if (result.isSuccess) {
                    _completedSuccess.value = true
                } else {
                    _error.value = "Failed to complete project"
                }
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _loading.value = false
            }
        }
    }

    private fun calculateCompletionPercent(filledRegions: Map<String, Int>): Int {
        val totalRegions = _canvasData.value?.regions?.size ?: return 0
        return if (totalRegions > 0) {
            (filledRegions.size * 100) / totalRegions
        } else 0
    }
}
