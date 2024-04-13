import tkinter as tk
from tkinter import ttk
import time
from tkinter import filedialog
import os
import cv2
from tkinter import messagebox
import JobThread as jt
import progress as pg
from PIL import Image, ImageTk
from numpy import zeros

model_path = "face_landmarker.task"
video_path_str = ""
csv_path_str = ""

def start_jobs():
    start_button["state"] = "disabled"
    global root
    #frameを作成してframeないに詳細を描画
    frame = tk.Frame(root)
    frame.grid(row=2, column=0,rowspan=3, columnspan=6, padx=10, pady=10, ipadx=100)

    #画像描画
    width = 100
    height = 80
    #NoImageを生成
    image = zeros((width, height, 3), dtype="uint8")

    # 描画パラメータを指定
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # 白色
    thickness = 2

    # テキストを描画
    cv2.putText(image, "No Image", (int(width/2), int(height/2)), font, font_scale, color, thickness)
    cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))

    #画像を描画
    canvas = tk.Canvas(frame, width=width, height=height)
    canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)
    canvas.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

    # 文字描画
    progress_text = tk.StringVar()
    progress_text.set("処理を開始しました...")
    progress_text_label = ttk.Label(frame, textvariable=progress_text)
    progress_text_label.grid(row=1, column=1, padx=10, pady=10)

    #progress barを生成
    progress = ttk.Progressbar(frame, length=500, mode='determinate', maximum=10000)
    progress.grid(row=3, column=1, padx=10, pady=10)

    thread = jt.JobThread(progress, start_button, model_path, csv_path_str,video_path_str)
    thread.start()


def select_video():
    filename = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4 *.avi *.mov')])
    if filename:
        global video_path_str
        video_path_str = filename
        video_path.set(filename)


def save_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[('csv', '*.csv')])
    if filename:
        global csv_path_str
        csv_path_str = filename
        csv_path.set(filename)

def show_info():
    root = tk.Tk()
    text = tk.Text(root)
    root.title("OpenCVのビルド状況")
    text.pack(side=tk.LEFT, fill=tk.Y)
    text.insert(tk.END, cv2.getBuildInformation())
    scroll = tk.Scrollbar(root)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Scrollbarの設定
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    root.mainloop()


root = tk.Tk()
root.title("Mediapipe CSV converter")

add_button = ttk.Button(root, text="追加", command=start_jobs)
add_button.grid(row=0, column=5, padx=10, pady=10)

# Button to select video file
select_video_button = ttk.Button(root, text="動画を選択", command=select_video)
select_video_button.grid(row=0, column=0, padx=10, pady=10)

# Label to display selected video path
video_path = tk.StringVar()
video_path.set("動画は選択されていません。")
video_path_label = ttk.Label(root, textvariable=video_path)
video_path_label.grid(row=0, column=1, padx=10, pady=10)

# Save to csv
select_csv_button = ttk.Button(root, text="save to the csv file", command=save_csv)
select_csv_button.grid(row=0, column=2, padx=10, pady=10)

csv_path = tk.StringVar()
csv_path.set("csvは選択されていません。")
csv_path_label = ttk.Label(root, textvariable=csv_path)
csv_path_label.grid(row=0, column=3, padx=10, pady=10)

opencv_button = ttk.Button(root, text="詳細", command=show_info)
opencv_button.grid(row=4, column=0, padx=10, pady=10)

start_button = ttk.Button(root, text="開始", command=start_jobs)
start_button.grid(row=0, column=5, padx=10, pady=10)

root.mainloop()
