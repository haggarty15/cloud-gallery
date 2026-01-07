package com.cloudgallery.portfolio.data.repository

import com.cloudgallery.portfolio.data.api.ApiService
import com.cloudgallery.portfolio.data.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MultipartBody
import okhttp3.RequestBody
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository for Coloring Projects and Sessions
 */
@Singleton
class ColoringRepository @Inject constructor(
    private val apiService: ApiService
) {

    /**
     * Create a new coloring project by uploading a photo
     */
    suspend fun createProject(
        imageFile: MultipartBody.Part,
        title: RequestBody,
        numColors: RequestBody,
        difficulty: RequestBody
    ): Result<CreateProjectResponse> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.createColoringProject(imageFile, title, numColors, difficulty)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to create project: ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get project details with canvas data
     */
    suspend fun getProject(projectId: String): Result<ColoringProject> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getColoringProject(projectId)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to load project"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get user's coloring projects
     */
    suspend fun getUserProjects(page: Int = 1, limit: Int = 20): Result<ProjectListResponse> = 
        withContext(Dispatchers.IO) {
            try {
                val response = apiService.getUserProjects(page, limit)
                if (response.isSuccessful && response.body() != null) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Failed to load projects"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    /**
     * Get or create a coloring session for a project
     */
    suspend fun getOrCreateSession(projectId: String): Result<ColoringSession> = 
        withContext(Dispatchers.IO) {
            try {
                val response = apiService.getOrCreateSession(projectId)
                if (response.isSuccessful && response.body() != null) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Failed to load session"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    /**
     * Save coloring progress
     */
    suspend fun saveSession(
        sessionId: String,
        request: SaveSessionRequest
    ): Result<ColoringSession> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.saveColoringSession(sessionId, request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to save session"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Mark project as completed
     */
    suspend fun completeProject(request: CompleteProjectRequest): Result<ColoringSession> = 
        withContext(Dispatchers.IO) {
            try {
                val response = apiService.completeColoringProject(request)
                if (response.isSuccessful && response.body() != null) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Failed to complete project"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    /**
     * Get user's completed colorings
     */
    suspend fun getCompletedColorings(page: Int = 1, limit: Int = 20): Result<SessionListResponse> = 
        withContext(Dispatchers.IO) {
            try {
                val response = apiService.getCompletedColorings(page, limit)
                if (response.isSuccessful && response.body() != null) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Failed to load completed colorings"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    /**
     * Delete a coloring project
     */
    suspend fun deleteProject(projectId: String): Result<Boolean> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.deleteColoringProject(projectId)
            Result.success(response.isSuccessful)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
