import tkinter as tk
from tkinter import colorchooser, messagebox


def rgb_to_xyz(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    return (x * 100, y * 100, z * 100)


def xyz_to_rgb(x, y, z):
    x /= 100
    y /= 100
    z /= 100
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    r, g, b = [max(0, min(255, int(c * 255))) for c in (r, g, b)]
    return r, g, b


def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return (0, 0, 0, 1)
    c = 1 - (r / 255)
    m = 1 - (g / 255)
    y = 1 - (b / 255)
    k = min(c, m, y)
    c = (c - k) / (1 - k) if k < 1 else 0
    m = (m - k) / (1 - k) if k < 1 else 0
    y = (y - k) / (1 - k) if k < 1 else 0
    return (c, m, y, k)


def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)


def update_colors(event=None):
    try:
        r = int(entry_r.get())
        g = int(entry_g.get())
        b = int(entry_b.get())

        if any(c < 0 or c > 255 for c in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255.")

        color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

        x, y, z = rgb_to_xyz(r, g, b)
        entry_x.delete(0, tk.END)
        entry_x.insert(0, f"{x:.2f}")
        entry_y.delete(0, tk.END)
        entry_y.insert(0, f"{y:.2f}")
        entry_z.delete(0, tk.END)
        entry_z.insert(0, f"{z:.2f}")

        c, m, y_cmyk, k = rgb_to_cmyk(r, g, b)
        entry_c.delete(0, tk.END)
        entry_c.insert(0, f"{c:.2f}")
        entry_m.delete(0, tk.END)
        entry_m.insert(0, f"{m:.2f}")
        entry_y_cmyk.delete(0, tk.END)
        entry_y_cmyk.insert(0, f"{y_cmyk:.2f}")
        entry_k.delete(0, tk.END)
        entry_k.insert(0, f"{k:.2f}")

        r_scale.set(r)
        g_scale.set(g)
        b_scale.set(b)
        x_scale.set(x)
        y_scale.set(y)
        z_scale.set(z)
        c_scale.set(c * 100)
        m_scale.set(m * 100)
        y_cmyk_scale.set(y_cmyk * 100)
        k_scale.set(k * 100)

    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))


def update_rgb_from_xyz(event=None):
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())

        r, g, b = xyz_to_rgb(x, y, z)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()

    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))


def update_rgb_from_cmyk(event=None):
    try:
        c = float(entry_c.get()) / 100
        m = float(entry_m.get()) / 100
        y_cmyk = float(entry_y_cmyk.get()) / 100
        k = float(entry_k.get()) / 100

        r, g, b = cmyk_to_rgb(c, m, y_cmyk, k)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()

    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))


def choose_color():
    color_code = colorchooser.askcolor(title="Выберите цвет")[1]
    if color_code:
        r = int(color_code[1:3], 16)
        g = int(color_code[3:5], 16)
        b = int(color_code[5:7], 16)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()


def scale_update(val):
    entry_r.delete(0, tk.END)
    entry_r.insert(0, r_scale.get())
    entry_g.delete(0, tk.END)
    entry_g.insert(0, g_scale.get())
    entry_b.delete(0, tk.END)
    entry_b.insert(0, b_scale.get())
    update_colors()

def scale_update_xyz(val):
    entry_x.delete(0, tk.END)
    entry_x.insert(0, x_scale.get())
    entry_y.delete(0, tk.END)
    entry_y.insert(0, y_scale.get())
    entry_z.delete(0, tk.END)
    entry_z.insert(0, z_scale.get())
    update_rgb_from_xyz()

def scale_update_cmyk(val):
    entry_c.delete(0, tk.END)
    entry_c.insert(0, c_scale.get())
    entry_m.delete(0, tk.END)
    entry_m.insert(0, m_scale.get())
    entry_y_cmyk.delete(0, tk.END)
    entry_y_cmyk.insert(0, y_cmyk_scale.get())
    entry_k.delete(0, tk.END)
    entry_k.insert(0, k_scale.get())
    update_rgb_from_cmyk()

root = tk.Tk()
root.title("Color converter")
root.geometry("500x600")
root.resizable(False, False)

r_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
r_scale.grid(row=1, column=2)
g_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
g_scale.grid(row=2, column=2)
b_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
b_scale.grid(row=3, column=2)
x_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_xyz, length=200)
x_scale.grid(row=5, column=2)
y_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_xyz, length=200)
y_scale.grid(row=6, column=2)
z_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_xyz, length=200)
z_scale.grid(row=7, column=2)
c_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_cmyk, length=200)
c_scale.grid(row=9, column=2)
m_scale = tk.Scale(orient=tk.HORIZONTAL,from_=0, to=100,  command=scale_update_cmyk, length=200)
m_scale.grid(row=10, column=2)
y_cmyk_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_cmyk, length=200)
y_cmyk_scale.grid(row=11, column=2)
k_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_cmyk, length=200)
k_scale.grid(row=12, column=2)

tk.Label(root, text="R:").grid(row=1, column=0)
tk.Label(root, text="G:").grid(row=2, column=0)
tk.Label(root, text="B:").grid(row=3, column=0)
tk.Label(root, text="__________").grid(row=4, column=0)
tk.Label(root, text="X:").grid(row=5, column=0)
tk.Label(root, text="Y:").grid(row=6, column=0)
tk.Label(root, text="Z:").grid(row=7, column=0)
tk.Label(root, text="__________").grid(row=8, column=0)
tk.Label(root, text="C:").grid(row=9, column=0)
tk.Label(root, text="M:").grid(row=10, column=0)
tk.Label(root, text="Y:").grid(row=11, column=0)
tk.Label(root, text="K:").grid(row=12, column=0)

entry_r = tk.Entry(root)
entry_g = tk.Entry(root)
entry_b = tk.Entry(root)
entry_x = tk.Entry(root)
entry_y = tk.Entry(root)
entry_z = tk.Entry(root)
entry_c = tk.Entry(root)
entry_m = tk.Entry(root)
entry_y_cmyk = tk.Entry(root)
entry_k = tk.Entry(root)

entry_r.grid(row=1, column=1)
entry_g.grid(row=2, column=1)
entry_b.grid(row=3, column=1)
entry_x.grid(row=5, column=1)
entry_y.grid(row=6, column=1)
entry_z.grid(row=7, column=1)
entry_c.grid(row=9, column=1)
entry_m.grid(row=10, column=1)
entry_y_cmyk.grid(row=11, column=1)
entry_k.grid(row=12, column=1)

r_scale.set(255)
g_scale.set(255)
b_scale.set(255)
x_scale.set(0)
y_scale.set(0)
z_scale.set(0)
c_scale.set(0)
m_scale.set(0)
y_cmyk_scale.set(0)
k_scale.set(0)

color_display = tk.Frame(root, width=400, height=70)
color_display.grid(row=13, columnspan=3, pady=10, padx=50)
color_display.config(bg="#ffffff")

btn_choose_color = tk.Button(root, text="Chose color", command=choose_color)
btn_choose_color.grid(row=0, columnspan=3)

for entry in [entry_r, entry_g, entry_b]:
    entry.bind("<KeyRelease>", update_colors)

for entry in [entry_x, entry_y, entry_z]:
    entry.bind("<KeyRelease>", update_rgb_from_xyz)

for entry in [entry_c, entry_m, entry_y_cmyk, entry_k]:
    entry.bind("<KeyRelease>", update_rgb_from_cmyk)

root.mainloop()