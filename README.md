
# Solar System Simulation

A visually stunning interactive simulation of our solar system built with Python's Tkinter GUI framework. This application features realistic planetary orbits, a toggleable display mode, and detailed planetary information panels.

## Key Features

### 🌌 Dual Display Modes
- **Orbital Mode**: Planets orbit the sun in elliptical paths with vertical flattening for 3D perspective
- **Linear Mode**: Planets displayed in scale along a horizontal axis with proportional spacing

### 🪐 Realistic Celestial Mechanics
- Elliptical orbits with Keplerian motion principles
- Individual orbital speeds based on real planetary data
- Depth-based size scaling for perspective effect
- Planets pass behind the sun with proper occlusion

### 🔭 Interactive Elements
- Planet selection system with detailed information panels
- Animated property displays showing:
  - Planetary diameter
  - Distance from sun
  - Surface temperature
- Visual connectors between planets and their data

### 🎨 Visual Design
- Starry background with procedurally generated stars
- High-resolution planet textures
- Smooth animations (60 FPS)
- Responsive UI with toggle button
- Clean information overlays with yellow highlight scheme

## Technical Implementation
- **Core Libraries**: 
  - `tkinter` for GUI rendering
  - `PIL` (Pillow) for image processing
  - `math` for orbital calculations
- **Optimization Techniques**:
  - Image preloading and caching
  - Canvas item management
  - Depth-based rendering
  - Selective redrawing
- **Physics Models**:
  - Angular velocity calculations
  - Elliptical orbit paths
  - Vertical flattening for 3D effect
  - Orbital alignment detection

## Data Visualization
Each planet displays:
- Name
- Diameter (km)
- Distance from sun (million km)
- Surface temperature (°C)

Supported planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune

## Requirements
- Python 3.6+
- Pillow (`pip install pillow`)

---
# Demo Images
<img width="1496" height="918" alt="image" src="https://github.com/user-attachments/assets/578c581a-050f-44b0-8d8e-a398fb7ccb8f" />
<img width="1480" height="866" alt="image" src="https://github.com/user-attachments/assets/48cd5044-6e24-43c0-8174-d24fbf3ef626" />
<img width="1486" height="866" alt="image" src="https://github.com/user-attachments/assets/d4b8d365-7056-4335-9162-319862ffca89" />
<img width="1485" height="859" alt="image" src="https://github.com/user-attachments/assets/3945fe73-2f80-4cab-baeb-842873eb8593" />
<img width="1496" height="914" alt="image" src="https://github.com/user-attachments/assets/db2f8a7b-9005-46de-a438-7b271bc7d702" />




