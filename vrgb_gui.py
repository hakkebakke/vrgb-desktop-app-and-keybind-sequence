#!/usr/bin/env python3
# Created for use with vrgb and a custom vrgb_sequence.sh for keybinding. This setup with vrgb now runs flawlessly on my ASUS Vivobook S14 M5406NA, and it should work on several other models as well.
# Also includes a desktop shortcut so it can be launched like a regular app. Both vrgb_sequence.sh and this file require permissions in sudo visudo.
# make sure keybordlight is turned on to the max brightness by the  F4 or fn+F4 button on your keyboard.

# Created by hakkebakke
#---------------------------------------------------------------------------
import tkinter as tk
import subprocess
import math

# The 12 predefined colors (Hex codes)
FASTE_FARGER = [
    {"name": "Red", "hex": "FF0000"}, {"name": "Green", "hex": "00FF00"},
    {"name": "Blue", "hex": "0000FF"}, {"name": "Yellow", "hex": "FFFF00"},
    {"name": "Cyan", "hex": "00FFFF"}, {"name": "Magenta", "hex": "FF00FF"},
    {"name": "Orange", "hex": "FFA500"}, {"name": "Purple", "hex": "800080"},
    {"name": "Pink", "hex": "FFC0CB"}, {"name": "White", "hex": "FFFFFF"},
    {"name": "Dark", "hex": "111111"}, {"name": "Off", "hex": "000000"}
]

# The 4 explicit brightness stages (0 to 100)
BRIGHTNESS_STAGES = [0, 33, 66, 100]

class VrgbCircularApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRGB Control Panel")
        self.root.geometry("460x840")
        
        # Track current state internally to handle absolute steps
        self.current_hex = "FFFFFF"
        self.brightness_index = 3 # Default to 100% (index 3)
        
        # Hardcoded Dark Theme background
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.root.configure(bg=self.bg_color)
        
        # Title
        title = tk.Label(root, text="VRGB Color Control", font=("Arial", 16, "bold"), fg=self.fg_color, bg=self.bg_color)
        title.pack(pady=(15, 5))
        
        # --- NEW SECTION: Brightness Controls (Now on top) ---
        bright_label = tk.Label(root, text="Brightness Control:", font=("Arial", 11, "bold"), fg="#aaaaaa", bg=self.bg_color)
        bright_label.pack(anchor="w", padx=25, pady=(5, 5))
        
        bright_frame = tk.Frame(root, bg=self.bg_color)
        bright_frame.pack(pady=(0, 10))
        
        # Brightness Down Button (Small Sun)
        dim_btn = tk.Button(
            bright_frame, 
            text="🔅", 
            font=("Arial", 18), 
            bg="#2d2d2d", 
            fg="white", 
            bd=0, 
            relief="flat",
            activebackground="#3a3a3a",
            activeforeground="white",
            cursor="hand2",
            padx=25,
            pady=5,
            command=lambda: self.adjust_brightness_step(-1)
        )
        dim_btn.pack(side=tk.LEFT, padx=15)
        
        # Brightness Up Button (Big Sun)
        bright_btn = tk.Button(
            bright_frame, 
            text="🔆", 
            font=("Arial", 18), 
            bg="#2d2d2d", 
            fg="white", 
            bd=0, 
            relief="flat",
            activebackground="#3a3a3a",
            activeforeground="white",
            cursor="hand2",
            padx=25,
            pady=5,
            command=lambda: self.adjust_brightness_step(1)
        )
        bright_btn.pack(side=tk.LEFT, padx=15)
        
        # Subtle Top Divider
        top_divider = tk.Frame(root, height=1, bg="#292929")
        top_divider.pack(fill=tk.X, padx=25, pady=10)
        
        # --- SECTION 2: Quick Select (Round Buttons with Text) ---
        btn_label = tk.Label(root, text="Quick Select (12 Steps):", font=("Arial", 11, "bold"), fg="#aaaaaa", bg=self.bg_color)
        btn_label.pack(anchor="w", padx=25, pady=(5, 5))
        
        grid_frame = tk.Frame(root, bg=self.bg_color)
        grid_frame.pack(fill=tk.X, padx=25)
        
        for i, farge in enumerate(FASTE_FARGER):
            row, col = i // 4, i % 4
            txt_c = "#000000" if farge["hex"] in ["FFFFFF", "FFFF00", "00FFFF", "FFC0CB"] else "#FFFFFF"
            
            c_btn = tk.Canvas(grid_frame, width=75, height=75, bg=self.bg_color, bd=0, highlightthickness=0, cursor="hand2")
            c_btn.grid(row=row, column=col, padx=6, pady=6)
            
            c_btn.create_oval(4, 4, 71, 71, fill=f"#{farge['hex']}", outline="black" if farge["hex"]=="000000" else f"#{farge['hex']}", width=1)
            c_btn.create_text(38, 38, text=farge["name"], fill=txt_c, font=("Arial", 10, "bold"))
            
            c_btn.bind("<Button-1>", lambda e, h=farge["hex"]: self.send_vrgb_command(h))
            grid_frame.grid_columnconfigure(col, weight=1)

        # Center Divider
        divider = tk.Frame(root, height=1, bg="#333333")
        divider.pack(fill=tk.X, padx=25, pady=15)

        # --- SECTION 3: Continuous Color Palette ---
        palett_label = tk.Label(root, text="Continuous Color Palette:", font=("Arial", 11, "bold"), fg="#aaaaaa", bg=self.bg_color)
        palett_label.pack(anchor="w", padx=25, pady=(0, 5))
        
        self.canvas_size = 250
        self.center = self.canvas_size // 2
        self.radius = self.center - 15
        
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg=self.bg_color, bd=0, highlightthickness=0)
        self.canvas.pack(pady=5)
        
        self.tegn_fargehjul()
        self.canvas.bind("<Button-1>", self.klikk_palett)
        self.canvas.bind("<B1-Motion>", self.klikk_palett)
        
        # Status footer at the bottom
        self.status_label = tk.Label(root, text="Ready. Click a color to send.", font=("Arial", 10), fg="#888888", bg=self.bg_color)
        self.status_label.pack(side=tk.BOTTOM, pady=15)

    def tegn_fargehjul(self):
        for vinkel in range(360):
            r, g, b = self.hsv_til_rgb(vinkel / 360.0, 1.0, 1.0)
            hex_farge = f"#{r:02X}{g:02X}{b:02X}"
            self.canvas.create_arc(self.center - self.radius, self.center - self.radius, self.center + self.radius, self.center + self.radius, start=vinkel, extent=1.5, fill=hex_farge, outline=hex_farge, width=2)
        
        self.canvas.create_oval(self.center - (self.radius - 35), self.center - (self.radius - 35), self.center + (self.radius - 35), self.center + (self.radius - 35), fill=self.bg_color, outline=self.bg_color)

    def hsv_til_rgb(self, h, s, v):
        if s == 0.0: return int(v*255), int(v*255), int(v*255)
        i = int(h*6.0); f = (h*6.0) - i
        p, q, t = v * (1.0 - s), v * (1.0 - s*f), v * (1.0 - s*(1.0-f))
        i = i % 6
        if i == 0: return int(v*255), int(t*255), int(p*255)
        if i == 1: return int(q*255), int(v*255), int(p*255)
        if i == 2: return int(p*255), int(v*255), int(t*255)
        if i == 3: return int(p*255), int(q*255), int(v*255)
        if i == 4: return int(t*255), int(p*255), int(p*255)
        if i == 5: return int(v*255), int(p*255), int(q*255)

    def klikk_palett(self, event):
        x, y = event.x - self.center, self.center - event.y
        avstand = math.sqrt(x**2 + y**2)
        if (self.radius - 40) <= avstand <= (self.radius + 5):
            vinkel_deg = math.degrees(math.atan2(y, x))
            if vinkel_deg < 0: vinkel_deg += 360
            r, g, b = self.hsv_til_rgb(vinkel_deg / 360.0, 1.0, 1.0)
            self.send_vrgb_command(f"{r:02X}{g:02X}{b:02X}")

    def send_vrgb_command(self, hex_color):
        self.current_hex = hex_color
        target_brightness = BRIGHTNESS_STAGES[self.brightness_index]
        try:
            subprocess.run(["sudo", "vrgb", "set", self.current_hex, str(target_brightness)], check=True)
            self.status_label.config(text=f"Active color: vrgb set {self.current_hex} {target_brightness}", fg="#00FF00")
        except:
            self.status_label.config(text="Error: Could not run vrgb. Check sudoers rule!", fg="#FF0000")

    def adjust_brightness_step(self, increment):
        """Steps through the 4 explicit levels (0, 33, 66, 100) bound checked."""
        new_index = self.brightness_index + increment
        if 0 <= new_index < len(BRIGHTNESS_STAGES):
            self.brightness_index = new_index
            target_brightness = BRIGHTNESS_STAGES[self.brightness_index]
            
            cmd = ["sudo", "vrgb", "set", self.current_hex, str(target_brightness)]
            try:
                subprocess.run(cmd, check=True)
                self.status_label.config(text=f"Brightness set to {target_brightness}%", fg="#00FF00")
            except Exception:
                self.status_label.config(text="Error: Check command syntax or sudoers!", fg="#FF0000")

if __name__ == "__main__":
    root = tk.Tk()
    app = VrgbCircularApp(root)
    root.mainloop()

