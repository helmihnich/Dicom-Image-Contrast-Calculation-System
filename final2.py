import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTk, CTkButton, CTkLabel , CTkFrame # Update with actual module names
from matplotlib.patches import Rectangle
import pydicom
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
from matplotlib.widgets import RectangleSelector
from PIL import Image

# Constants
FIGURE_SIZE = (7, 6)
BUTTON_WIDTH = 468
BUTTON_HEIGHT = 80
LABEL_FONT = ("Times", 20)

# Global Variables
file_path = None
selected_roi_coordinates = []
contrast_values_list = []
contrast_values_list_te = []

def organize_imports():
    import tkinter as tk
    from tkinter import filedialog
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from customtkinter import CTk, CTkButton, CTkLabel
    from matplotlib.patches import Rectangle
    import pydicom
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import re
    from matplotlib.widgets import RectangleSelector
    from PIL import Image


def greeting():
    global ax1, canvas1, label3, label4, label6, label5, label7, root

    root = CTk(fg_color="#bcbbbe")
    root.title("Interface IRM")
    root.geometry("1700x900")

    bg_image = tk.PhotoImage(file="bg.gif")
    bg_image_label = tk.Label(root, image=bg_image)
    bg_image_label.place(x=0, y=0 )


    open_button = CTkButton(
        root,
        text="Se connecter",
        fg_color="#252A34",
        border_width=2,
        width=505,
        height=140,
        font=("Times", 45),
        corner_radius=20,
        command=create_main_gui,
    )
    open_button.place(x=269, y=524)

   
    root.mainloop()


def create_main_gui():
    global ax1, canvas1, label3, label4, label6, label5, label7, root
    root.destroy()

    root = CTk(fg_color="#b9b8bb")
    root.title("Interface IRM")
    root.geometry("1700x900")

    bg_image = tk.PhotoImage(file="bg1.gif")
    bg_image_label = tk.Label(root, image=bg_image)
    bg_image_label.place(x=0, y=0 )
    

    fig1 = plt.Figure(figsize=FIGURE_SIZE, dpi=100, facecolor="#EAEAEA")
    ax1 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1.get_tk_widget().place(x=40, y=150)
    open_button = CTkButton(
        root,
        text="Ouvrir image DICOM",
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font=("Times", 30),
        command=open_dicom_image1,
    )
    open_button.place(x=788, y=116)

    create_roi_button = CTkButton(
        root,
        text="Créer ROI",
        
        border_width=2,
        
        width=300,
        height=69,
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        font=("Times", 30),
        command=create_roi
    )
    create_roi_button.place(x=259, y=780)

    mean_intensity_button = CTkButton(
        root,
        text="Calculer les moyennes des intensités",
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        font=("Times", 25),
        command=calculate_mean_intensity
    )
    mean_intensity_button.place(x=788, y=230)


    label3 = CTkLabel(root, text="", font=("Times", 25), anchor='e')
    label3.place(x=1545, y=233)

    label4 = CTkLabel(root, text="",font=("Times",25),anchor='e')
    label4.place(x = 1545, y=271)

    # Créer un bouton pour calculer le RSB
    rsb_button = CTkButton(
        root, 
        text="Calculer le RSB",
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2, 
        height= 80, width=468,
        font=("Times",30),
        command=calculate_rsb)
    rsb_button.place(x=788,y=350)

    # Ajout de nouveaux labels pour le RSB
    label5 = CTkLabel(
        root,
        text="",
                                font=("Times",25),anchor='e'
                                )
    label5.place(x=1545,y=353)
    label6 = CTkLabel(root, text="",font=("Times",25),anchor='e')
    label6.place(x=1545,y=388)

    # Créer un bouton pour calculer le contraste
    contrast_button = CTkButton(
        root, 
        text="Calculer le contraste",
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2, 
        width=468,
        font=("Times",30),
        height=80,
        command=calculate_and_display_contrast)
    contrast_button.place(x=788,y=481)


    label7 = CTkLabel(root, text="",font=("Times",25),anchor='e')
    label7.place(x=1545,y=498)



    # # Créer un bouton pour charger une deuxième image DICOM
    # open_button = CTkButton(
    #     root, 
    #     text="Ouvrir la deuxième image DICOM",
    #     fg_color="#252A34",
    #     border_width=2, 
    #     width=300,
    #     font=("Times",15),
    #     height=40,
    #     command=open_dicom_image2)
    # open_button.pack(pady=12,padx=20)

    # Ajouter un bouton pour tracer la courbe de contraste
    plot_contrast_button = CTkButton(
        root, 
        text="Tracer Courbe TR en fonction de Contraste", 
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2, 
        width=468,
        font=("Times",20),
        height=80,
        command=calculate_contrast_curve)
    plot_contrast_button.place(x=788,y=616)

    # Ajouter un bouton pour tracer la courbe de contraste
    plot_contrast_button = CTkButton(
        root, 
        text="Tracer Courbe TE en fonction de contraste de Contraste", 
        fg_color="#D0D4CA",
        border_color="#161A30",
        text_color="black",
        border_width=2, 
        width=468,
        font=("Times",20),
        height=80,
        command=calculate_contrast_curve_te)
    plot_contrast_button.place(x=788,y=741)

    root.mainloop()

