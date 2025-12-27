# R&D Internship Assignment: 3D Visualization & Packing

## Overview
This project contains solutions for two primary tasks:
1. **OBB Computation**: Calculating and visualizing the Oriented Bounding Box (OBB) for various 3D meshes.
2. **3D Bin Packing**: An optimized 3D packing algorithm for rectangular items with gravity and support constraints.

---

## Part 1: OBB Computation (`obb_script.py`)

### Approach
- **Mesh Processing**: Uses the `trimesh` library to load `.obj` files. Scenes are automatically concatenated into a single mesh.
- **OBB Calculation**: Computes the true Oriented Bounding Box (not Axis-Aligned) using `mesh.bounding_box_oriented`, which minimizes volume by finding the optimal rotation.
- **Metrics**: Calculates length, width, height, and volume from the OBB extents.
- **Visualization**: Generates an interactive 3D view showing the original mesh (translucent blue) and the OBB overlay (translucent red wireframe).

### Objects Processed
- `CUBE.obj`
- `CYLINDER.obj`
- `TEAPOT.obj`

---

## Part 2: 3D Bin Packing (`main.py`)

### Algorithm: Greedy Bottom-Left-Back (BLB) with Rotations
- **Sorting**: Items are sorted by base area (Width × Depth) in descending order to prioritize a stable foundation.
- **Candidate Points**: Implements an anchor-point strategy. New candidate points (anchors) are generated at the top, right, and front faces of every placed item.
- **Rotations**: For each item, all 6 unique 3D orientations (permutations of dimensions) are tested.
- **Constraints**:
    - **Bounds**: Items must stay within the 100x100x100 container.
    - **Overlaps**: No two items can occupy the same space.
    - **Gravity/Support**: Every item must be supported by either the floor (Z=0) or the top surface of another placed item (center-point support).

### Enhancements
- **Validation Pass**: Programmatically verifies all placements post-packing for boundary or overlap violations.
- **Structured Data**: Results are exported to `packing_results.json`.
- **Visualization**: 
    - 3D Animation showing the step-by-step placement.
    - Container wireframe for spatial context.
    - Numeric labels on items for easy identification.
    - Interactive 3D view for full rotation and inspection.

---

## Metrics & PERFORMANCE
- **Container Size**: 100 x 100 x 100 (Volume: 1,000,000 units³)
- **Items Packed**: 20 / 20 (100% success rate for the provided list)
- **Total Packed Volume**: 168,250 units³
- **Packing Density (Efficiency)**: **16.83%**

*Note: The density is relatively low but reflects the sparse nature of the provided item dimensions relative to the large container size.*

---

## Limitations & Future Work
- **Static Support**: Currently uses center-point support. Multi-point support could allow for more complex stacking.
- **Heuristic**: The greedy approach is fast but may not reach theoretical maximum density (NP-hard problem).
- **Visualization**: Large numbers of items might overlap labels in the static view.

---

## Setup & Execution
1. Ensure the virtual environment is active.
2. Run OBB Computation:
   ```bash
   ./venv/bin/python obb_script.py
   ```
3. Run 3D Bin Packing:
   ```bash
   ./venv/bin/python main.py
   ```
