import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import easyocr
from ultralytics import YOLO
import supervision as sv
import torch

# Initialize EasyOCR reader
reader = easyocr.Reader(['th','en'], gpu=True)
import torch
# Check if CUDA (GPU) is available
# Initialize YOLO model
def sw_yolo_model(str):
    if torch.cuda.is_available():
        model = YOLO(str).cuda()
        print(torch.cuda.is_available())
    else:
        model = YOLO(str)
    return model
model = sw_yolo_model("model/A_500.pt")

tracker = sv.ByteTrack()
box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
# Create the main window with an initial size
root = tk.Tk()
root.title("Video Processing App")
root.geometry("1320x960")  # Set the initial size

# Set the desired frame size to match the label's size
frame_width = 1280
frame_height = 720

# Video processing variables
video_path = ""
processing = False
frame_skip = 5  # Process every 5th frame
# Create a label on the left side to display vehicle information
info_label = ttk.Treeview(root, columns=("ID", "Type", "License Plate"), show="headings")
info_label.heading("ID", text="ID", anchor="w")
info_label.heading("Type", text="Type")
info_label.heading("License Plate", text="License Plate")
info_label.column("ID", anchor="w")  # "ID" column will be left-aligned
for col in ("Type", "License Plate"):
    info_label.column(col, anchor="center")  # Other columns will be center-aligned
info_label.pack(side="bottom", padx=10)

# Video processing function
def process_frame(frame):
    # Resize the frame to match the label's size
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Perform object detection
    results = model(frame)[0]

    # Annotate the frame
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)

    labels = [
        f"#{tracker_id} {results.names[class_id]}"
        for class_id, tracker_id
        in zip(detections.class_id, detections.tracker_id)
    ]

    annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
     # Recognize license plates
    vehicle_info = []
    for detection in detections.xyxy:  # Access the xyxy field
        x1, y1, x2, y2 = int(detection[0]), int(detection[1]), int(detection[2]), int(detection[3])  # Extract coordinates
        confidence = detections.confidence[0]  # Extract confidence
        class_id = detections.class_id[0]  # Extract class ID

        if x1 < 0:
            x1 = 0
        if x2 > frame.shape[1]:
            x2 = frame.shape[1]
        if y1 < 0:
            y1 = 0
        if y2 > frame.shape[0]:
            y2 = frame.shape[0]

        info = (
            len(vehicle_info) + 1,  # ID based on the number of elements in the list
            results.names[class_id],  # Vehicle type (replace with actual data) 
            ""  # License plate (initialize as empty string)
        )

        # Crop the region of the detected license plate and use EasyOCR for recognition
        license_plate_region = frame[y1:y2, x1:x2]
        if license_plate_region.shape[0] > 0 and license_plate_region.shape[1] > 0:
            license_plate = reader.readtext(license_plate_region)

            if license_plate:
                info = (
                    info[0], info[1], license_plate[0][-2]
                ) 
        vehicle_info.append(info)


    return annotated_frame, vehicle_info

def process_video():
    global video_path, processing
    if model is None:
        messagebox.showwarning("Warning", "Please load YOLO model before processing the video.")
        return
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        processing = True
        cap = cv2.VideoCapture(video_path)

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the beginning when the end is reached
                continue

            frame_count += 1

            if frame_count % frame_skip != 0:
                continue  # Skip this frame

            annotated_frame, vehicle_info = process_frame(frame)

            img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(image=img)
            label.config(image=img)
            label.image = img

            info_label.delete(*info_label.get_children())
            for info in vehicle_info:
                info_label.insert("", "end", values=info)

            root.update()

        # cap.release()
        # processing = False

# Add video button
add_video_button = tk.Button(root, text="Add Video", command=process_video)
add_video_button.pack(pady=5)
def load_yolo_model():
    global model
    model_path = filedialog.askopenfilename(filetypes=[("YOLO Model Files", "*.pt *.weights")])
    if model_path:
        model = YOLO(model_path)

load_model_button = tk.Button(root, text="Load YOLO Model", command=load_yolo_model)
load_model_button.pack(pady=5)
# Label for displaying the processed video with a size of 548x783
label = tk.Label(root, width=frame_width, height=frame_height)
label.pack()

# Process video button (enabled only when not processing)
process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.pack(pady=5)
process_button["state"] = "disabled"

# Function to enable the process button
def enable_process_button():
    process_button["state"] = "active"

# Check for video completion and enable process button
def check_video_completion():
    while True:
        if not processing:
            enable_process_button()
            break

# Start a thread to check for video completion
thread = threading.Thread(target=check_video_completion)
thread.daemon = True
thread.start()

# Start the main loop
root.mainloop()