def onselect(eclick, erelease, roi_rectangles):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    roi = (min(x1, x2), min(y1, y2), width, height)
    roi_rectangles.append(Rectangle((roi[0], roi[1]), roi[2], roi[3], linewidth=1, edgecolor='r', facecolor='none'))
    plt.gca().add_patch(roi_rectangles[-1])
    plt.draw()
    
def create_roi():
    global roi_coordinates1, roi_coordinates2,file_path
    dicom_path = file_path
    if not dicom_path:
        print("No DICOM file selected. Exiting.")
        return
    

    dicom_data = pydicom.dcmread(dicom_path)
    
    roi_rectangles=[]
    fig, ax = plt.subplots()
    rs = RectangleSelector(ax, lambda eclick, erelease: onselect(eclick, erelease, roi_rectangles),
                            button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    plt.imshow(dicom_data.pixel_array, cmap='gray')
    # Wait for user to interactively select ROIs
    plt.show()

    # Get ROI coordinates
    if len(roi_rectangles) != 2:
        print("Please select exactly two ROIs.")
        return

    for roi in roi_rectangles:
        selected_roi_coordinates.append((roi.get_x(), roi.get_y(), roi.get_width(), roi.get_height()))
    print("ROI Coordinates:", selected_roi_coordinates)

def open_dicom_image1():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*.IMA")])
    if file_path:
        dicom_image = pydicom.dcmread(file_path)
        display_dicom_image(dicom_image, ax1, canvas1)
        
def create_roi():
    global file_path
    dicom_path = file_path
    if not dicom_path:
        print("No DICOM file selected. Exiting.")
        return

    dicom_data = pydicom.dcmread(dicom_path)
    
    roi_rectangles = []
    fig, ax = plt.subplots()
    rs = RectangleSelector(ax, lambda eclick, erelease: onselect(eclick, erelease, roi_rectangles),
                            button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    plt.imshow(dicom_data.pixel_array, cmap='gray')
    plt.show()

    if len(roi_rectangles) != 2:
        print("Please select exactly two ROIs.")
        return

    for roi in roi_rectangles:
        selected_roi_coordinates.append((roi.get_x(), roi.get_y(), roi.get_width(), roi.get_height()))
    print("ROI Coordinates:", selected_roi_coordinates)

# Fonction pour afficher les coordonnées de la ROI
def display_roi_coordinates(coordinates, label):
    if coordinates:
        x, y, width, height = map(int, coordinates)
        label.config(text=f" (x, y, largeur, hauteur): ({x}, {y}, {width}, {height})")

def calculate_mean_intensity():
    global selected_roi_coordinates, file_path
    if file_path and selected_roi_coordinates:
        dicom_image = pydicom.dcmread(file_path)
        mean_intensity1 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[0])
        mean_intensity2 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[1])
        label3.configure(text=f"{mean_intensity1:.2f}",bg_color="transparent",fg_color="transparent")
        label4.configure(text=f"{mean_intensity2:.2f}")
        print(f"Moyenne des intensités de la ROI : {mean_intensity1:.2f}")
    else:
        label3.configure(text="Aucune ROI définie")
        print("Aucune ROI définie")

