import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import random
import itertools
import os

def load_items(filepath):
    with open(filepath, 'r') as f:
        items = json.load(f)
    return items

def check_overlap(pos1, dim1, pos2, dim2):
    x1, y1, z1 = pos1
    w1, d1, h1 = dim1
    x2, y2, z2 = pos2
    w2, d2, h2 = dim2

    return not (x1 + w1 <= x2 or x2 + w2 <= x1 or
                y1 + d1 <= y2 or y2 + d2 <= y1 or
                z1 + h1 <= z2 or z2 + h2 <= z1)

def check_supported(pos, dim, placed_items):
    x, y, z = pos
    w, d, h = dim
    
    if z == 0:
        return True

    cx = x + w / 2
    cy = y + d / 2
    
    supported = False
    for p_pos, p_dim, _ in placed_items:
        px, py, pz = p_pos
        pw, pd, ph = p_dim
        
        if abs((pz + ph) - z) < 1e-6: 
            if px <= cx <= px + pw and py <= cy <= py + pd:
                supported = True
                break
    return supported

def validate_packing(placements, container_dims=(100, 100, 100)):
    print("\nStarting Validation Pass...")
    cw, cd, ch = container_dims
    errors = []
    
    for i, item1 in enumerate(placements):
        x1, y1, z1 = item1['pos']
        w1, d1, h1 = item1['dims']
        
        # Bounds check
        if x1 < 0 or y1 < 0 or z1 < 0 or x1 + w1 > cw or y1 + d1 > cd or z1 + h1 > ch:
            errors.append(f"Item {item1['id']} is out of bounds.")
            
        # Overlap check
        for j, item2 in enumerate(placements):
            if i == j: continue
            if check_overlap(item1['pos'], item1['dims'], item2['pos'], item2['dims']):
                errors.append(f"Overlap detected between Item {item1['id']} and Item {item2['id']}.")
                
    if not errors:
        print("Validation Successful: No overlaps or boundary violations found.")
        return True
    else:
        print(f"Validation Failed: {len(errors)} issues found.")
        for e in errors[:5]: # Show first 5 errors
            print(f"  > {e}")
        return False

def pack_items(items):
    item_list = []
    for i in items:
        w, d, h = i['dims']
        item_list.append({
            'id': i['id'],
            'dims': (w, d, h),
            'type': i['type'],
            'vol': w*d*h,
            'area': w*d 
        })
        
    item_list.sort(key=lambda x: x['area'], reverse=True)
    
    placed_items = [] 
    candidate_points = [(0,0,0)]
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'orange', 'purple', 'brown', 'pink']
    final_placements = []
    
    master_box_vol = 100 * 100 * 100
    packed_vol = 0

    print(f"Starting packing of {len(item_list)} items...")

    for item in item_list:
        candidate_points.sort(key=lambda p: (p[2], p[1], p[0]))
        found_spot = None
        best_orientation = None
        
        orientations = list(set(itertools.permutations(item['dims'])))
        
        for pt in candidate_points:
            x, y, z = pt
            for orient in orientations:
                w, d, h = orient
                if x + w > 100 or y + d > 100 or z + h > 100:
                    continue
                
                overlap = False
                for p_pos, p_dim, _ in placed_items:
                    if check_overlap((x,y,z), (w,d,h), p_pos, p_dim):
                        overlap = True
                        break
                if overlap:
                    continue
                    
                if check_supported((x,y,z), (w,d,h), placed_items):
                    found_spot = (x,y,z)
                    best_orientation = (w,d,h)
                    break
            if found_spot: break
        
        if found_spot:
            x, y, z = found_spot
            w, d, h = best_orientation
            color = random.choice(colors)
            placed_items.append(((x,y,z), (w,d,h), color))
            final_placements.append({
                'id': item['id'],
                'pos': (x,y,z),
                'dims': (w,d,h),
                'color': color,
                'type': item['type']
            })
            packed_vol += (w*d*h)
            
            new_candidates = [(x+w, y, z), (x, y+d, z), (x, y, z+h)]
            for np in new_candidates:
                if np[0] < 100 and np[1] < 100 and np[2] < 100:
                   if np not in candidate_points:
                       candidate_points.append(np)
            if found_spot in candidate_points:
                candidate_points.remove(found_spot)
        else:
            print(f"Could not place item {item['id']} ({item['type']})")

    efficiency = (packed_vol / master_box_vol) * 100
    print(f"\n--- Packing Complete ---")
    print(f"Packed {len(final_placements)} / {len(items)} items")
    print(f"Total Packed Volume: {packed_vol}")
    print(f"Master Box Volume: {master_box_vol}")
    print(f"Packing Density (Efficiency): {efficiency:.2f}%")
    
    # Save results to JSON
    with open('packing_results.json', 'w') as f:
        json.dump({
            'metrics': {
                'total_items': len(items),
                'packed_items': len(final_placements),
                'efficiency_percent': round(efficiency, 2),
                'total_volume': packed_vol
            },
            'placements': final_placements
        }, f, indent=4)
    print("Structured placement data saved to 'packing_results.json'")
    
    validate_packing(final_placements)
    
    return final_placements

def update_plot(frame, placements, ax, title_text):
    if frame >= len(placements):
        return
        
    item = placements[frame]
    x, y, z = item['pos']
    w, d, h = item['dims']
    color = item['color']
    
    ax.bar3d(x, y, z, w, d, h, color=color, alpha=0.7, edgecolor='k')
    
    # Add label in the center of the box
    ax.text(x + w/2, y + d/2, z + h/2, f"{item['id']}", color='black', 
            ha='center', va='center', fontsize=8, fontweight='bold')
    
    title_text.set_text(f"Placed {frame+1}/{len(placements)}: {item['type']} ID:{item['id']}")

def visualize(placements):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Bin Packing Animation')
    
    # Draw Container Wireframe
    container_corners = [
        [0,0,0], [100,0,0], [100,100,0], [0,100,0],
        [0,0,100], [100,0,100], [100,100,100], [0,100,100]
    ]
    edges = [
        (0,1), (1,2), (2,3), (3,0), # Bottom
        (4,5), (5,6), (6,7), (7,4), # Top
        (0,4), (1,5), (2,6), (3,7)  # Pillars
    ]
    for edge in edges:
        p1, p2 = container_corners[edge[0]], container_corners[edge[1]]
        ax.plot3D(*zip(p1, p2), color="gray", linestyle="--", alpha=0.5)

    title_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    ani = animation.FuncAnimation(
        fig, 
        update_plot, 
        frames=len(placements) + 5,
        fargs=(placements, ax, title_text), 
        interval=300, 
        repeat=False
    )
    
    print("Saving animation to 'packing_animation.mp4'...")
    try:
        ani.save('packing_animation.mp4', writer='ffmpeg', fps=3)
        print("Saved as mp4")
    except Exception as e:
        print(f"FFmpeg failed ({e}), saving as GIF...")
        ani.save('packing_animation.gif', writer='pillow', fps=3)
        print("Saved as gif")

    print("\nOpening interactive 3D view...")
    plt.show()

if __name__ == "__main__":
    items_path = '../R&D assignment questions/Item List.json'
    if not os.path.exists(items_path):
        print(f"Error: {items_path} not found.")
    else:
        items = load_items(items_path)
        placements = pack_items(items)
        visualize(placements)
