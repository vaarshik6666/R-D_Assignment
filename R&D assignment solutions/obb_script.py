import trimesh
import numpy as np
import os

def process_file(filename):
    filepath = os.path.join('../R&D assignment questions', filename)
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return

    print(f"\n" + "="*40)
    print(f"Processing: {filename}")
    print("="*40)
    
    try:
        mesh = trimesh.load(filepath)
        
        if isinstance(mesh, trimesh.Scene):
            if len(mesh.geometry) == 0:
                 print("  > Empty scene.")
                 return
            mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))

        obb = mesh.bounding_box_oriented
        dims = obb.primitive.extents
        volume = obb.volume
        
        print(f"Metrics:")
        print(f"  > Length:  {dims[0]:.4f}")
        print(f"  > Width:   {dims[1]:.4f}")
        print(f"  > Height:  {dims[2]:.4f}")
        print(f"  > Volume:  {volume:.4f}")
        print(f"\nOBB Transform Matrix:\n{obb.primitive.transform}")

        mesh.visual.face_colors = [100, 100, 255, 150] 
        obb.visual.face_colors = [255, 0, 0, 50]       
        
        print(f"\nOpening interactive window for {filename}...")
        print("(Close the window to proceed to the next object)")
        
        scene = trimesh.Scene([mesh, obb])
        scene.show(resolution=(800, 600), caption=f"{filename} - OBB Visualization")

    except Exception as e:
        print(f"  > Error processing {filename}: {e}")

if __name__ == "__main__":
    files = ["CUBE.obj", "CYLINDER.obj", "TEAPOT.obj"]
    for f in files:
        process_file(f)
    print("\nAll objects processed.")
