package com.cloudgallery.portfolio.data.models

import com.google.gson.annotations.SerializedName

/**
 * Coloring Project - A photo converted to paint-by-numbers template
 */
data class ColoringProject(
    val id: String,
    @SerializedName("user_id")
    val userId: String,
    val title: String?,
    @SerializedName("original_image_url")
    val originalImageUrl: String,
    @SerializedName("template_data")
    val templateData: CanvasData?,
    @SerializedName("color_palette")
    val colorPalette: List<ColorInfo>,
    val difficulty: String, // easy, medium, hard
    @SerializedName("num_colors")
    val numColors: Int,
    val status: String, // processing, completed, failed
    @SerializedName("created_at")
    val createdAt: String,
    @SerializedName("updated_at")
    val updatedAt: String?
)

/**
 * Canvas Data - Region boundaries and color mappings for interactive coloring
 */
data class CanvasData(
    val regions: List<Region>,
    val colors: List<ColorInfo>,
    val dimensions: Dimensions
)

/**
 * Region - A clickable area in the coloring canvas
 */
data class Region(
    val id: String,
    @SerializedName("color_num")
    val colorNum: Int,
    val boundary: List<Point>,
    val centroid: Point,
    var filled: Boolean = false,
    @SerializedName("filled_color")
    var filledColor: Int? = null // User's chosen color
)

/**
 * Point - Coordinate in the canvas
 */
data class Point(
    val x: Float,
    val y: Float
)

/**
 * Color Info - Color palette entry
 */
data class ColorInfo(
    val num: Int,
    val rgb: List<Int>,
    val hex: String
) {
    fun toAndroidColor(): Int {
        return android.graphics.Color.rgb(rgb[0], rgb[1], rgb[2])
    }
}

/**
 * Canvas Dimensions
 */
data class Dimensions(
    val width: Int,
    val height: Int
)

/**
 * Coloring Session - User's progress on a project
 */
data class ColoringSession(
    val id: String,
    @SerializedName("project_id")
    val projectId: String,
    @SerializedName("user_id")
    val userId: String,
    @SerializedName("filled_regions")
    val filledRegions: Map<String, Int>, // regionId -> colorNum
    @SerializedName("completion_percent")
    val completionPercent: Int,
    @SerializedName("colored_image_url")
    val coloredImageUrl: String?,
    @SerializedName("is_completed")
    val isCompleted: Boolean,
    @SerializedName("started_at")
    val startedAt: String,
    @SerializedName("updated_at")
    val updatedAt: String?,
    @SerializedName("completed_at")
    val completedAt: String?
)

/**
 * Request/Response models
 */
data class CreateProjectRequest(
    val title: String?,
    @SerializedName("num_colors")
    val numColors: Int,
    val difficulty: String
)

data class CreateProjectResponse(
    val success: Boolean,
    @SerializedName("project_id")
    val projectId: String?,
    val status: String?,
    val message: String?
)

data class FillRegionRequest(
    @SerializedName("region_id")
    val regionId: String,
    @SerializedName("color_num")
    val colorNum: Int
)

data class SaveSessionRequest(
    @SerializedName("filled_regions")
    val filledRegions: Map<String, Int>,
    @SerializedName("completion_percent")
    val completionPercent: Int
)

data class CompleteProjectRequest(
    @SerializedName("session_id")
    val sessionId: String
)

data class ProjectListResponse(
    val projects: List<ColoringProject>,
    val pagination: Pagination
)

data class SessionListResponse(
    val sessions: List<ColoringSession>,
    val pagination: Pagination
)
