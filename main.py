from tinytuya import BulbDevice
import time
import tkinter as tk

# Configurando a lâmpada inteligente

bulb = BulbDevice('id', 'ip_address', 'local_key')
bulb.set_version(3.5)
bulb.set_socketPersistent(True)

# Funções de controle da lâmpada

def shutdown():
    
    bulb.set_brightness_percentage(0)
    

def brightness(percentage):

    bulb.set_brightness_percentage(percentage)
    

def white(colourtemp):

    bulb.set_mode('white', True)
    bulb.set_colourtemp_percentage(colourtemp) 
      

def colour(r, g, b):

    bulb.set_mode('colour', True)
    bulb.set_colour(r, g, b)
    

# Interface de controle da lâmpada

root = tk.Tk()
root.title("Bulb Control")

# Espaçamento 

PADX = 12
SECTION_PADY = (10, 6)
ITEM_PADY = 6
SCALE_LEN = 260

# Brilho

current_brightness = int(bulb.brightness() / 10)

frm_brightness = tk.Frame(root)
frm_brightness.pack(padx=PADX, pady=SECTION_PADY, fill="x")

brightness_scale = tk.Scale(frm_brightness, from_=1, to=100, orient="horizontal", label="Brightness", length=SCALE_LEN)
brightness_scale.set(current_brightness)
brightness_scale.pack(fill="x")
brightness_scale.bind("<ButtonRelease-1>", lambda e: brightness(brightness_scale.get()))

# Modo branco

current_colourtemp = int(bulb.colourtemp() / 10)

frm_white = tk.Frame(root)
frm_white.pack(padx=PADX, pady=SECTION_PADY, fill="x")

ct_var = tk.IntVar(value=current_colourtemp)
ct_scale = tk.Scale(frm_white, from_=0, to=100, orient="horizontal", label="Temperature (White)", variable=ct_var, length=SCALE_LEN)
ct_scale.pack(fill="x")

# Modo RGB

current_rgb = bulb.colour_rgb()

frm_rgb = tk.Frame(root)
frm_rgb.pack(padx=PADX, pady=SECTION_PADY, fill="x")

r_var = tk.IntVar(value=current_rgb[0])
g_var = tk.IntVar(value=current_rgb[1])
b_var = tk.IntVar(value=current_rgb[2])

tk.Label(frm_rgb, text="Color (RGB)").pack(anchor="w", pady=(0, 4))

for letter, var, color in (("R", r_var, "red"), ("G", g_var, "green"), ("B", b_var, "blue")):
    row = tk.Frame(frm_rgb)
    row.pack(fill="x", pady=ITEM_PADY)
    tk.Label(row, text=letter, fg=color, width=2).pack(side="left", padx=(0, 8))
    tk.Scale(row, from_=0, to=255, orient="horizontal", variable=var, length=SCALE_LEN)\
        .pack(side="left", fill="x", expand=True)

# Botões de ação

frm_actions = tk.Frame(root)
frm_actions.pack(padx=PADX, pady=(12, 12), fill="x")

tk.Button(frm_actions, text="Apply White", command=lambda: white(ct_var.get())).pack(pady=ITEM_PADY, fill="x")
tk.Button(frm_actions, text="Apply Color", command=lambda: colour(r_var.get(), g_var.get(), b_var.get())).pack(pady=ITEM_PADY, fill="x")
tk.Button(frm_actions, text="Shutdown", command=shutdown).pack(pady=ITEM_PADY, fill="x")

root.mainloop()