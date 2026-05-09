#do not mess with imports, need for wokring with folders, paths and textensions
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

#dont mess with this, stores the file categories to be called on later
file_types = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "videos": [".mp4", ".mov", ".avi"],
    "music": [".mp3", ".wav"],
    "archives": [".zip", ".rar", ".7z"],
    "code": [".py", ".js", ".html", ".css", ".php", ".json", ".java", ".cpp"]
}
# choosing folder function 
#opens folder picker to choose a folder
def choose_folder():
    picked_folder = filedialog.askdirectory()  # asks to choose folder to save

    
    if picked_folder:  #validation to ensure folder picked
        
        folder_path.set(picked_folder) # saves picked folder

        
        status_text.set("folder Selected.") # updates status text from sidebar yet to be implemented 

       
        update_folder_summary() # refreshes count summary
        
#category decider function via extension checks
def get_category(filename):
    _, ext = os.path.splitext(filename.lower()) # splits filename into name and extension, makes it lowercase

    for category, extensions in file_types.items(): #goes through each category to list extension
        if ext in extensions:
            return category


    return "other" # validation for files not matched places in other

#file counter and update label 
def update_folder_summary():
    current_folder = folder_path.get() # pulls currently selected folder pathway

    if current_folder == "" or not os.path.exists(current_folder):#validation for blank folders or non existant
        folder_summary.config(text="no folder selected.")
        return

    count = 0 # ensures file counter starts at 0

    for item in os.listdir(current_folder): # loops through everything inside folder 
        
        full_path = os.path.join(current_folder, item) # builds path to current item

    
        if os.path.isfile(full_path): # ensures count only increases if its a file not a folder
            count += 1

    
    folder_summary.config(text=f"files found: {count}") # updates file countlabel
    
#main section file organiser function
def organise_files(): #move file into category based on extension function
    current_folder = folder_path.get() # pulls current folder path

    if current_folder == "": # no folder selected validation 
        messagebox.showwarning("no folder selected", "please choose a Folder first")
        return

    if not os.path.exists(current_folder): #if invalid path show error and stop 
        messagebox.showerror("invalid folder", "the selected folder does not Exist")
        return

    answer = messagebox.askyesno( # ask confirmation to move file
        "confirm organisation",
        "are you sure you want to organise the files in this folder?"
    )

    if not answer: # if no cancel return
        status_text.set("cancelled")
        return

    moved = 0 # shows moved file count
    skipped = 0 # shows folder skip count 
    category_totals = {} # store total for category 

    status_text.set("working on files...") #updates status for ui 
    output_box.config(state="normal") # turns on output box for texts
    output_box.delete("1.0", tk.END) # clears old text in output boxes

    for item in os.listdir(current_folder): # loops every item in folder
        old_path = os.path.join(current_folder, item)#builds original path

        if os.path.isdir(old_path):#skips item in folder, only want to move files
            skipped += 1
            continue
        folder_name = get_category(item)#figures out category folder for files
        new_folder = os.path.join(current_folder, folder_name)#building new path and folder
        if not os.path.exists(new_folder):#force create folder if not existing
            os.makedirs(new_folder)
        new_path = os.path.join(new_folder, item)#builds destination path for files
        try: # try to move files, moves from old location to new set path

            shutil.move(old_path, new_path)

            
            output_box.insert(tk.END, f"moved: {item} -> {folder_name}\n")#success message

            
            moved += 1 # increases moved file every success

            
            category_totals[folder_name] = category_totals.get(folder_name, 0) + 1 #increase category count per success

        except Exception as err: # when something goes wrong show error in box validation
            output_box.insert(tk.END, f"could not move {item}: {err}\n")

    output_box.insert(tk.END, "\nsummary\n") # builds summary section 
    output_box.insert(tk.END, "--------------------\n")

    for category, total in category_totals.items(): # shows the total for category
        output_box.insert(tk.END, f"{category}: {total}\n")

    output_box.insert(tk.END, f"\ntotal moved: {moved}\n") # shows moved files total count 
    output_box.insert(tk.END, f"skipped folders: {skipped}\n") # shows the skipped folder count
    output_box.config(state="disabled") # turn off output box to prevent typing from user 
    status_text.set("completed")#status update when complete
    update_folder_summary() # refreshes folder summary when files moved

#clear function to reset app display back to default 
def clear_all():
    folder_path.set("")#clear the stored pathways
    status_text.set("ready")#resets status
    folder_summary.config(text="no folder selected")#resets summary labels
    output_box.config(state="normal")#turns on output box to be cleared
    output_box.delete("1.0", tk.END)#deletes text in box
    output_box.config(state="disabled") #closes output box again after clear
    
#building main app window
root = tk.Tk() # this creates main application window
root.title("file manager")#gives the window a title
root.geometry("980x620")#sets the window size on open
root.minsize(860, 560)#sets minimum size of window
root.configure(bg="#f3f4f6") # sets background colour 

