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

    thread = jt.JobThread(progress, start_button, model_path, csv_path_str,video_path_str)
    thread.start()


def select_video():
    filename = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4 *.avi *.mov')])
    if filename:
        global video_path_str
        global canvas
        global height
        global width
        video_path_str = filename
        video_path.set(filename)

        cap = cv2.VideoCapture(filename)

        ret, frame = cap.read()

        if ret:
            display_image_on_canvas(frame,canvas)


def display_image_on_canvas(cv_img, canvas):
    global tk_img  # 必ずこの画像はグローバルで保存しておく
    global image_id  # 画像アイテムのIDを保存するための変数
    global height
    global width

    # BGRからRGBに変換（OpenCVはBGR、TkinterはRGB）
    cv_img = resize_with_border(cv_img, width, height)
    cv_img_color = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    # OpenCVの画像からPIL画像に変換
    pil_img = Image.fromarray(cv_img_color)
    # PILからTkinter用の画像に変換
    tk_img = ImageTk.PhotoImage(image=pil_img)
    # Canvasに画像を表示または更新
    if 'image_id' in globals():
        # 画像アイテムが既に存在する場合、その'image'属性を更新
        canvas.itemconfig(image_id, image=tk_img)
    else:
        # まだ画像アイテムが存在しない場合、新しく作成しIDを保持
        image_id = canvas.create_image(0, 0, image=tk_img, anchor='nw')

def resize_with_border(img, width, height):
    # アスペクト比を維持したままリサイズする
    h, w, _ = img.shape
    if w > h:
        new_w = width
        new_h = int(h * width / w)
    else:
        new_h = height
        new_w = int(w * height / h)

    img_resized = cv2.resize(img, (new_w, new_h))

    # リサイズした画像の高さと幅
    h, w, _ = img_resized.shape

    # 上下左右に追加するボーダーの大きさ
    top = (height - h) // 2
    bottom = height - h - top
    left = (width - w) // 2
    right = width - w - left

    # ボーダーを追加（色は黒）
    img_with_border = cv2.copyMakeBorder(img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, (0, 0, 0))

    return img_with_border

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

#進捗状況の表示
frame = ttk.Frame(root)
frame.grid(row=1, column=0, columnspan=5 , padx=10, pady=10)
#進捗
progress = ttk.Progressbar(frame, length=700, mode='determinate', maximum=10000)


# 画像描画
width = 170
height = 170
# NoImageを生成
image = zeros((width, height, 3), dtype="uint8")

# 描画パラメータを指定
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (255, 255, 255)  # 白色
thickness = 2

# テキストを描画
cv2.putText(image, "No Image", (int(width / 13), int(height / 1.8)), font, font_scale, color, thickness)
cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv_img))

# 画像を描画
canvas = tk.Canvas(frame, width=width, height=height)
image_id = canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)

# 文字描画
progress_text = tk.StringVar()
progress_text.set("動画を選択して開始を押してください。")
progress_text_label = ttk.Label(frame, textvariable=progress_text)
progress_text_label.grid(row=0, column=1, padx=10, pady=10)
canvas.grid(row=0, column=0, rowspan = 2,padx=5, pady=5)
progress.grid(row=1, column=1, columnspan=1,rowspan=5, padx=10, pady=10)


opencv_button = ttk.Button(root, text="詳細", command=show_info)
opencv_button.grid(row=4, column=0, padx=10, pady=10)

start_button = ttk.Button(root, text="開始", command=start_jobs)
start_button.grid(row=0, column=5, padx=10, pady=10)

root.mainloop()
