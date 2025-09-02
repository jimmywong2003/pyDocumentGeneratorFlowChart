#!/usr/bin/env python3
"""
Mermaid Chart Generator - GUI Interface
Graphical user interface for converting Markdown files with Mermaid diagrams.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path

class MermaidGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mermaid Chart Generator")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.getcwd())
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Ready")
        
        # Configure styles
        self.setup_styles()
        
        # Create interface
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 9))
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header
        header = ttk.Label(main_frame, text="Mermaid Chart Generator", 
                          style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Markdown File:").grid(row=1, column=0, 
                                                         sticky=tk.W, pady=5)
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(input_frame, textvariable=self.input_file).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse...", 
                  command=self.browse_input_file).grid(row=0, column=1)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=2, column=0, 
                                                            sticky=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_dir).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="Browse...", 
                  command=self.browse_output_dir).grid(row=0, column=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="Generate DOCX + Charts", 
                  command=self.generate_docx).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Export Charts Only", 
                  command=self.export_charts_only).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear", 
                  command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        ttk.Label(main_frame, text="Progress:").grid(row=4, column=0, 
                                                    sticky=tk.W, pady=(20, 5))
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), 
                           pady=(20, 5))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress,
                                           maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Label(progress_frame, textvariable=self.progress).grid(
            row=0, column=1, padx=(5, 0))
        
        # Status area
        ttk.Label(main_frame, text="Status:").grid(row=5, column=0, 
                                                  sticky=tk.W, pady=(10, 5))
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), 
                         pady=(10, 5))
        status_frame.columnconfigure(0, weight=1)
        
        ttk.Label(status_frame, textvariable=self.status, 
                 style='Status.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Log area
        ttk.Label(main_frame, text="Log:").grid(row=6, column=0, 
                                               sticky=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, 
                                                 wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.grid(row=6, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=(10, 0))
        
        # Configure row weights for main frame
        main_frame.rowconfigure(6, weight=1)
        
    def browse_input_file(self):
        """Browse for input Markdown file"""
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Set default output directory to same as input file
            self.output_dir.set(os.path.dirname(filename))
            
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if directory:
            self.output_dir.set(directory)
            
    def clear_fields(self):
        """Clear all input fields"""
        self.input_file.set("")
        self.output_dir.set(os.getcwd())
        self.progress.set(0)
        self.status.set("Ready")
        self.log_text.delete(1.0, tk.END)
        
    def log_message(self, message):
        """Add message to log area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status message"""
        self.status.set(message)
        self.log_message(message)
        self.root.update_idletasks()
        
    def update_progress(self, value):
        """Update progress bar"""
        self.progress.set(value)
        self.root.update_idletasks()
        
    def run_command_thread(self, command, description):
        """Run command in separate thread"""
        def thread_function():
            try:
                self.update_status(f"Starting {description}...")
                self.update_progress(10)
                
                # Run the command
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Read output in real-time
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log_message(output.strip())
                
                # Check return code
                return_code = process.wait()
                if return_code == 0:
                    self.update_status(f"✓ {description} completed successfully")
                    self.update_progress(100)
                    messagebox.showinfo("Success", f"{description} completed successfully!")
                else:
                    error_output = process.stderr.read()
                    self.log_message(f"Error: {error_output}")
                    self.update_status(f"✗ {description} failed")
                    messagebox.showerror("Error", f"{description} failed:\n{error_output}")
                    
            except Exception as e:
                self.update_status(f"✗ Error during {description}")
                self.log_message(f"Exception: {str(e)}")
                messagebox.showerror("Error", f"Exception during {description}:\n{str(e)}")
            finally:
                self.update_progress(0)
                
        # Start the thread
        thread = threading.Thread(target=thread_function)
        thread.daemon = True
        thread.start()
        
    def generate_docx(self):
        """Generate DOCX document with embedded charts"""
        if not self.validate_inputs():
            return
            
        input_file = self.input_file.get()
        output_dir = self.output_dir.get()
        
        # Build command
        cmd = f'python export_document.py "{input_file}" --output-dir "{output_dir}"'
        self.run_command_thread(cmd, "DOCX generation")
        
    def export_charts_only(self):
        """Export only charts to PNG"""
        if not self.validate_inputs():
            return
            
        input_file = self.input_file.get()
        output_dir = self.output_dir.get()
        
        # Build command
        cmd = f'python export_flowcharts_only.py "{input_file}" --output-dir "{output_dir}"'
        self.run_command_thread(cmd, "Chart export")
        
    def validate_inputs(self):
        """Validate input fields"""
        input_file = self.input_file.get()
        output_dir = self.output_dir.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input Markdown file")
            return False
            
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file does not exist:\n{input_file}")
            return False
            
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return False
            
        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create output directory:\n{str(e)}")
            return False
            
        return True

def main():
    """Main function"""
    root = tk.Tk()
    app = MermaidGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
