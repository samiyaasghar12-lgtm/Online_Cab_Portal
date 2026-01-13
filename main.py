import tkinter as tk
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import os
import random

root = tk.Tk()
root.title("Online Cab Portal")
root.geometry("1300x820")
root.configure(bg="#ffffff")

# Exact neon color of this drive has been matched
SERVICES = {
    "Yango": {"main": "#ff0000", "base": 60, "types": ["Toyota Vitz", "Suzuki Swift", "Corolla"], "logo": "yango_logo.png"},
    "Uber": {"main": "#000000", "base": 55, "types": ["Mehran", "Alto", "Toyota Corolla"], "logo": "uber_logo.png"},
    "Careem": {"main": "#00af41", "base": 58, "types": ["Suzuki WagonR", "Toyota Yaris", "Honda Civic"], "logo": "careem_logo.png"},
    "InDrive": {"main": "#b5ff00", "base": 50, "types": ["Mercedes C-Class", "Honda City", "Toyota Aqua"], "logo": "indrive_logo.png"}
}

selected_service = tk.StringVar(value="Yango")
selected_ride_idx = tk.IntVar(value=-1)
logo_refs, image_labels, detail_labels, image_frames = [], [], [], []

def show_custom_popup(title, message, color):
    popup = tk.Toplevel(root)
    popup.geometry("220x155+415+510") 
    popup.configure(bg="white", bd=1, relief="solid")
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    tk.Frame(popup, bg=color, height=3).pack(fill="x")
    tk.Label(popup, text=title, font=("Arial", 9, "bold"), bg="white", fg="black").pack(pady=(10, 2))
    tk.Label(popup, text=message, font=("Arial", 8), bg="white", justify="center", wraplength=200).pack(pady=5)
    tk.Button(popup, text="OK", width=7, bg="black", fg="white", font=("Arial", 8, "bold"), command=popup.destroy, bd=0).pack(pady=10)

def update_prices(event=None):
    p, d = pickup_entry.get().strip(), dest_entry.get().strip()
    if p and d:
        distance = random.randint(25, 50) 
        s = selected_service.get()
        multipliers = [1.0, 1.5, 2.5]
        for i in range(3):
            fare = int(distance * SERVICES[s]["base"] * multipliers[i])
            if fare < 1500: fare = 1500 + (i * 200) 
            detail_labels[i].config(text=f"{SERVICES[s]['types'][i]}\nFare Price: {fare}")

def cancel_ride():
    pickup_entry.delete(0, tk.END)
    dest_entry.delete(0, tk.END)
    selected_ride_idx.set(-1)
    for f in image_frames:
        f.config(highlightthickness=1, highlightbackground="#eee")
    map_view.set_position(24.8607, 67.0011)

def confirm_booking():
    p = pickup_entry.get().strip()
    d = dest_entry.get().strip()
    idx = selected_ride_idx.get()
    s = selected_service.get()
    theme_color = SERVICES[s]["main"]

    if not p or not d:
        show_custom_popup("ATTENTION", "Please enter all locations to proceed.", "#e74c3c")
        return
    if idx == -1:
        show_custom_popup("ATTENTION", "Please choose a ride to proceed.", "#e74c3c")
        return

    map_view.set_address(p, marker=True)
    full_text = detail_labels[idx].cget("text")
    amount = full_text.split("Fare Price: ")[1]
    msg = f"Brand: {s}\nModel: {SERVICES[s]['types'][idx]}\nFare: {amount}\nArriving in Few Minutes"
    show_custom_popup("RIDE CONFIRMED", msg, theme_color)

def select_card(idx, col):
    selected_ride_idx.set(idx)
    for i, f in enumerate(image_frames):
        f.config(highlightthickness=4 if i == idx else 1, highlightbackground=col if i == idx else "#eee")

def change_service(name):
    selected_service.set(name)
    theme = SERVICES[name]
    logo_bar.config(bg=theme["main"])
    # button color match logic for this indrive has been implemented
    confirm_btn.config(bg=theme["main"], fg="black" if name == "InDrive" else "white")
    selected_ride_idx.set(-1)
    for i in range(3):
        path = f"{name.lower()}{i+1}.png"
        if os.path.exists(path):
            img = Image.open(path).resize((220, 110), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img); image_labels[i].config(image=photo); image_labels[i].image = photo
        base_fare = 1500 + (i * 1000)
        detail_labels[i].config(text=f"{theme['types'][i]}\nFare Price: {base_fare}")
        image_frames[i].config(highlightthickness=1, highlightbackground="#eee")

# UI Layout remains exactly same
left_panel = tk.Frame(root, bg="white", padx=25)
left_panel.place(relx=0, rely=0, relwidth=0.7, relheight=1)

logo_bar = tk.Frame(left_panel, height=60, bg="#ff0000")
logo_bar.pack(fill="x", pady=(0, 15))
logo_inner = tk.Frame(logo_bar, bg="white", padx=5, pady=5)
logo_inner.place(relx=0.5, rely=0.5, anchor="center")

for name in SERVICES.keys():
    logo_path = SERVICES[name]["logo"]
    if os.path.exists(logo_path):
        l_img = Image.open(logo_path).resize((80, 30), Image.LANCZOS)
        l_photo = ImageTk.PhotoImage(l_img); logo_refs.append(l_photo)
        tk.Button(logo_inner, image=l_photo, bg="white", bd=0, command=lambda n=name: change_service(n)).pack(side="left", padx=10)

tk.Label(left_panel, text="PICKUP LOCATION", font=("Arial", 8, "bold"), bg="white", fg="#333").pack(anchor="w")
pickup_entry = tk.Entry(left_panel, font=("Arial", 11), bg="#f4f4f4", fg="black", bd=0)
pickup_entry.pack(fill="x", ipady=10, pady=(5, 15))
pickup_entry.bind("<FocusOut>", update_prices)

tk.Label(left_panel, text="DROP-OFF LOCATION", font=("Arial", 8, "bold"), bg="white", fg="#333").pack(anchor="w")
dest_entry = tk.Entry(left_panel, font=("Arial", 11), bg="#f4f4f4", fg="black", bd=0)
dest_entry.pack(fill="x", ipady=10, pady=(5, 15))
dest_entry.bind("<FocusOut>", update_prices)

card_container = tk.Frame(left_panel, bg="white")
card_container.pack(pady=10)
for i in range(3):
    f = tk.Frame(card_container, bg="white", highlightthickness=1, highlightbackground="#eee")
    f.grid(row=0, column=i, padx=5); image_frames.append(f)
    lbl = tk.Label(f, bg="white", width=220, height=110); lbl.pack(); image_labels.append(lbl)
    d_lbl = tk.Label(f, font=("Arial", 9, "bold"), bg="white", pady=5); d_lbl.pack(); detail_labels.append(d_lbl)
    for w in (f, lbl, d_lbl):
        w.bind("<Button-1>", lambda e, x=i: select_card(x, SERVICES[selected_service.get()]["main"]))

btn_frame = tk.Frame(left_panel, bg="white")
btn_frame.pack(side="bottom", pady=60) 

confirm_btn = tk.Button(btn_frame, text="CONFIRM BOOKING", width=22, height=2, font=("Arial", 10, "bold"), bd=0, command=confirm_booking)
confirm_btn.grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="CANCEL RIDE", width=22, height=2, bg="black", fg="white", font=("Arial", 10, "bold"), bd=0, command=cancel_ride).grid(row=0, column=1, padx=10)

map_view = TkinterMapView(root)
map_view.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
map_view.set_position(24.8607, 67.0011)

change_service("Yango")
root.mainloop() 

