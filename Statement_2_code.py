import tkinter as tk
from tkinter import messagebox

# Initialize window
root = tk.Tk()
root.title("Disaster Management Inventory")
root.geometry("800x600")

# Data lists
list1 = []  # Item names
list2 = []  # Quantities with units (e.g., 5kg)
list3 = []  # Locations

# --- Functions ---

# Add item to inventory
def add_item():
    item = entry_item.get()
    quantity = entry_quantity.get()
    location = entry_location.get()
    
    if item and quantity and location:
        list1.append(item)
        list2.append(quantity)
        list3.append(location)
        display_items()
        entry_item.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_location.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Display inventory
def display_items():
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "📦 Current Inventory:\n")
    output_box.insert(tk.END, "-"*70 + "\n")
    for i in range(len(list1)):
        output_box.insert(tk.END, f"{i+1}. {list1[i]} | Qty: {list2[i]} | Location: {list3[i]}\n")

# Dispatch item
def dispatch_item():
    index = entry_dispatch_index.get()
    amount = entry_dispatch_qty.get()
    
    if index.isdigit() and amount:
        idx = int(index) - 1
        if 0 <= idx < len(list1):
            # Get current quantity and unit
            current_qty_str = list2[idx]
            try:
                num_part = ''.join([c for c in current_qty_str if c.isdigit()])
                unit_part = ''.join([c for c in current_qty_str if not c.isdigit()])
                if not num_part:
                    raise ValueError
                current_qty = int(num_part)
                dispatch_num = int(''.join([c for c in amount if c.isdigit()]))
                dispatch_unit = ''.join([c for c in amount if not c.isdigit()])
                if dispatch_unit != unit_part:
                    messagebox.showwarning("Unit Mismatch", f"Expected unit '{unit_part}'.")
                    return
                if current_qty >= dispatch_num:
                    new_qty = current_qty - dispatch_num
                    list2[idx] = f"{new_qty}{unit_part}"
                    output_box.insert(tk.END, f"\n✅ Dispatched {dispatch_num}{unit_part} of {list1[idx]}.\n")
                else:
                    messagebox.showwarning("Stock Error", f"Only {current_qty}{unit_part} available.")
            except:
                messagebox.showerror("Format Error", "Quantities must have number+unit (e.g., 10kg).")
        else:
            messagebox.showerror("Error", "Invalid item number.")
    else:
        messagebox.showwarning("Input Error", "Enter valid numbers.")
    display_items()
    entry_dispatch_index.delete(0, tk.END)
    entry_dispatch_qty.delete(0, tk.END)

# FCFS strategy display
def fcfs_strategy():
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "📋 FCFS Dispatch Order:\n")
    output_box.insert(tk.END, "-"*70 + "\n")
    for i in range(len(list1)):
        output_box.insert(tk.END, f"{i+1}. {list1[i]} | Qty: {list2[i]} | Location: {list3[i]}\n")

# Priority strategy (lowest quantity first)
def priority_strategy():
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "⚡ Priority Dispatch Order (Low Qty First):\n")
    output_box.insert(tk.END, "-"*70 + "\n")
    try:
        combined = []
        for i in range(len(list1)):
            num_part = int(''.join([c for c in list2[i] if c.isdigit()]))
            unit_part = ''.join([c for c in list2[i] if not c.isdigit()])
            combined.append((list1[i], num_part, unit_part, list3[i]))
        sorted_items = sorted(combined, key=lambda x: x[1])
        for i, item in enumerate(sorted_items):
            output_box.insert(tk.END, f"{i+1}. {item[0]} | Qty: {item[1]}{item[2]} | Location: {item[3]}\n")
    except:
        messagebox.showerror("Error", "Ensure quantities have number+unit (e.g., 10kg).")

# --- Layout (Centered) ---

frame = tk.Frame(root)
frame.pack(pady=20)

# Input Labels and Entries
tk.Label(frame, text="Item Name").grid(row=0, column=0, padx=10, pady=5)
entry_item = tk.Entry(frame, width=20)
entry_item.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Quantity (e.g., 10kg)").grid(row=1, column=0, padx=10, pady=5)
entry_quantity = tk.Entry(frame, width=20)
entry_quantity.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Location").grid(row=2, column=0, padx=10, pady=5)
entry_location = tk.Entry(frame, width=20)
entry_location.grid(row=2, column=1, pady=5)

# Buttons Row 1
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Add Item", width=15, command=add_item).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Display Inventory", width=15, command=display_items).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="FCFS Strategy", width=15, command=fcfs_strategy).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Priority Strategy", width=15, command=priority_strategy).grid(row=0, column=3, padx=5)

# Dispatch Inputs
dispatch_frame = tk.Frame(root)
dispatch_frame.pack(pady=15)

tk.Label(dispatch_frame, text="Dispatch Item No.").grid(row=0, column=0, padx=10)
entry_dispatch_index = tk.Entry(dispatch_frame, width=10)
entry_dispatch_index.grid(row=0, column=1)

tk.Label(dispatch_frame, text="Quantity to Dispatch").grid(row=0, column=2, padx=10)
entry_dispatch_qty = tk.Entry(dispatch_frame, width=10)
entry_dispatch_qty.grid(row=0, column=3)

tk.Button(dispatch_frame, text="Dispatch Item", command=dispatch_item).grid(row=0, column=4, padx=10)

# Output Display Box
output_box = tk.Text(root, height=15, width=90)
output_box.pack(pady=20)

# Run GUI
root.mainloop()