def calculate_rsb():
    global selected_roi_coordinates, file_path
    if file_path and selected_roi_coordinates:
        dicom_image = pydicom.dcmread(file_path)
        signal_mean1 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[0])
        signal_mean2 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[1])
        signal_mean = (signal_mean1+signal_mean2)/2
        noise_std1 = calculate_roi_std_intensity(dicom_image, selected_roi_coordinates[0])
        noise_std2 = calculate_roi_std_intensity(dicom_image, selected_roi_coordinates[1])
        rsb1 = calculate_signal_noise_ratio(signal_mean1, noise_std1)
        rsb2 = calculate_signal_noise_ratio(signal_mean2, noise_std2)
        label5.configure(text=f"{rsb1:.2f}")
        label6.configure(text=f"{rsb2:.2f}")
        print(f"RSB de la ROI : {rsb1:.2f}")

def calculate_and_display_rsn():
    global selected_roi_coordinates, file_path,selected_roi_coordinates
    dicom_image = pydicom.dcmread(file_path)
    signal_mean1 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[0])
    noise_std1 = calculate_roi_std_intensity(dicom_image, selected_roi_coordinates[0])

    signal_mean2 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[1])
    noise_std2 = calculate_roi_std_intensity(dicom_image, selected_roi_coordinates[1])

    rsb1 = calculate_signal_noise_ratio(signal_mean1, noise_std1)
    rsb2 = calculate_signal_noise_ratio(signal_mean2, noise_std2)

    print(f"RSB de la ROI 1: {rsb1:.2f}")
    print(f"RSB de la ROI 2: {rsb2:.2f}")

def calculate_roi_std_intensity(image, coordinates):
    if coordinates:
        x, y, width, height = map(int, coordinates)  # Convert coordinates to integers
        pixel_array = image.pixel_array
        roi = pixel_array[y:y+height, x:x+width]
        mean_intensity = np.std(roi)
        return mean_intensity

    return None

def calculate_signal_noise_ratio(signal_mean, noise_std):
    if noise_std == 0:
        return float('inf')  # Pour éviter une division par zéro
    else:
        return signal_mean / noise_std

# def open_dicom_image2():
#     global roi_coordinates, file_path
#     file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*IMA")])
#     if file_path:
#         dicom_image = pydicom.dcmread(file_path)
#         display_dicom_image(dicom_image, ax2, canvas2)
#         roi_coordinates = generate_random_roi_coordinates(dicom_image)

def calculate_roi_mean_intensity(image, coordinates):
    if coordinates:
        x, y, width, height = map(int, coordinates)  # Convert coordinates to integers
        pixel_array = image.pixel_array
        roi = pixel_array[y:y+height, x:x+width]
        mean_intensity = np.mean(roi)
        return mean_intensity
    return None

def display_roi_mean_intensity(image, coordinates,label):
    mean_intensity1 = calculate_roi_mean_intensity(image, coordinates[0])
    mean_intensity2 = calculate_roi_mean_intensity(image, coordinates[1])
    mean_intensity = (mean_intensity1+mean_intensity2)/2
    if mean_intensity is not None:
        label.config(text=f"Moyenne des intensités de la ROI: {mean_intensity:.2f}")
        print(f"Moyenne des intensités de la ROI: {mean_intensity:.2f}")
    else:
        label.config(text="Aucune ROI définie")
        print("Aucune ROI définie")

