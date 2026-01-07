package com.cloudgallery.portfolio.ui.gallery

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.cloudgallery.portfolio.data.models.ColoringProject
import com.cloudgallery.portfolio.data.models.ColoringSession
import com.cloudgallery.portfolio.data.repository.ColoringRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class GalleryViewModel @Inject constructor(
    private val repository: ColoringRepository
) : ViewModel() {

    private val _projects = MutableLiveData<List<ColoringProject>>()
    val projects: LiveData<List<ColoringProject>> = _projects

    private val _completedColorings = MutableLiveData<List<ColoringSession>>()
    val completedColorings: LiveData<List<ColoringSession>> = _completedColorings

    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    fun loadProjects() {
        _loading.value = true
        viewModelScope.launch {
            try {
                val result = repository.getUserProjects()
                if (result.isSuccess) {
                    _projects.value = result.getOrNull()?.projects ?: emptyList()
                } else {
                    _error.value = "Failed to load projects"
                }
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _loading.value = false
            }
        }
    }

    fun loadCompletedColorings() {
        viewModelScope.launch {
            try {
                val result = repository.getCompletedColorings()
                if (result.isSuccess) {
                    _completedColorings.value = result.getOrNull()?.sessions ?: emptyList()
                }
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }

    fun deleteProject(projectId: String) {
        viewModelScope.launch {
            try {
                val result = repository.deleteProject(projectId)
                if (result.isSuccess) {
                    loadProjects() // Refresh list
                } else {
                    _error.value = "Failed to delete project"
                }
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }
}
