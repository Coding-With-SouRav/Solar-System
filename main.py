import tkinter as tk
from PIL import Image, ImageTk
import math, random
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 1200, 700
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SUN_SIZE = 180
ORBIT_SCALE = 0.6
VERTICAL_FLATTEN = 0.35

# Planet info: name, image path, orbit radius, speed, size, diameter, distance from sun (million km), temperature (°C)
planets_info = [
    ("Mercury", "images/mercury.png", 160, 0.0321, 20, 4879, 57.9, 167),
    ("Venus",   "images/venus.png",   240, 0.0235, 40, 12104, 108.2, 464),
    ("Earth",   "images/earth.png",   330, 0.02, 70, 12756, 149.6, 15),
    ("Mars",    "images/mars.png",    420, 0.0162, 35, 6792, 227.9, -65),
    ("Jupiter", "images/jupiter.png", 560, 0.0088, 110, 142984, 778.6, -110),
    ("Saturn",  "images/saturn.png",  700, 0.0065, 200, 120536, 1433.5, -140),
    ("Uranus",  "images/uranus.png",  820, 0.0046, 70, 51118, 2872.5, -195),
    ("Neptune", "images/neptune.png", 940, 0.0036, 70, 49528, 4495.1, -200),
]

# Scale orbit radius
for i in range(len(planets_info)):
    name, path, radius, speed, size, *props = planets_info[i]
    planets_info[i] = (name, path, radius * ORBIT_SCALE, speed, size, *props)

# ---------- HELPER: RESAMPLE (compatibility) ----------
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

# ---------- TKINTER SETUP ----------
root = tk.Tk()
root.title("Solar System Simulation")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

# Starry background (draw once)
for _ in range(250):
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    size = random.choice([1, 3])
    canvas.create_oval(x, y, x+size, y+size, fill="white", outline="")

# Load toggle button images (keep references)
toggle_off_img = ImageTk.PhotoImage(Image.open("images/toggle_off.png").resize((100, 50), RESAMPLE))
toggle_on_img  = ImageTk.PhotoImage(Image.open("images/toggle_on.png").resize((100, 50), RESAMPLE))

linear_mode = tk.BooleanVar(value=False)

def toggle_linear_mode(event=None):
    linear_mode.set(not linear_mode.get())
    canvas.itemconfig(toggle_btn, image=toggle_on_img if linear_mode.get() else toggle_off_img)
    # Clear mode-specific caches
    if linear_mode.get():
        for tag in ("planet_orbit_item", "planet_orbit_text"):
            canvas.delete(tag)
    else:
        for tag in ("planet_linear_item", "planet_linear_text"):
            canvas.delete(tag)

toggle_btn = canvas.create_image(WIDTH-60, 30, image=toggle_off_img, anchor="center")
canvas.tag_bind(toggle_btn, "<Button-1>", toggle_linear_mode)

# ---------- PRELOAD BASE IMAGES ----------
base_images = {}
# load sun
sun_img_full = Image.open("images/sun.png").resize((SUN_SIZE, SUN_SIZE), RESAMPLE)
sun_photo = ImageTk.PhotoImage(sun_img_full)
half_height = SUN_SIZE // 2
sun_upper_img = sun_img_full.crop((0, 0, SUN_SIZE, half_height))
sun_upper_photo = ImageTk.PhotoImage(sun_upper_img)

# load planet base images (PIL Image)
for name, path, *_ in planets_info:
    pth = path if os.path.exists(path) else f"images/{name.lower()}.png"
    base_images[name] = Image.open(pth).convert("RGBA")

# ---------- STATE / CACHES ----------
angles = [0.0 for _ in planets_info]
planet_photo_refs = {}       # keep current PhotoImage references keyed by planet name
planet_canvas_ids = {}       # canvas image item ids keyed by planet name (orbit mode)
planet_text_ids = {}         # canvas text ids keyed by planet name (orbit mode)
planet_linear_ids = {}       # canvas image ids keyed by planet name (linear mode)
planet_linear_texts = {}     # canvas text ids for linear mode
selected_planet = None

# Create sun on canvas (normal orbit mode sun)
canvas_sun = canvas.create_image(CENTER_X, CENTER_Y, image=sun_photo)

