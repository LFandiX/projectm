import tkinter as tk
from tkinter import ttk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("My Tkinter Workspace")
    root.geometry("800x600")

    # Create a frame for the layout
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a label
    label = ttk.Label(frame, text="Welcome to My Tkinter Workspace!")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    # Add an entry field
    entry = ttk.Entry(frame, width=50)
    entry.grid(row=1, column=0, columnspan=2, pady=10)

    # Add a button
    button = ttk.Button(frame, text="Click Me")
    button.grid(row=2, column=0, pady=10)

    # Add a quit button
    quit_button = ttk.Button(frame, text="Quit", command=root.quit)
    quit_button.grid(row=2, column=1, pady=10)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
