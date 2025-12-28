# Digital Paint-by-Numbers Coloring App - Architecture Redesign

## 🎨 Vision
Transform personal photos into interactive paint-by-numbers coloring templates that users color digitally in the app (like Zen Color). Tap colors at the bottom, tap regions to fill, and save completed artwork to your gallery.

## 📋 What We Keep from Current Architecture

### ✅ Infrastructure (Already Working)
- **Firebase Authentication** - User accounts, Google Sign-In
- **Google Cloud Storage** - Store original photos and generated templates
- **PostgreSQL** - Store user projects, templates, settings
- **React Frontend** - Web interface (mobile-responsive)
- **Flask Backend** - API server
- **Android/iOS Structure** - Ready for mobile apps

### ✅ Features to Reuse
- User authentication and profiles
- Image upload mechanism
- Cloud storage integration
- Database schema (modify tables)

---

## 🎯 New Features to Build

### 1. **Image Processing Pipeline**

#### Core Algorithm:
```
User Photo → Processing → Interactive Coloring Canvas
```

**Steps:**
1. **Upload & Validation**
   - Accept: JPG, PNG (max 10MB)
   - Resize to optimal dimensions (e.g., 800x600)

2. **Edge Detection**
   - Use OpenCV to detect boundaries
   - Convert to region outlines

3. **Color Quantization**
   - Reduce colors to paintable palette (10-50 colors)
   - User can select difficulty: Easy (10 colors), Medium (25), Hard (50)

4. **Region Segmentation**
   - Group adjacent pixels of same color using flood fill
   - Assign numbers to each color region
   - **Generate region boundaries** as polygons/paths for click detection

5. **Interactive Canvas Data Generation**
   - Create **SVG paths** or **Canvas regions** for each area
   - Map each region to its color number
   - Output JSON with region coordinates, color mappings, boundaries
   - Enable tap-to-fill interaction

6. **Color Palette UI Data**
   - Generate color picker bar (colors + numbers)
   - Match colors to regions for validation

### 2. **GCP Services Integration**

#### Option A: Vision AI + Custom Processing
```python
# Use GCP Vision API for initial analysis
from google.cloud import vision

client = vision.ImageAnnotatorClient()
# Detect dominant colors
# Edge detection
# Then custom processing
```

#### Option B: Pure OpenCV (Cost-effective)
```python
import cv2
import numpy as np
from sklearn.cluster import KMeans

# All processing local/in-backend
# No additional GCP costs
```

#### Recommended: **Hybrid Approach**
- Use **Cloud Run** for scalable processing
- Use **Cloud Tasks** for async job queue
- Use **GCS** for storing templates
- **OpenCV** for processing (cheaper than Vision API)

---

## 🗄️ Database Schema Updates

### Current Tables (Modify):
```sql
-- Rename: images → projects
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    original_image_url TEXT,
    template_data JSON,         -- NEW: Region boundaries, color mappings
    color_palette JSON,         -- NEW: Color reference [{num: 1, rgb: [r,g,b]}]
    difficulty VARCHAR(20),     -- NEW: easy/medium/hard
    num_colors INTEGER,         -- NEW: 10-50
    status VARCHAR(20),         -- processing/completed/failed
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- NEW: Store user's coloring progress
CREATE TABLE coloring_sessions (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    user_id VARCHAR(255) NOT NULL,
    filled_regions JSON,        -- {regionId: colorNum} - which regions user filled
    completion_percent INTEGER, -- 0-100
    colored_image_url TEXT,     -- Final colored result saved to GCS
    is_completed BOOLEAN,
    started_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- NEW: Store processing jobs
CREATE TABLE processing_jobs (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    status VARCHAR(20),         -- queued/processing/completed/failed
    progress INTEGER,           -- 0-100
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- NEW: Store user preferences
CREATE TABLE user_preferences (
    user_id VARCHAR(255) PRIMARY KEY,
    default_difficulty VARCHAR(20),
    default_colors INTEGER,
    email_notifications BOOLEAN,
    created_at TIMESTAMP
);
```

---

## 🎨 Frontend Features

### New Pages/Components:

1. **Upload Page** (`/upload`)
   - Drag & drop photo upload
   - Preview original image
   - Select difficulty/color count
   - Processing progress bar

2. **Coloring Canvas Page** (`/color/:projectId`)
   - **Main Canvas**: Interactive SVG or HTML5 Canvas
   - **Color Picker Bar** (bottom): Row of colored circles with numbers
   - **Features**:
     - Tap color to select
     - Tap region to fill with selected color
     - Undo/redo buttons
     - Zoom/pan controls
     - Completion percentage
     - Hint mode (show correct colors)
   - **Save progress** automatically
   - **Finish** button → saves completed image to gallery

3. **Gallery Page** (`/my-gallery`)
   - User's completed colored images
   - Before/after slider view
   - Filter by completion status
   - Share completed artwork
   - Delete/restart options

4. **Project Detail Page** (`/project/:projectId`)
   - View completed coloring
   - Stats: time spent, date completed
   - Download colored image
   - Share on social media

---

## 🔧 Backend API Changes

### New Endpoints:

