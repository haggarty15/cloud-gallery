package com.cloudgallery.portfolio.data.api

import com.cloudgallery.portfolio.data.models.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit API service interface
 */
interface ApiService {
    
    // ============ Legacy Image Gallery Endpoints ============
    
    @Multipart
    @POST("api/upload")
    suspend fun uploadImage(
        @Part file: MultipartBody.Part,
        @Part("title") title: RequestBody?,
        @Part("description") description: RequestBody?
    ): Response<UploadResponse>
    
    @GET("api/uploads")
    suspend fun getUserUploads(
        @Query("status") status: String?,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<ImageListResponse>
    
    @DELETE("api/images/{imageId}")
    suspend fun deleteImage(
        @Path("imageId") imageId: String
    ): Response<Map<String, Any>>
    
    @GET("api/gallery")
    suspend fun getGallery(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20,
        @Query("sort") sort: String = "newest"
    ): Response<ImageListResponse>
    
    // ============ Coloring App Endpoints ============
    
    /**
     * Create a new coloring project by uploading a photo
     * Returns project ID and processing status
     */
    @Multipart
    @POST("api/projects/create")
    suspend fun createColoringProject(
        @Part file: MultipartBody.Part,
        @Part("title") title: RequestBody,
        @Part("num_colors") numColors: RequestBody,
        @Part("difficulty") difficulty: RequestBody
    ): Response<CreateProjectResponse>
    
    /**
     * Get coloring project details with canvas data
     */
    @GET("api/projects/{projectId}")
    suspend fun getColoringProject(
        @Path("projectId") projectId: String
    ): Response<ColoringProject>
    
    /**
     * Get user's coloring projects
     */
    @GET("api/projects")
    suspend fun getUserProjects(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<ProjectListResponse>
    
    /**
     * Get or create a coloring session for a project
     */
    @POST("api/coloring/session/{projectId}")
    suspend fun getOrCreateSession(
        @Path("projectId") projectId: String
    ): Response<ColoringSession>
    
    /**
     * Save coloring progress (auto-save)
     */
    @PUT("api/coloring/session/{sessionId}")
    suspend fun saveColoringSession(
        @Path("sessionId") sessionId: String,
        @Body request: SaveSessionRequest
    ): Response<ColoringSession>
    
    /**
     * Mark project as completed and generate final colored image
     */
    @POST("api/coloring/complete")
    suspend fun completeColoringProject(
        @Body request: CompleteProjectRequest
    ): Response<ColoringSession>
    
    /**
     * Get user's completed colorings (gallery)
     */
    @GET("api/coloring/completed")
    suspend fun getCompletedColorings(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<SessionListResponse>
    
    /**
     * Delete a coloring project
     */
    @DELETE("api/projects/{projectId}")
    suspend fun deleteColoringProject(
        @Path("projectId") projectId: String
    ): Response<Map<String, Any>>
}
