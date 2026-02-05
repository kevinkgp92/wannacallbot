import customtkinter as ctk
from PIL import Image
import os
import sys

class UpdateWindow(ctk.CTkToplevel):
    def __init__(self, master, current_version, new_version, changelog_text, on_update_confirm):
        super().__init__(master)
        
        self.title(f"Actualización Disponible: v{new_version}")
        self.geometry("600x450")
        self.resizable(False, False)
        self.on_update_confirm = on_update_confirm
        
        # Make it modal-ish
        self.attributes("-topmost", True)
        self.after(10, self.focus_force)
        self.grab_set()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🚀 Nueva Versión Lista", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left")
        
        self.ver_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"v{current_version} ➔ v{new_version}", 
            font=ctk.CTkFont(size=14),
            text_color="#gray70"
        )
        self.ver_label.pack(side="right")

        # Changelog Area
        self.changelog_frame = ctk.CTkFrame(self, fg_color="#1a1a24", corner_radius=10)
        self.changelog_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.changelog_text = ctk.CTkTextbox(
            self.changelog_frame, 
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            wrap="word",
            border_width=0
        )
        self.changelog_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.changelog_text.insert("0.0", changelog_text)
        self.changelog_text.configure(state="disabled")

        # Progress Area (Hidden initially)
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, mode="indeterminate", height=10)
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Preparando actualización...", font=ctk.CTkFont(size=12))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame, 
            text="Ahora No", 
            fg_color="transparent",
            border_width=1,
            text_color="#ff5555",
            border_color="#ff5555",
            hover_color="#331111",
            width=120,
            command=self.destroy
        )
        self.cancel_button.pack(side="left")
        
        self.update_button = ctk.CTkButton(
            self.button_frame, 
            text="Actualizar y Reiniciar 🚀", 
            fg_color="#2eb362",
            hover_color="#248f4e",
            text_color="white",
            font=ctk.CTkFont(weight="bold"),
            command=self._start_update_ui
        )
        self.update_button.pack(side="right", expand=True, fill="x", padx=(20, 0))

    def _start_update_ui(self):
        """Changes the UI to show progress and calls the actual update logic."""
        self.update_button.configure(state="disabled", text="Actualizando...")
        self.cancel_button.configure(state="disabled")
        
        # Show progress bar
        self.changelog_frame.grid_forget()
        self.progress_frame.grid(row=1, column=0, padx=40, pady=60, sticky="nsew")
        self.progress_label.pack(pady=(0, 10))
        self.progress_bar.pack(fill="x")
        self.progress_bar.start()
        
        # Give UI time to update
        self.after(500, self.on_update_confirm)

    def set_status(self, text):
        """Updates the progress label text."""
        self.progress_label.configure(text=text)
        self.update()