```python
# POST /api/projects/create
# Upload image, start processing
{
  "title": "Family Photo",
  "difficulty": "medium",
  "num_colors": 25
}
→ Returns: { "project_id": "...", "job_id": "..." }

# GET /api/projects/:id
# Get project template data for coloring
→ Returns: {
  "id": "...",
  "template_data": {
    "regions": [
      {"id": 1, "colorNum": 3, "path": "M10,10 L20,15...", "filled": false},
      ...
    ],
    "colors": [
      {"num": 1, "rgb": [255, 120, 80]},
      ...
    ]
  },
  "status": "ready"
}

# GET /api/coloring/:sessionId
# Get user's current coloring progress
→ Returns: {
  "filled_regions": {"region_1": 3, "region_5": 1},
  "completion_percent": 45
}

# POST /api/coloring/:sessionId/fill
# User fills a region
{
  "region_id": "region_12",
  "color_num": 5
}
→ Returns: updated progress

# POST /api/coloring/:sessionId/complete
# Mark coloring as finished, save final image
→ Returns: { "colored_image_url": "gs://...", "completion_time": "..." }

# GET /api/gallery
# Get user's completed colorings
→ Returns: [{
  "id": "...",
  "title": "...",
  "original_url": "...",
  "colored_url": "...",
  "completed_at": "..."
}]
```

---

## 🧮 Image Processing Service

### Create: `backend/app/image_processor.py`

```python
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw, ImageFont
import cairosvg

class PaintByNumbersGenerator:
    def __init__(self, image_path, num_colors=20):
        self.image = cv2.imread(image_path)
        self.num_colors = num_colors
        
    def process(self):
        # 1. Resize for optimal processing
        self.resize_image()
        
        # 2. Color quantization
        self.quantize_colors()
        
        # 3. Edge detection
        self.detect_edges()
        
        # 4. Create regions and assign numbers
        self.create_numbered_regions()
        
        # 5. Generate outputs
        return self.generate_templates()
    
    def quantize_colors(self):
        """Reduce image to N colors using K-means"""
        pixels = self.image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=self.num_colors, random_state=42)
        labels = kmeans.fit_predict(pixels)
        self.color_palette = kmeans.cluster_centers_.astype(int)
        self.color_labels = labels.reshape(self.image.shape[:2])
    
    def detect_edges(self):
        """Find region boundaries"""
        edges = cv2.Canny(self.image, 100, 200)
        # Combine with color boundaries
        return edges
    
    def create_numbered_regions(self):
        """Assign numbers to each color region"""
        # Connected components analysis
        # Label each region with its color number
        pass
    
    def generate_templates(self):
        """Create PDF, SVG, PNG outputs"""
        # Template with numbers
        # Color reference card
        # Return download URLs
        pass
```

---

## 📱 Mobile App Features

### Android/iOS (Future Phases)
- Camera integration (take photo → paint by numbers)
- Gallery integration (select existing photo)
- Offline mode (download templates)
- Share templates with friends
- In-app color picker for physical painting

---

## 🚀 Revised Implementation Phases

### **Phase 1: Core Image Processing** (1-2 weeks)
- [ ] Implement color quantization algorithm
- [ ] Edge detection and region segmentation
- [ ] Generate basic numbered template (PNG)
- [ ] Create color palette reference

### **Phase 2: Template Generation** (1 week)
- [ ] PDF generation with proper sizing
- [ ] SVG generation for scalability
- [ ] Print-optimized layouts
- [ ] Color reference card design

### **Phase 3: Backend Integration** (1 week)
- [ ] Update database schema
- [ ] Create new API endpoints
- [ ] Implement async processing queue
- [ ] File storage for templates

### **Phase 4: Frontend Rebuild** (2 weeks)
- [ ] Upload page with settings
- [ ] Processing status display
- [ ] Editor page with preview
- [ ] Download/print interface
- [ ] User project gallery

### **Phase 5: Polish & Features** (1 week)
- [ ] Error handling
- [ ] Progress indicators
- [ ] Template customization options
- [ ] Print guides/instructions

### **Phase 6: Mobile Apps** (2-3 weeks)
- [ ] Android app (Kotlin)
- [ ] iOS app (Swift/React Native)
- [ ] Camera integration
- [ ] Offline capabilities

---

## 💰 Cost Optimization

### What We Use (Costs):
- **Cloud Storage**: ~$0.02/GB/month
- **Cloud Run**: Pay per request (generous free tier)
- **PostgreSQL**: Local dev (free), Cloud SQL production (~$10-50/month)
- **Firebase Auth**: Free up to 50k users

### What We DON'T Need:
- ❌ Vision API ($1.50 per 1000 images)
- ❌ Use OpenCV instead (free)

### Estimated Monthly Cost:
- **Development**: $0 (local PostgreSQL)
- **Production (100 users)**: ~$15-25/month

---

## 🎯 MVP Feature Set

### Must Have:
1. ✅ Upload photo
2. ✅ Select difficulty (color count)
3. ✅ Generate numbered template
4. ✅ Download as PDF/PNG
5. ✅ View color palette

### Nice to Have:
- Adjust color palette manually
- Preview before processing
- Share templates
- Print directly from app
- Template marketplace (share designs)

### Future Ideas:
- AI-suggested difficulty based on photo
- Custom color palettes (match specific paint sets)
- Collaborative painting (multiple users)
- Time-lapse of painting progress
- AR preview (see how it looks painted)

---

## 📝 Next Steps

1. **Decide on approach**: Pure OpenCV vs some GCP AI
2. **Build MVP processing algorithm** (Python notebook test)
3. **Update database schema**
4. **Create one working example** (photo → template)
5. **Build frontend upload flow**
6. **Polish and add features**

---

## 🤔 Questions to Consider:

1. **Target audience**: Kids? Adults? Professional artists?
2. **Print sizes**: Standard letter (8.5x11)? Poster sizes?
3. **Color matching**: Match specific paint brands (Crayola, etc.)?
4. **Monetization**: Free with limits? Premium features?
5. **Social features**: Share templates? Template marketplace?

---

Would you like me to start implementing the image processing algorithm first, or would you prefer to update the frontend/backend structure?
