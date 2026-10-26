import trimesh
import numpy as np

# פרמטרים הנדסיים גלובליים
BASE_THICKNESS = 4.0      # עובי הבסיס במ"מ
EMBOSS_HEIGHT = 1.2       # גובה הבלטת הטקסט והאייקונים במ"מ
GRID_SPACING_X = 48.0     # מרווח בלוח
GRID_SPACING_Y = 68.0

def make_keychain_mesh():
    """יוצר מחזיק מפתחות בסיסי בתלת-ממד"""
    # בסיס מלבני
    base = trimesh.creation.box(extents=[34, 52, BASE_THICKNESS])
    base.apply_translation([0, 0, BASE_THICKNESS / 2])
    
    # טבעת למפתחות בחלק העליון (קוטר 8 מ"מ עם חור 4.5 מ"מ)
    ring = trimesh.creation.annulus(r_min=2.25, r_max=4.0, height=BASE_THICKNESS)
    ring.apply_translation([0, 26, BASE_THICKNESS / 2])
    
    # הבלטה של סמל/טקסט מעל הבסיס
    emboss = trimesh.creation.box(extents=[20, 26, EMBOSS_HEIGHT])
    emboss.apply_translation([0, -2, BASE_THICKNESS + (EMBOSS_HEIGHT / 2)])
    
    return trimesh.util.concatenate([base, ring, emboss])

# יצירת מערך 3x3 של 9 מחזיקי מפתחות
scene_meshes = []

for row in range(3):
    for col in range(3):
        x_off = (col - 1) * GRID_SPACING_X
        y_off = (1 - row) * GRID_SPACING_Y
        
        kc = make_keychain_mesh()
        kc.apply_translation([x_off, y_off, 0])
        scene_meshes.append(kc)

# איחוד כל 9 המחזיקים לקובץ STL אחד
combined_mesh = trimesh.util.concatenate(scene_meshes)
output_filename = "road_safety_9_keychains_array.stl"
combined_mesh.export(output_filename)

print(f"קובץ ה-STL המאוחד נוצר בהצלחה: {output_filename}")
