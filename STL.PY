import cadquery as cq

# ==========================================
# פרמטרים הנדסיים גלובליים להדפסה
# ==========================================
BASE_THICKNESS = 4.0      # עובי הבסיס במ"מ
EMBOSS_HEIGHT = 1.2       # גובה הבלטת הטקסט והאייקונים במ"מ
TOTAL_HEIGHT = BASE_THICKNESS + EMBOSS_HEIGHT # total: 5.2mm

RING_OUTER_R = 4.0        # רדיוס חיצוני של חור הטבעת (קוטר 8 מ"מ)[cite: 2]
RING_INNER_R = 2.25       # רדיוס חור פנימי (קוטר 4.5 מ"מ)[cite: 2]

# מרווחים בין מרכזי מחזיקי המפתחות על המשטח (במ"מ)
GRID_SPACING_X = 48.0     
GRID_SPACING_Y = 68.0     

# ==========================================
# פונקציות עזר לבסיסים וטבעות
# ==========================================

def add_keychain_ring(base_shape, top_y_offset):
    """מוסיף טבעת חיזוק עם חור לטבעת מפתחות"""
    ring = (
        cq.Workplane("XY")
        .center(0, top_y_offset)
        .circle(RING_OUTER_R)
        .circle(RING_INNER_R)
        .extrude(BASE_THICKNESS)
    )
    return base_shape.union(ring)

def create_shield_base():
    """צורת מגן"""
    pts = [(0, 28), (17, 18), (15, -14), (0, -28), (-15, -14), (-17, 18)]
    base = (
        cq.Workplane("XY")
        .polyline(pts)
        .close()
        .extrude(BASE_THICKNESS)
        .edges("|Z")
        .fillet(2.0)
    )
    return add_keychain_ring(base, 26)

def create_rect_base():
    """צורת מלבן מעוגל"""
    base = (
        cq.Workplane("XY")
        .box(34, 52, BASE_THICKNESS)
        .edges("|Z")
        .fillet(3.0)
        .translate((0, 0, BASE_THICKNESS / 2))
    )
    return add_keychain_ring(base, 26)

def create_hexagon_base():
    """צורת משושה"""
    base = (
        cq.Workplane("XY")
        .polygon(6, 38)
        .extrude(BASE_THICKNESS)
        .edges("|Z")
        .fillet(1.5)
    )
    return add_keychain_ring(base, 21)

# ==========================================
# בניית 9 מחזיקי המפתחות (זהירות בדרכים)
# ==========================================

def make_kc_1():
    """1. מגן + מעבר חצייה"""
    base = create_shield_base()
    stripes = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .pushPoints([(-6, -6), (-2, -2), (2, 2), (6, 6)])
        .box(3, 10, EMBOSS_HEIGHT)
    )
    return base.union(stripes)

def make_kc_2():
    """2. מלבן + "זהירות בדרכים" ותמרור"""
    base = create_rect_base()
    tri = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .center(0, 10)
        .polygon(3, 16)
        .extrude(EMBOSS_HEIGHT)
    )
    txt = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .center(0, -10)
        .text("זהירות", 5, EMBOSS_HEIGHT, font="Arial", kind="bold")
    )
    return base.union(tri).union(txt)

def make_kc_3():
    """3. משושה + פסי זברה"""
    base = create_hexagon_base()
    stripes = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .pushPoints([(-8, 0), (-4, 0), (0, 0), (4, 0), (8, 0)])
        .box(2, 18, EMBOSS_HEIGHT)
    )
    return base.union(stripes)

def make_kc_4():
    """4. משולש סכנה / החלקה"""
    base = (
        cq.Workplane("XY")
        .polygon(3, 40)
        .extrude(BASE_THICKNESS)
        .edges("|Z")
        .fillet(2.0)
    )
    base = add_keychain_ring(base, 19)
    inner_tri = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .polygon(3, 26)
        .extrude(EMBOSS_HEIGHT)
    )
    return base.union(inner_tri)

def make_kc_5():
    """5. תמרור עגול + "עצור"""
    base = cq.Workplane("XY").circle(19).extrude(BASE_THICKNESS)
    base = add_keychain_ring(base, 19)
    txt = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .text("עצור", 7, EMBOSS_HEIGHT, font="Arial", kind="bold")
    )
    return base.union(txt)

def make_kc_6():
    """6. מגן + אייקון חגורת בטיחות"""
    base = create_shield_base()
    icon = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .center(0, -2)
        .rrect(14, 20, 2)
        .extrude(EMBOSS_HEIGHT)
    )
    return base.union(icon)

def make_kc_7():
    """7. מלבן רמזור"""
    base = create_rect_base()
    lights = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .pushPoints([(0, 10), (0, 0), (0, -10)])
        .circle(4)
        .extrude(EMBOSS_HEIGHT)
    )
    return base.union(lights)

def make_kc_8():
    """8. מגן + רוכב אופניים / שתף את הכביש"""
    base = create_shield_base()
    wheels = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .pushPoints([(-6, -5), (6, -5)])
        .circle(4.5)
        .extrude(EMBOSS_HEIGHT)
    )
    return base.union(wheels)

def make_kc_9():
    """9. תמניון + "בטיחות""""
    base = (
        cq.Workplane("XY")
        .polygon(8, 36)
        .extrude(BASE_THICKNESS)
        .edges("|Z")
        .fillet(1.5)
    )
    base = add_keychain_ring(base, 18)
    txt = (
        cq.Workplane("XY")
        .workplane(offset=BASE_THICKNESS)
        .text("בטיחות", 5.5, EMBOSS_HEIGHT, font="Arial", kind="bold")
    )
    return base.union(txt)

# ==========================================
# איחוד 9 העיצובים לקובץ STL אחד (גריד 3x3)
# ==========================================

generators = [
    [make_kc_1, make_kc_2, make_kc_3],
    [make_kc_4, make_kc_5, make_kc_6],
    [make_kc_7, make_kc_8, make_kc_9]
]

# אובייקט ראשי המאחד את כל המודלים
single_stl_compound = cq.Workplane("XY")

for row in range(3):
    for col in range(3):
        # חישוב קואורדינטות מיקום לכל מחזיק מפתח
        x_off = (col - 1) * GRID_SPACING_X
        y_off = (1 - row) * GRID_SPACING_Y
        
        # יצירת המודל והזזתו למיקום המיועד
        item = generators[row][col]()
        positioned_item = item.translate((x_off, y_off, 0))
        
        # מיזוג לקובץ היחיד
        single_stl_compound = single_stl_compound.union(positioned_item)

# יצוא הקובץ היחיד
output_filename = "road_safety_9_keychains_array.stl"
cq.exporters.export(single_stl_compound, output_filename)

print(f"קובץ ה-STL המאוחד נוצר בהצלחה: {output_filename}")
