import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont
import random

# ================= THEMES =================
THEMES = {
    "Cute": {
        "bg": (255, 235, 240),
        "text": (160, 40, 80),
        "heart": (255, 120, 150)
    },
    "Navy": {
        "bg": (12, 28, 52),
        "text": (230, 240, 255),
        "heart": (90, 150, 220)
    },
    "Night": {
        "bg": (20, 20, 30),
        "text": (240, 240, 245),
        "heart": (200, 80, 120)
    }
}

GIF_FRAMES = 40
FONT_SIZE = 34

try:
    FONT = ImageFont.truetype("arial.ttf", FONT_SIZE)
except:
    FONT = ImageFont.load_default()

# ================= GIF GENERATION =================
def generate_gif():
    text = message_entry.get().strip()
    theme_name = theme_var.get()
    animation = anim_var.get()

    if not text:
        messagebox.showwarning("Missing Input", "Please enter a message")
        return

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    width, height = int(screen_w * 0.6), int(screen_h * 0.6)

    theme = THEMES[theme_name]
    frames = []

    hearts = [[random.randint(40, width-40), height + random.randint(0, 200)]
              for _ in range(10)]

    for i in range(GIF_FRAMES):
        img = Image.new("RGB", (width, height), theme["bg"])
        draw = ImageDraw.Draw(img)

        # ---- Text animation ----
        if animation == "Fade":
            alpha = int(255 * (i / GIF_FRAMES))
            txt = Image.new("RGBA", img.size, (0,0,0,0))
            tdraw = ImageDraw.Draw(txt)
            tdraw.text((width//6, height//2),
                       text, fill=theme["text"] + (alpha,), font=FONT)
            img = Image.alpha_composite(img.convert("RGBA"), txt).convert("RGB")

        elif animation == "Slide":
            x = int(-width + (i * (width / GIF_FRAMES)))
            draw.text((x, height//2),
                      text, fill=theme["text"], font=FONT)

        else:  # Bounce
            y = height//2 + int(12 * (-1)**i)
            draw.text((width//6, y),
                      text, fill=theme["text"], font=FONT)

        # ---- Floating hearts ----
        for h in hearts:
            h[1] -= 2
            if h[1] < -20:
                h[0] = random.randint(40, width-40)
                h[1] = height + random.randint(0, 150)
            draw.text((h[0], h[1]), "♥",
                      fill=theme["heart"], font=FONT)

        frames.append(img)

    frames[0].save(
        "custom_message.gif",
        save_all=True,
        append_images=frames[1:],
        duration=90,
        loop=0
    )

    messagebox.showinfo("Success", "GIF generated successfully!\nSaved as custom_message.gif")

# ================= UI =================
root = tk.Tk()
root.title("Message & GIF Studio")
root.state("zoomed")          # FULL SCREEN (Windows)
root.attributes("-fullscreen", True)  # fallback
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

# ---- Header ----
header = tk.Frame(root, bg="#1f2933", height=70)
header.pack(fill="x")

tk.Label(
    header,
    text="Message & GIF Studio",
    font=("Segoe UI", 22, "bold"),
    bg="#1f2933",
    fg="white"
).pack(side="left", padx=30)

tk.Label(
    header,
    text="Create customizable animated messages",
    font=("Segoe UI", 11),
    bg="#1f2933",
    fg="#cbd5e1"
).pack(side="left", padx=20)

# ---- Main Content ----
content = tk.Frame(root, bg="#f4f6f9")
content.pack(expand=True)

card = tk.Frame(content, bg="white", padx=40, pady=30)
card.pack(pady=60)

# Message input
tk.Label(card, text="Message",
         font=("Segoe UI", 11, "bold"),
         bg="white").grid(row=0, column=0, sticky="w")

message_entry = ttk.Entry(card, width=40, font=("Segoe UI", 12))
message_entry.grid(row=1, column=0, columnspan=2, pady=10)
message_entry.insert(0, "Always proud of you ⚓")

# Theme
tk.Label(card, text="Theme",
         font=("Segoe UI", 11, "bold"),
         bg="white").grid(row=2, column=0, sticky="w")

theme_var = tk.StringVar(value="Navy")
ttk.Combobox(card, textvariable=theme_var,
             values=list(THEMES.keys()),
             state="readonly").grid(row=3, column=0, pady=10)

# Animation
tk.Label(card, text="Animation",
         font=("Segoe UI", 11, "bold"),
         bg="white").grid(row=2, column=1, sticky="w")

anim_var = tk.StringVar(value="Fade")
ttk.Combobox(card, textvariable=anim_var,
             values=["Fade", "Slide", "Bounce"],
             state="readonly").grid(row=3, column=1, pady=10)

# Generate button
ttk.Button(
    card,
    text="Generate GIF",
    command=generate_gif
).grid(row=4, column=0, columnspan=2, pady=25)

# Footer
footer = tk.Frame(root, bg="#e5e7eb", height=30)
footer.pack(fill="x")

tk.Label(
    footer,
    text="Press ESC to exit full screen",
    font=("Segoe UI", 9),
    bg="#e5e7eb",
    fg="#374151"
).pack(pady=5)

root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