# Fonction pour afficher une image DICOM
def display_dicom_image(dicom_image,ax,canvas,roi_coordinates1=None,roi_coordinates2=None):
    cv_image = dicom_image.pixel_array
    ax.clear()
    ax.imshow(cv_image, cmap="gray")
    if roi_coordinates1:
        x1, y1, width1, height1 = roi_coordinates1
        cv_image_with_roi1 = cv_image.copy()
        cv2.rectangle(cv_image_with_roi1, (x1, y1), (x1 + width1, y1 + height1), (255, 0, 0), 2)
        ax.imshow(cv_image_with_roi1, cmap="gray")
    if roi_coordinates2:
        x2, y2, width2, height2 = roi_coordinates2
        cv_image_with_roi2 = cv_image.copy()
        cv2.rectangle(cv_image_with_roi2, (x2, y2), (x2 + width2, y2 + height2), (0, 255, 0), 2)
        ax.imshow(cv_image_with_roi2, cmap="gray")
    canvas.draw()

    def add_tr_contrast_pair():
        global contrast_values_list, file_path, roi_coordinates1, roi_coordinates2
        if file_path and roi_coordinates1 and roi_coordinates2:
            dicom_image = pydicom.dcmread(file_path)

def get_tr_value_from_filename(filename):
    # Utiliser une expression régulière pour extraire la valeur TR du nom du fichier
    match = re.search(r'(\d+)TE10', filename)
    if match:
        tr_value = int(match.group(1))
        return tr_value
    else:
        return None
    
def get_te_value_from_filename(filename)  :  
    # Utiliser une expression régulière pour extraire la valeur TE du nom du fichier
    match = re.search(r'TR4000_TE(\d+)', filename)
    if match:
        te_value = int(match.group(1))
        return te_value
    else:
        return None
        

# Fonction pour générer des coordonnées de ROI aléatoires
def calculate_contrast(mean_intensity1, mean_intensity2):
    return np.abs(mean_intensity1 - mean_intensity2) / (mean_intensity1 + mean_intensity2)

def calculate_and_display_contrast():
    global selected_roi_coordinates, file_path
    if file_path and selected_roi_coordinates:
        dicom_image = pydicom.dcmread(file_path)
        mean_intensity1 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[0])
        mean_intensity2 = calculate_roi_mean_intensity(dicom_image, selected_roi_coordinates[1])
        contrast_value = calculate_contrast(mean_intensity1, mean_intensity2)  # Use your contrast calculation function
        label7.configure(text=f"{contrast_value:.4f}")

        tr_value = get_tr_value_from_filename(file_path)  # Remplacez cela par la fonction appropriée 
        te_value = get_te_value_from_filename(file_path)

        #pour obtenir la valeur TR
        if tr_value is not None:
            contrast_values_list.append((tr_value, contrast_value))
        if te_value is not None:
            contrast_values_list_te.append((te_value, contrast_value))
        else:
            print(f"Attention : Impossible d'extraire la valeur TR du fichier {file_path}")

def calculate_contrast_curve():
    global contrast_values_list
    if contrast_values_list:
        tr_values, contrast_values = zip(*contrast_values_list)
        print(zip(*contrast_values_list))

        # Tracer la courbe
        fig = plt.figure()
        plt.plot(tr_values, contrast_values, marker='o')  # Ajout de markers pour chaque point
        plt.xlabel('TR Values')
        plt.ylabel('Contrast')
        plt.title('Contrast Curve vs TR')


        # Intégrer la figure à une nouvelle fenêtre
        new_window = tk.Toplevel(root)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        plt.close(fig)

def calculate_contrast_curve_te():
    global contrast_values_list_te
    if contrast_values_list_te:
        te_value, contrast_values = zip(*contrast_values_list_te)
        print(zip(*contrast_values_list))

        # Tracer la courbe
        fig = plt.figure()
        plt.plot(te_value, contrast_values, marker='o')  # Ajout de markers pour chaque point
        plt.xlabel('TE Values')
        plt.ylabel('Contrast')
        plt.title('Contrast Curve vs TE')


        # Intégrer la figure à une nouvelle fenêtre
        new_window = tk.Toplevel(root)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        plt.close(fig)

if __name__ == "__main__":
    organize_imports()
    greeting()