#all styling colour options here ------------------------------------------------------------------------ 
bg_main = "#f3f4f6"  # main app bg
sidebar_bg = "#1f2937"  # sidebars bg 
sidebar_text = "#f9fafb"  # sidebar text
sidebar_muted = "#cbd5e1" # second text for sidebar
panel_bg = "#ffffff" # panel bg 
panel_border = "#d1d5db"  # border colours
dark_text = "#111827"   # main text to stand out ---- 
muted_text = "#6b7280"  # secondary texts
accent = "#0f766e"  # accent button covers
accent_hover = "#115e59" # hover button colour
secondary = "#334155" # secondary button colour
secondary_hover = "#1e293b" # hover scondary button 

#font styling ---------------------------------------------
title_font = ("Arial", 16, "bold")   
head_font = ("Arial", 11, "bold")    
normal_font = ("Arial", 10)          
small_font = ("Arial", 9)            
button_font = ("Arial", 10, "bold")  

#main container and frame
main_frame = tk.Frame(root, bg=bg_main) # creates main frame to hold sidebar and workspace in 
main_frame.pack(fill="both", expand=True) # forces frame to fill window size

#sidebar frame and container 
sidebar = tk.Frame(main_frame, bg=sidebar_bg, width=260)
sidebar.pack(side="left", fill="y") # forces container to left to create sidebar
sidebar.pack_propagate(False) # stops sidebar shrinking 
sidebar_top = tk.Frame(sidebar, bg=sidebar_bg, padx=20, pady=20)#creates top label in sidebar
sidebar_top.pack(fill="x")#fill container stretch 

app_title = tk.Label( # creates main title for the app
    sidebar_top,#forces label in top bar
    text="file manager", #title text -----------
    font=title_font,          
    bg=sidebar_bg,           
    fg=sidebar_text           
)
app_title.pack(anchor="w") #forces label to align on the left

#title subtitle --- 
app_subtitle = tk.Label(
    sidebar_top,
    text="automatically sort your files into folders here",
    font=normal_font,
    bg=sidebar_bg,
    fg=sidebar_muted
)
app_subtitle.pack(anchor="w", pady=(6, 20)) 

#creates button to open folder
folder_button = tk.Button(
    sidebar_top,          
    text="choose folder", #button label ---
    command=choose_folder, #runs prior function when clicked
    font=button_font,            
    bg=accent,                   
    fg="white",                 
    activebackground=accent_hover,  
    activeforeground="white",        
    relief="flat",              
    padx=10,                     
    pady=8                  
)
folder_button.pack(fill="x", pady=(0, 10)) 

#creates organise button 
organise_button = tk.Button(
    sidebar_top,
    text="organise files",
    command=organise_files,
    font=button_font,
    bg=secondary,
    fg="white",
    activebackground=secondary_hover,
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=8
)
organise_button.pack(fill="x", pady=(0, 10))

#clear button 
clear_button = tk.Button(
    sidebar_top,
    text="clear",
    command=clear_all,
    font=button_font,
    bg="#475569",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    relief="flat",
    padx=10,
    pady=8
)
clear_button.pack(fill="x")

sidebar_info = tk.Frame(sidebar, bg=sidebar_bg, padx=20, pady=20) #builds section in sidebar for info and status
sidebar_info.pack(fill="x")


info_heading = tk.Label(#folder summary label
    sidebar_info,
    text="folder summary",
    font=head_font,
    bg=sidebar_bg,
    fg=sidebar_text
)
info_heading.pack(anchor="w", pady=(0, 10))

folder_path = tk.StringVar() # stores folder path 

folder_summary = tk.Label( # label for folder sumamry 
    sidebar_info,
    text="no folder selected",
    font=normal_font,
    bg=sidebar_bg,
    fg=sidebar_muted,
    justify="left"
)
folder_summary.pack(anchor="w")

status_heading = tk.Label( # heading for status bit
    sidebar_info,
    text="status",
    font=head_font,
    bg=sidebar_bg,
    fg=sidebar_text
)
status_heading.pack(anchor="w", pady=(24, 10))

status_text = tk.StringVar(value="ready") # stores status message

status_label = tk.Label( # label for status text
    sidebar_info,
    textvariable=status_text,
    font=normal_font,
    bg=sidebar_bg,
    fg=sidebar_muted,
    justify="left"
)
status_label.pack(anchor="w")

sidebar_footer = tk.Frame(sidebar, bg=sidebar_bg, padx=20, pady=20)#creates footer section in sidebar 
sidebar_footer.pack(side="bottom", fill="x") # stretches and pins footer

footer_label = tk.Label( # creates label at bottom throw s0 number in
    sidebar_footer,
    text="S0305360",
    font=small_font,
    bg=sidebar_bg,
    fg="#94a3b8"
)
footer_label.pack(anchor="w")

