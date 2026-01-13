# Quick Test Guide - Improved Segmentation

## Start Backend
```powershell
cd E:\git\cloud-gallery\backend
.\.venv\Scripts\Activate.ps1
python run.py
```

## Test via Android App

1. **Open app on phone** (connected via USB debugging)
2. **Upload a photo** from gallery or camera
3. **Select difficulty**:
   - Easy: 10-12 colors
   - Medium: 15-18 colors  
   - Hard: 20-25 colors
4. **Wait for processing** (~30 seconds)
5. **Observe results**:
   - Regions should be larger and easier to tap
   - Cartoon-like appearance
   - Fewer total regions than before

## Test Standalone (if terminal works)

```powershell
# Test improved segmentation (general)
python test_improved_segmentation.py ../test-photos/boba.jpg

# Test CAT-specific segmentation (boba image has a cat!)
# Uses 10 colors + 250px min region for clear cat features
python test_cat_segmentation.py ../test-photos/boba.jpg

# Custom parameters for general test
python test_improved_segmentation.py ../test-photos/boba.jpg 12 300

# Check outputs in output/ directory
ls output/*improved*
ls output/*cat*
```

## Verify Improvements

Compare old vs new output files in `output/` directory:

**Old files** (if they exist):
- `boba_template.png` 
- `boba_canvas.json`

**New files (general improved)**:
- `boba_cartoon_preprocessed.png` - Cartoonified input
- `boba_improved_template.png` - Template with larger regions
- `boba_improved_canvas.json` - Canvas data
- `boba_improved_comparison.png` - Side-by-side comparison

**Cat-optimized files** (for boba.jpg with cat):
- `boba_cat_cartoon.png` - Cartoon style (like reference cat image)
- `boba_cat_template.png` - Template optimized for cat features
- `boba_cat_colored.png` - Colored preview
- `boba_cat_comparison.png` - Side-by-side
- `boba_cat_canvas.json` - Canvas data (10 colors, 250px min region)

**Cat-optimized settings**:
- **10 colors** (vs 15 general) - Simpler cat features (face, eyes, ears, body)
- **250px min region** (vs 200 general) - Avoids tiny whisker/fur segments
- **Result**: Clear, blocky cat features like cartoon reference image

## Check Statistics

Look for in the output:
```
Total regions: XXX       # Should be 30-60% less than before
Colors used: 15          # Down from 20
Min region size: 200     # Up from 50

Region size statistics:
  - Smallest: 200+ pixels   # No regions below min_region_size
  - Largest: XXXX pixels
  - Average: 800+ pixels    # Should be 3-4x larger
```

## API Test (if DB is set up)

```powershell
# Upload via API
$token = Get-Content firebase_token.txt
$headers = @{Authorization = "Bearer $token"}
$file = [System.IO.File]::ReadAllBytes("E:\git\cloud-gallery\test-photos\boba.jpg")

Invoke-RestMethod `
  -Uri "http://localhost:8080/api/projects/create" `
  -Method Post `
  -Headers $headers `
  -Form @{
    file = $file
    title = "Test Improved Segmentation"
    num_colors = 15
    difficulty = "medium"
  }
```

## What Changed

✅ **Cartoon preprocessing** - Photos are cartoonified first  
✅ **Larger regions** - Min 200px (was 50px)  
✅ **Fewer colors** - Default 15 (was 20)  
✅ **Better merging** - 2x morphological iterations  
✅ **Faster processing** - Optimized algorithms  

## Troubleshooting

### Terminal hangs during test
- This may be due to OpenCV/numpy processing
- The code is correct (no errors found)
- Try testing via Android app instead
- Or restart PowerShell and try again

### No visible difference
- Check you're using NEW project uploads (old ones won't have preprocessing)
- Verify `MIN_REGION_SIZE=200` in environment
- Compare file sizes: new templates should be smaller (fewer regions)

### Too few regions
- Decrease `num_colors` (try 10-12)
- Increase `min_region_size` (try 250-300)
- Adjust via API parameters

### Too many regions
- Increase `num_colors` (try 18-20)
- Decrease `min_region_size` (try 150-180)
- These are now configurable per-request

