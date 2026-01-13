# Image Segmentation Improvements

## Summary of Changes (January 9, 2026)

### Problem
- Too many segments (too dense)
- Segments too small for users to tap on mobile
- Need cartoonish effect to better group objects

### Solution Implemented

#### 1. Enhanced Cartoon Preprocessing Filter
**File**: `backend/app/stylized_processor.py`

**Improvements**:
- **Multiple bilateral filter passes**: 2 iterations with optimized parameters (d=9, sigmaColor=75, sigmaSpace=75)
- **Posterization**: Reduces colors to 6 levels per channel for blocky cartoon effect
- **Median blur**: Smooths out small variations
- **Performance optimization**: Downscales large images (>1200px) during processing, then upscales result
- **Removed slow mean shift filtering**: Replaced with faster bilateral + posterization combo

**Effect**: Creates larger, more uniform color regions perfect for segmentation

#### 2. Increased Minimum Region Size
**Files**: `backend/app/canvas_processor.py`, `backend/app/coloring_routes.py`

**Changes**:
- Default `min_region_size`: **50 → 200 pixels**
- Regions smaller than 200px are merged with neighbors
- Better UX for mobile tapping (larger touch targets)

#### 3. More Aggressive Region Simplification
**File**: `backend/app/canvas_processor.py` - `_simplify_labels()` method

**Improvements**:
- Larger morphological kernel size: `sqrt(min_region_size)` instead of `sqrt(min_region_size)/2`
- **2 iterations** of morphological operations (closing + opening)
- Pre-processing with median blur before morphological operations
- Better merging of small fragmented regions

#### 4. Reduced Default Color Count
**Files**: `backend/app/canvas_processor.py`, `backend/app/coloring_routes.py`

**Changes**:
- Default `num_colors`: **20 → 15**
- Fewer colors = fewer segments = easier coloring experience
- Difficulty range: **8-50** (was 10-50)

#### 5. Automatic Cartoon Preprocessing in API
**File**: `backend/app/coloring_routes.py` - `process_image_async()` function

**New Pipeline**:
1. Upload original photo
2. **Apply cartoon filter** (new step!)
3. Run segmentation on cartoonified image
4. Generate interactive canvas
5. Save and upload results

This ensures all uploaded photos get the benefit of cartoon preprocessing automatically.

## Testing

### Test Script
Created `backend/test_improved_segmentation.py` for testing improvements:

```bash
# Activate venv
cd E:\git\cloud-gallery\backend
.\.venv\Scripts\Activate.ps1

# Test with defaults (15 colors, 200px min region)
python test_improved_segmentation.py ../test-photos/boba.jpg

# Test with custom parameters
python test_improved_segmentation.py ../test-photos/boba.jpg 12 300
python test_improved_segmentation.py ../test-photos/ldn.jpg 10 250
```

### Expected Results
- **Fewer total regions**: 30-60% reduction compared to before
- **Larger average region size**: 3-4x larger
- **No regions smaller than min_region_size**: Better mobile UX
- **Cartoon-like appearance**: Clearer boundaries, uniform colors
- **Processing time**: ~5-10 seconds (optimized from potentially 30+ seconds)

## Performance Optimizations

### Before
- Direct segmentation on photos
- No preprocessing
- Slow mean shift filtering
- Small regions everywhere

### After  
- Cartoon preprocessing creates cleaner input
- Optimized bilateral filtering (2 passes vs 3)
- Automatic downscaling for large images
- Aggressive region merging (200px minimum)
- **Result**: Faster processing + better UX

## API Usage

When creating a project via API:

```bash
POST /api/projects/create
Content-Type: multipart/form-data

{
  "file": <image file>,
  "title": "My Photo",
  "num_colors": 15,        # Optional, default 15 (was 20)
  "difficulty": "medium"
}
```

Backend now automatically:
1. Applies cartoon filter
2. Uses min_region_size=200 (configurable via `MIN_REGION_SIZE` env var)
3. Generates larger, more tap-friendly regions

## Configuration

Environment variables in `.env`:
```bash
MIN_REGION_SIZE=200      # Minimum pixels per region (default 200)
MAX_CANVAS_SIZE=800      # Maximum canvas dimension
```

## Benefits

### User Experience
✅ Larger tap targets on mobile  
✅ Fewer overwhelming segments  
✅ Clear, cartoon-like boundaries  
✅ More enjoyable coloring experience

### Technical
✅ Faster processing (optimized algorithms)  
✅ Better color grouping  
✅ Automatic preprocessing pipeline  
✅ Configurable parameters

## Files Modified

1. `backend/app/stylized_processor.py` - Enhanced cartoon filter
2. `backend/app/canvas_processor.py` - Increased min_region_size, improved simplification
3. `backend/app/coloring_routes.py` - Added automatic cartoon preprocessing
4. `backend/test_improved_segmentation.py` - Created test script

## Next Steps

1. Test on real photos with Android app
2. Fine-tune parameters based on user feedback
3. Consider adding difficulty-based auto-tuning:
   - Easy: 10 colors, 300px regions
   - Medium: 15 colors, 200px regions
   - Hard: 25 colors, 150px regions
4. Add option to skip cartoon preprocessing for artistic photos