#main workspace area on the right 
workspace = tk.Frame(main_frame, bg=bg_main, padx=20, pady=20) # creates workspace on right
workspace.pack(side="left", fill="both", expand=True) # puts next to sidebar and forces to fill to winddow

header_label = tk.Label( #label for area
    workspace,
    text="workspace",
    font=("Arial", 14, "bold"),
    bg=bg_main,
    fg=dark_text
)
header_label.pack(anchor="w")

header_text = tk.Label( # explanation text under heading
    workspace,
    text="select a folder, then sort the files into categories",
    font=normal_font,
    bg=bg_main,
    fg=muted_text
)
header_text.pack(anchor="w", pady=(4, 16))

#creates the panel to show selected folder
folder_panel = tk.Frame(
    workspace,
    bg=panel_bg,
    highlightbackground=panel_border,
    highlightthickness=1
)
folder_panel.pack(fill="x", pady=(0, 16))
folder_panel_inner = tk.Frame(folder_panel, bg=panel_bg, padx=14, pady=12) # styling inner frame
folder_panel_inner.pack(fill="both", expand=True)
folder_panel_title = tk.Label( # panel title here 
    folder_panel_inner,
    text="selected folder",
    font=head_font,
    bg=panel_bg,
    fg=dark_text
)
folder_panel_title.pack(anchor="w")
folder_entry = tk.Entry( # creates box link to folder path to show selected folder
    folder_panel_inner,
    textvariable=folder_path,
    font=normal_font,
    bg="#f9fafb",
    fg=dark_text,
    insertbackground=dark_text,
    relief="solid",
    bd=1
)
folder_entry.pack(fill="x", pady=(10, 0))

middle_row = tk.Frame(workspace, bg=bg_main) # creates middle row to hold panels neatly
middle_row.pack(fill="both", expand=True)#forces to fill remaining space
#category panel
categories_panel = tk.Frame( # creates category panel on the left side of middle section 
    middle_row,
    bg=panel_bg,
    highlightbackground=panel_border,
    highlightthickness=1,
    width=260
)
categories_panel.pack(side="left", fill="y", padx=(0, 16))
categories_panel.pack_propagate(False) # forces to fit content, stops shrink
categories_inner = tk.Frame(categories_panel, bg=panel_bg, padx=14, pady=12) # styling inner frame
categories_inner.pack(fill="both", expand=True)
categories_title = tk.Label( # panel title 
    categories_inner,
    text="sorting categories",
    font=head_font,
    bg=panel_bg,
    fg=dark_text
)
categories_title.pack(anchor="w", pady=(0, 10))

for category, extensions in file_types.items(): # loops extensions in cateogry
    text_line = f"{category}: " + ", ".join(extensions) # builds one line of text showing images and then extension to force join

    category_label = tk.Label( #creates label for category line
        categories_inner,
        text=text_line,
        font=normal_font,
        bg=panel_bg,
        fg=muted_text,
        justify="left",
        anchor="w",
        wraplength=220
    )
    category_label.pack(anchor="w", pady=3)

other_label = tk.Label( # create label for files not matching extension 
    categories_inner,
    text="other: any file types not listed above",
    font=normal_font,
    bg=panel_bg,
    fg=muted_text,
    justify="left",
    anchor="w",
    wraplength=220
)
other_label.pack(anchor="w", pady=(8, 0))

results_panel = tk.Frame( # creates result panel right side of middle 
    middle_row,
    bg=panel_bg,
    highlightbackground=panel_border,
    highlightthickness=1
)
results_panel.pack(side="left", fill="both", expand=True)
results_inner = tk.Frame(results_panel, bg=panel_bg, padx=14, pady=12) #styling padding
results_inner.pack(fill="both", expand=True)

results_title = tk.Label( # results title 
    results_inner,
    text="results",
    font=head_font,
    bg=panel_bg,
    fg=dark_text
)
results_title.pack(anchor="w")

results_info = tk.Label( # create explain text
    results_inner,
    text="moved files and any errors will show here",
    font=normal_font,
    bg=panel_bg,
    fg=muted_text
)
results_info.pack(anchor="w", pady=(4, 10))

#text box and scrollbar frames
results_text_frame = tk.Frame(results_inner, bg=panel_bg)
results_text_frame.pack(fill="both", expand=True)
scrollbar = tk.Scrollbar(results_text_frame) # makes scrollbar vertical 
scrollbar.pack(side="right", fill="y")

output_box = tk.Text( # creates text box with styling 
    results_text_frame,
    wrap="word",                 
    font=normal_font,            
    bg="#f9fafb",                
    fg=dark_text,                
    insertbackground=dark_text,  
    relief="solid",              
    bd=1,                        
    yscrollcommand=scrollbar.set #connects scrolling with scrollbar
)
output_box.pack(side="left", fill="both", expand=True)
output_box.config(state="disabled") # disable text box to stop typing
scrollbar.config(command=output_box.yview)#links scrollbar back to textbox

root.mainloop() #starts tkinter loop to run app, dont remove this or app wont launch 