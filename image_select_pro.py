#!/usr/bin/env python3
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

IMG_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

def get_image_files(directory):
    """Recursively collect all image files from directory."""
    images = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(IMG_EXTS):
                images.append(os.path.join(root, f))
    return images

class ImageViewer:
    def __init__(self, master, images):
        self.master = master
        self.images = images
        self.total = len(images)
        self.current = 0
        self.marked = set()

        master.title("Image Reviewer – Mark & Next")
        master.geometry("900x700")

        # Top bar
        top = tk.Frame(master)
        top.pack(pady=5, fill=tk.X)
        self.lbl_info = tk.Label(top, text="")
        self.lbl_info.pack(side=tk.LEFT, padx=10)
        self.lbl_marked = tk.Label(top, text="Marked: 0", fg="red")
        self.lbl_marked.pack(side=tk.RIGHT, padx=10)

        # Canvas for image with scrollbars
        canvas_frame = tk.Frame(master)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.canvas = tk.Canvas(canvas_frame)
        scroll_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scroll_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.img_label = tk.Label(self.inner)
        self.img_label.pack(pady=10)

        # Navigation buttons
        nav = tk.Frame(master)
        nav.pack(pady=10)
        self.btn_prev = tk.Button(nav, text="◀ Previous", command=self.prev_image, width=10)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        self.btn_next = tk.Button(nav, text="Next ▶", command=self.next_image, width=10)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        self.btn_mark = tk.Button(nav, text="🗑️ Mark & Next", command=self.mark_and_next, bg="orange", width=15)
        self.btn_mark.pack(side=tk.LEFT, padx=20)

        # Status bar
        self.status = tk.Label(master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Action buttons
        action = tk.Frame(master)
        action.pack(pady=10)
        self.btn_delete = tk.Button(action, text="Delete Marked & Exit", command=self.confirm_delete, bg="red", fg="white")
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        self.btn_save = tk.Button(action, text="Save Marked List", command=self.save_list)
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.load_image()

    def load_image(self):
        if not (0 <= self.current < self.total):
            return
        path = self.images[self.current]
        self.current_path = path
        try:
            pil_img = Image.open(path)
            pil_img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(pil_img)
            self.img_label.config(image=self.tk_img)
            self.lbl_info.config(text=f"Image {self.current+1}/{self.total}\n{os.path.basename(path)}")
        except Exception as e:
            self.img_label.config(image='', text=f"Error: {e}")
            self.lbl_info.config(text=f"Error: {path}")
        self.update_mark_display()
        self.status.config(text=f"Path: {path}")

    def update_mark_display(self):
        cnt = len(self.marked)
        self.lbl_marked.config(text=f"Marked: {cnt}")
        if self.current_path in self.marked:
            self.btn_mark.config(text="✅ Unmark", bg="lightgreen")
        else:
            self.btn_mark.config(text="🗑️ Mark & Next", bg="orange")

    def mark_and_next(self):
        if self.current_path in self.marked:
            self.marked.remove(self.current_path)
            self.update_mark_display()
        else:
            self.marked.add(self.current_path)
            self.update_mark_display()
            self.next_image()

    def prev_image(self):
        if self.current > 0:
            self.current -= 1
            self.load_image()
        else:
            messagebox.showinfo("Info", "First image reached.")

    def next_image(self):
        if self.current < self.total - 1:
            self.current += 1
            self.load_image()
        else:
            self.end_reached()

    def end_reached(self):
        cnt = len(self.marked)
        if cnt == 0:
            messagebox.showinfo("Done", "You reviewed all images. No files marked.")
            self.master.quit()
        else:
            ans = messagebox.askyesno("End of slideshow",
                                      f"You marked {cnt} file(s) for deletion.\nDelete them now?")
            if ans:
                self.delete_marked()
            else:
                self.save_list()
            self.master.quit()

    def confirm_delete(self):
        cnt = len(self.marked)
        if cnt == 0:
            messagebox.showinfo("Info", "No files marked for deletion.")
            return
        if messagebox.askyesno("Confirm Delete", f"Permanently delete {cnt} marked file(s)?"):
            self.delete_marked()
            self.master.quit()

    def delete_marked(self):
        deleted = 0
        failed = 0
        for path in self.marked:
            try:
                os.remove(path)
                deleted += 1
            except Exception as e:
                print(f"Failed: {path} - {e}")
                failed += 1
        messagebox.showinfo("Done", f"Deleted {deleted} files. Failed: {failed}")

    def save_list(self):
        if not self.marked:
            messagebox.showinfo("Info", "No marked files.")
            return
        filename = "marked_for_deletion.txt"
        with open(filename, "w") as f:
            for p in self.marked:
                f.write(p + "\n")
        messagebox.showinfo("Saved", f"Saved {len(self.marked)} paths to {filename}")

def select_directory():
    """Create a popup to select directory either by entry or browse."""
    win = tk.Tk()
    win.title("Select Directory")
    win.geometry("500x150")
    win.resizable(False, False)

    tk.Label(win, text="Enter directory path or browse:").pack(pady=5)
    entry = tk.Entry(win, width=60)
    entry.pack(pady=5)

    path_var = tk.StringVar()

    def browse():
        d = filedialog.askdirectory()
        if d:
            entry.delete(0, tk.END)
            entry.insert(0, d)
            path_var.set(d)

    tk.Button(win, text="Browse", command=browse).pack(pady=5)

    def ok():
        path = entry.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Invalid directory path.")
            return
        path_var.set(path)
        win.quit()

    tk.Button(win, text="OK", command=ok).pack(pady=5)

    win.mainloop()
    win.destroy()
    return path_var.get() if path_var.get() else None

def select_sample_size():
    """Ask user how many images to sample."""
    win = tk.Tk()
    win.title("Sample Size")
    win.geometry("300x150")
    win.resizable(False, False)

    tk.Label(win, text="How many images to load?").pack(pady=10)
    var = tk.StringVar(value="100")
    choices = ["ALL", "10", "100", "500", "1000"]
    combobox = ttk.Combobox(win, textvariable=var, values=choices, state="readonly")
    combobox.pack(pady=5)

    result = [None]
    def ok():
        result[0] = var.get()
        win.quit()
    tk.Button(win, text="OK", command=ok).pack(pady=10)

    win.mainloop()
    win.destroy()
    return result[0]

def main():
    # Step 1: Get directory
    directory = select_directory()
    if not directory:
        print("No directory selected. Exiting.")
        return

    # Step 2: Get sample size
    sample_choice = select_sample_size()
    if not sample_choice:
        print("No sample size selected. Exiting.")
        return

    print(f"Scanning for images in {directory} ...")
    all_images = get_image_files(directory)
    total_found = len(all_images)
    print(f"Found {total_found} image files.")

    if total_found == 0:
        messagebox.showerror("Error", "No image files found in selected directory.")
        return

    # Sample images based on choice
    if sample_choice == "ALL":
        selected = all_images
    else:
        try:
            n = int(sample_choice)
            if n >= total_found:
                selected = all_images
            else:
                selected = random.sample(all_images, n)
        except ValueError:
            selected = all_images

    print(f"Loading {len(selected)} images into viewer...")
    root = tk.Tk()
    app = ImageViewer(root, selected)
    root.mainloop()

if __name__ == "__main__":
    main()
