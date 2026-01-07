package com.cloudgallery.portfolio.ui.coloring

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import androidx.core.content.ContextCompat
import com.cloudgallery.portfolio.R
import com.cloudgallery.portfolio.data.models.CanvasData
import com.cloudgallery.portfolio.data.models.ColorInfo
import com.cloudgallery.portfolio.data.models.Region
import kotlin.math.max
import kotlin.math.min

/**
 * Interactive Coloring Canvas - Tap to fill regions with colors
 * 
 * Features:
 * - Tap detection on regions
 * - Zoom and pan gestures
 * - Color filling animation
 * - Progress tracking
 */
class ColoringCanvasView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    // Canvas data
    private var canvasData: CanvasData? = null
    private var selectedColorNum: Int = 1
    private val filledRegions = mutableMapOf<String, Int>()

    // Paint objects
    private val regionPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
    }
    private val borderPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 1f
        color = Color.GRAY
    }
    private val textPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.BLACK
        textAlign = Paint.Align.CENTER
        textSize = 24f
    }
    private val highlightPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 4f
        color = Color.YELLOW
    }

    // Transform for zoom/pan
    private val matrix = Matrix()
    private val inverseMatrix = Matrix()
    private var scaleFactor = 1f
    private var translateX = 0f
    private var translateY = 0f
    private var lastTouchX = 0f
    private var lastTouchY = 0f

    // Gesture detectors
    private val scaleDetector = ScaleGestureDetector(context, ScaleListener())
    private val gestureDetector = GestureDetector(context, GestureListener())

    // Listeners
    var onRegionTappedListener: ((Region) -> Unit)? = null
    var onProgressChanged: ((Int) -> Unit)? = null

    // Cached paths for regions
    private val regionPaths = mutableMapOf<String, Path>()
    private val regionBounds = mutableMapOf<String, RectF>()

    fun setCanvasData(data: CanvasData) {
        canvasData = data
        buildRegionPaths()
        fitCanvasToView()
        invalidate()
    }

    fun setSelectedColor(colorNum: Int) {
        selectedColorNum = colorNum
        invalidate()
    }

    fun fillRegion(regionId: String, colorNum: Int) {
        filledRegions[regionId] = colorNum
        updateProgress()
        invalidate()
    }

    fun getFilledRegions(): Map<String, Int> = filledRegions.toMap()

    fun clearCanvas() {
        filledRegions.clear()
        updateProgress()
        invalidate()
    }

    fun loadSession(filled: Map<String, Int>) {
        filledRegions.clear()
        filledRegions.putAll(filled)
        updateProgress()
        invalidate()
    }

    private fun buildRegionPaths() {
        val data = canvasData ?: return
        regionPaths.clear()
        regionBounds.clear()

        data.regions.forEach { region ->
            if (region.boundary.isNotEmpty()) {
                val path = Path()
                val bounds = RectF()

                // Create path from boundary points
                val firstPoint = region.boundary.first()
                path.moveTo(firstPoint.x, firstPoint.y)

                region.boundary.drop(1).forEach { point ->
                    path.lineTo(point.x, point.y)
                }
                path.close()

                // Calculate bounds
                path.computeBounds(bounds, true)

                regionPaths[region.id] = path
                regionBounds[region.id] = bounds
            }
        }
    }

    private fun fitCanvasToView() {
        val data = canvasData ?: return
        if (width == 0 || height == 0) return

        val canvasWidth = data.dimensions.width.toFloat()
        val canvasHeight = data.dimensions.height.toFloat()

        val scaleX = width / canvasWidth
        val scaleY = height / canvasHeight
        scaleFactor = min(scaleX, scaleY) * 0.9f // 90% to add padding

        // Center the canvas
        translateX = (width - canvasWidth * scaleFactor) / 2f
        translateY = (height - canvasHeight * scaleFactor) / 2f

        updateMatrix()
    }

    private fun updateMatrix() {
        matrix.reset()
        matrix.postScale(scaleFactor, scaleFactor)
        matrix.postTranslate(translateX, translateY)
        matrix.invert(inverseMatrix)
        invalidate()
    }

    private fun updateProgress() {
        val data = canvasData ?: return
        val totalRegions = data.regions.size
        val filled = filledRegions.size
        val progress = if (totalRegions > 0) {
            (filled * 100) / totalRegions
        } else 0
        
        onProgressChanged?.invoke(progress)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val data = canvasData ?: return

        canvas.save()
        canvas.concat(matrix)

        // Draw all regions
        data.regions.forEach { region ->
            val path = regionPaths[region.id] ?: return@forEach
            val colorNum = filledRegions[region.id] ?: region.colorNum

            // Get color for this region
            val colorInfo = data.colors.find { it.num == colorNum }
            val fillColor = if (filledRegions.containsKey(region.id)) {
                // User filled - use actual color
                colorInfo?.toAndroidColor() ?: Color.WHITE
            } else {
                // Unfilled - use light gray
                Color.parseColor("#F5F5F5")
            }

            // Fill region
            regionPaint.color = fillColor
            canvas.drawPath(path, regionPaint)

            // Draw border
            canvas.drawPath(path, borderPaint)

            // Draw number if not filled
            if (!filledRegions.containsKey(region.id)) {
                canvas.drawText(
                    region.colorNum.toString(),
                    region.centroid.x,
                    region.centroid.y + textPaint.textSize / 3,
                    textPaint
                )
            }
        }

        canvas.restore()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        var handled = scaleDetector.onTouchEvent(event)
        handled = gestureDetector.onTouchEvent(event) || handled

        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                lastTouchX = event.x
                lastTouchY = event.y
            }
            MotionEvent.ACTION_MOVE -> {
                if (!scaleDetector.isInProgress && event.pointerCount == 1) {
                    val dx = event.x - lastTouchX
                    val dy = event.y - lastTouchY
                    translateX += dx
                    translateY += dy
                    lastTouchX = event.x
                    lastTouchY = event.y
                    updateMatrix()
                }
            }
        }

        return handled || super.onTouchEvent(event)
    }

    private fun handleTap(x: Float, y: Float) {
        val data = canvasData ?: return

        // Transform touch coordinates to canvas coordinates
        val points = floatArrayOf(x, y)
        inverseMatrix.mapPoints(points)
        val canvasX = points[0]
        val canvasY = points[1]

        // Find tapped region
        data.regions.find { region ->
            val path = regionPaths[region.id] ?: return@find false
            val bounds = regionBounds[region.id] ?: return@find false

            // Quick bounds check first
            if (!bounds.contains(canvasX, canvasY)) return@find false

            // Detailed path check
            val pathRegion = android.graphics.Region()
            val clip = android.graphics.Region(
                bounds.left.toInt(),
                bounds.top.toInt(),
                bounds.right.toInt(),
                bounds.bottom.toInt()
            )
            pathRegion.setPath(path, clip)
            pathRegion.contains(canvasX.toInt(), canvasY.toInt())
        }?.let { tappedRegion ->
            // Region tapped - fill it with selected color
            filledRegions[tappedRegion.id] = selectedColorNum
            updateProgress()
            invalidate()
            onRegionTappedListener?.invoke(tappedRegion)
        }
    }

    private inner class ScaleListener : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScale(detector: ScaleGestureDetector): Boolean {
            scaleFactor *= detector.scaleFactor
            scaleFactor = max(0.5f, min(scaleFactor, 5.0f)) // Limit zoom 0.5x to 5x

            // Adjust translation to zoom towards focal point
            val focusX = detector.focusX
            val focusY = detector.focusY
            translateX = focusX - (focusX - translateX) * detector.scaleFactor
            translateY = focusY - (focusY - translateY) * detector.scaleFactor

            updateMatrix()
            return true
        }
    }

    private inner class GestureListener : GestureDetector.SimpleOnGestureListener() {
        override fun onSingleTapConfirmed(e: MotionEvent): Boolean {
            handleTap(e.x, e.y)
            return true
        }

        override fun onDoubleTap(e: MotionEvent): Boolean {
            // Reset zoom on double tap
            fitCanvasToView()
            return true
        }
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        if (canvasData != null) {
            fitCanvasToView()
        }
    }
}