# ---------- DRAW ORBITS ----------
def draw_orbits():
    canvas.delete("orbit")
    for _, _, orbit_radius, _, _, *_ in planets_info:
        x0 = CENTER_X - orbit_radius
        y0 = CENTER_Y - orbit_radius * VERTICAL_FLATTEN
        x1 = CENTER_X + orbit_radius
        y1 = CENTER_Y + orbit_radius * VERTICAL_FLATTEN
        canvas.create_oval(x0, y0, x1, y1, outline="#666666", width=2, tags="orbit", dash=(8, 8))
    # sun upper mask (for overlapping effect)
    canvas.create_image(CENTER_X, CENTER_Y - SUN_SIZE // 4, image=sun_upper_photo, tags="mask", anchor="center")

# ---------- PLANET PROPERTY SELECTION ----------
def select_planet(name):
    global selected_planet
    selected_planet = name

# ---------- BOTTOM PLANET NAMES ----------
for i, (name, _, _, _, _, *_ ) in enumerate(planets_info):
    btn = tk.Button(root, text=name, font=("Arial", 15), bg="black", fg="white", bd =0, activebackground="black", activeforeground="white",
                    command=lambda n=name: select_planet(n))
    btn.place(x=50 + i*140, y=HEIGHT-50)

# ---------- UPDATE LOOP ----------
def update():
    global selected_planet
    canvas.delete("property")
    canvas.delete("line")
    canvas.delete("box")

    if linear_mode.get():
        canvas.itemconfig("orbit", state="hidden")
        canvas.itemconfig(canvas_sun, state="hidden")
        canvas.delete("mask")
        if not canvas.find_withtag("sun_linear"):
            canvas.create_image(200, CENTER_Y, image=sun_photo, tags="sun_linear")
        start_x = 200
        spacing = (WIDTH - start_x - SUN_SIZE - 50) / (len(planets_info) + 1)
        for i, (name, _, _, _, size, *_ ) in enumerate(planets_info):
            x = int(start_x + SUN_SIZE + 50 + spacing * (i + 1))
            y = CENTER_Y
            img = base_images[name].resize((size, size), RESAMPLE)
            photo = ImageTk.PhotoImage(img)
            planet_photo_refs[name] = photo

            if name in planet_linear_ids and canvas.type(planet_linear_ids[name]) == "image":
                canvas.coords(planet_linear_ids[name], x, y)
                canvas.itemconfig(planet_linear_ids[name], image=photo)
            else:
                cid = canvas.create_image(x, y, image=photo, tags=("planet", "planet_linear_item"))
                planet_linear_ids[name] = cid

            if name in planet_linear_texts and canvas.type(planet_linear_texts[name]) == "text":
                canvas.coords(planet_linear_texts[name], x, y + 60)
            else:
                tid = canvas.create_text(x, y + 60, text=name, fill="white", font=("Arial", 12),
                                          tags=("planet", "planet_linear_text"))
                planet_linear_texts[name] = tid

            if name == selected_planet:
                for planet in planets_info:
                    if planet[0] == name:
                        _, _, _, _, _, diameter, distance, temp = planet
                        box_width, box_height = 220, 80
                        box_x0 = x - box_width//2
                        box_y0 = y - size*2 - box_height - 10
                        box_x1 = x + box_width//2
                        box_y1 = y - size*2 - 10
                        canvas.create_rectangle(box_x0, box_y0, box_x1, box_y1,
                                                fill="#222222", outline="yellow", width=3, tags="box")
                        canvas.create_text(box_x0 + 10, box_y0 + 10,
                                           text=f"{name}\nDiameter: {diameter} km\nDistance: {distance} million km\nTemp: {temp}°C",
                                           fill="yellow", font=("Arial", 10), anchor="nw", tags="property")
                        line_mid_y = box_y1 + 5
                        canvas.create_line(x, y - size//2, x, line_mid_y, fill="yellow", width=3, tags="line")
                        break

    else:
        canvas.itemconfig("orbit", state="normal")
        canvas.delete("sun_linear")
        all_aligned = True
        base_angle = None

        for i, (name, _, orbit_radius, orbit_speed, size, *_ ) in enumerate(planets_info):
            angles[i] += orbit_speed * 3
            x = CENTER_X + orbit_radius * math.cos(angles[i])
            y = CENTER_Y + (orbit_radius * VERTICAL_FLATTEN) * math.sin(angles[i])

            display_size = size
            if name == selected_planet:
                display_size = int(display_size * 2)

            depth_scale = 0.5 + 0.5 * ((y - 0) / HEIGHT)
            img_size = max(10, int(display_size * depth_scale))
            img = base_images[name].resize((img_size, img_size), RESAMPLE)
            photo = ImageTk.PhotoImage(img)
            planet_photo_refs[name] = photo

            if name in planet_canvas_ids and canvas.type(planet_canvas_ids[name]) == "image":
                canvas.coords(planet_canvas_ids[name], x, y)
                canvas.itemconfig(planet_canvas_ids[name], image=photo)
            else:
                cid = canvas.create_image(x, y, image=photo, tags=("planet", "planet_orbit_item"))
                planet_canvas_ids[name] = cid

            if name == selected_planet:
                for planet in planets_info:
                    if planet[0] == name:
                        _, _, _, _, _, diameter, distance, temp = planet
                        box_width, box_height = 220, 80
                        box_x0 = x - box_width//2
                        box_y0 = y - img_size - box_height - 10
                        box_x1 = x + box_width//2
                        box_y1 = y - img_size - 10
                        canvas.create_rectangle(box_x0, box_y0, box_x1, box_y1,
                                                fill="#222222", outline="yellow", width=3, tags="box")
                        canvas.create_text(box_x0 + 10, box_y0 + 10,
                                           text=f"{name}\nDiameter: {diameter} km\nDistance: {distance} million km\nTemp: {temp}°C",
                                           fill="yellow", font=("Arial", 10), anchor="nw", tags="property")
                        line_start_y = y - img_size//2
                        line_end_y = box_y1 + 5
                        canvas.create_line(x, line_start_y, x, line_end_y, fill="yellow", width=3, tags="line")
                        break

            ang_deg = (math.degrees(angles[i]) % 360)
            if base_angle is None:
                base_angle = ang_deg
            else:
                diff = abs(ang_deg - base_angle) % 360
                if not (diff < 5 or abs(diff - 180) < 5):
                    all_aligned = False

        if all_aligned:
            canvas.itemconfig(canvas_sun, state="hidden")
            canvas.delete("mask")
        else:
            canvas.itemconfig(canvas_sun, state="normal")
            # ensure mask exists (only one)
            if not canvas.find_withtag("mask"):
                mask_id = canvas.create_image(CENTER_X, CENTER_Y - SUN_SIZE // 4, 
                                            image=sun_upper_photo, tags="mask", anchor="center")
            else:
                mask_id = canvas.find_withtag("mask")[0]
            # raise mask above all planets
            canvas.tag_raise(mask_id)
    root.after(15, update)

# ---------- INITIAL DRAW ----------
draw_orbits()
update()
root.mainloop()
