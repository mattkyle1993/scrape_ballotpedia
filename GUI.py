import tkinter as tk
from tkinter import scrolledtext

# Function to be executed on button press
def process_input():
    number = number_input.get()
    # Print and display the results
    result_str = f"Number: {number}, Choice: {'True' if true_false_var.get() else 'False'}"
    print(result_str)  # This goes to the console
    output_area.config(state=tk.NORMAL)
    output_area.insert(tk.END, result_str + "\n")
    output_area.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Simple GUI Program")

# Create a frame for the input
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Number input
tk.Label(frame, text="Enter a number:").pack(side=tk.LEFT)
number_input = tk.Entry(frame)
number_input.pack(side=tk.LEFT)

# True/False radio buttons
true_false_var = tk.BooleanVar()
true_false_var.set(True)  # Set default to True
tk.Radiobutton(frame, text="True", variable=true_false_var, value=True).pack(side=tk.LEFT)
tk.Radiobutton(frame, text="False", variable=true_false_var, value=False).pack(side=tk.LEFT)

# Button to execute the function
process_button = tk.Button(root, text="Process Input", command=process_input)
process_button.pack(pady=5)

# Text area for output
output_area = scrolledtext.ScrolledText(root, height=10, width=50, state=tk.DISABLED)
output_area.pack(padx=10, pady=10)

root.mainloop()
