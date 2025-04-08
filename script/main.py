import tkinter as tk
from tkinter import ttk
import time
from tkinter import filedialog, font
import os
import cv2
from tkinter import messagebox
import JobThread as jt
import progress as pg
from PIL import Image, ImageTk
from numpy import zeros

import re

base_dir = os.path.dirname(os.path.abspath(__file__))

# Use this as the base for any files that you need to access
face_model_path = os.path.join(base_dir, "face_landmarker.task")
pose_lite_model_path = os.path.join(base_dir, "pose_landmarker_lite.task")
pose_heavy_model_path = os.path.join(base_dir, "pose_landmarker_heavy.task")
hand_model_path = os.path.join(base_dir, "hand_landmarker.task")
hand_gesture_mode_path = os.path.join(base_dir, "gesture_recognizer.task")
file_path_strs = []
csv_path_strs = []
mode = "Face"
thread = None
running = False


def start_jobs():
    global start_button
    start_button["state"] = "disabled"

    global progress_text
    global canvas
    global thread

    if not thread:
        model_path = ""
        if mode == "Pose -heavy":
            model_path = pose_heavy_model_path
        elif mode == "Pose -lite":
            model_path = pose_lite_model_path
        elif mode == "Face" or mode == "Face without landmarks":
            model_path = face_model_path
        elif mode == "Hand":
            model_path = hand_model_path
        elif mode ==  "Hand gesture":
            model_path = hand_gesture_mode_path
        thread = jt.JobThread(progress, start_button, model_path, csv_path_strs,file_path_strs,progress_text,display_image_on_canvas,mode,updateChangeVideoBox)
        thread.start()


root = tk.Tk()
root.title("Mediapipe CSV converter")

#ビデオバス
video_paths_listbox = tk.Listbox(root, selectmode=tk.SINGLE,width=100)
video_paths_listbox.grid(row=4, column=0,columnspan=5, padx=10, pady=10)

#CSVパス
#csv_paths_listbox = tk.Listbox(root, selectmode=tk.SINGLE,width=50)
#csv_paths_listbox.grid(row=4, column=3,columnspan=2, padx=10, pady=10)

def updateChangeVideoBox(index, newString):
    video_paths_listbox.delete(index)
    video_paths_listbox.insert(index, newString.expandtabs(10))

def select_video():
    # Listboxをクリア
    video_paths_listbox.delete(0, tk.END)


    filenames = filedialog.askopenfilenames(title="動画を選択",filetypes=[('Video Files', '*.mp4 *.avi *.mov'),("すべてのファイル", "*.*")])

    if filenames:
        global file_path_strs
        global csv_path_strs
        global canvas
        global height
        global width
        file_path_strs = filenames
        video_path.set(filenames[0])
        csv_path_strs = []
        for name in filenames:
            csv_path_strs.append(re.sub(r'\.[^.]+$', '_mediapipe.csv', name))
        csv_path.set(csv_path_strs[0])


        cap = cv2.VideoCapture(filenames[0])

        ret, frame = cap.read()

        for index in range(len(filenames)):
            video_paths_listbox.insert(tk.END,  str(str(index)+":\t"+filenames[index]).expandtabs(10))
            #csv_paths_listbox.insert(tk.END, csv_path_strs[index])


def select_folder():
    # フォルダ選択ダイアログを表示
    folder_path = filedialog.askdirectory(title="フォルダを選択")

    if folder_path:
        # リストボックスをクリア
        video_paths_listbox.delete(0, tk.END)

        # 動画ファイルの拡張子を定義
        video_file_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')

        # フォルダ内のファイルを再帰的に探索
        global file_path_strs
        global csv_path_strs

        file_path_strs = []
        csv_path_strs = []

        for root_dir, _, files in os.walk(folder_path):  # os.walkですべてのサブディレクトリを探索
            for filename in files:
                # 動画ファイルかチェック
                if filename.lower().endswith(video_file_extensions):
                    full_path = os.path.join(root_dir, filename)
                    file_path_strs.append(full_path)
                    csv_path_strs.append(re.sub(r'\.[^.]+$', '_mediapipe.csv', full_path))

        # リストボックスに追加
        for index, path in enumerate(file_path_strs):
            video_paths_listbox.insert(tk.END, f"{index}: {path}")

        if file_path_strs:
            # 最初の動画ファイルをセット
            video_path.set(file_path_strs[0])
            csv_path.set(csv_path_strs[0])
        else:
            video_path.set("動画ファイルが見つかりませんでした。")
            csv_path.set("")



def display_image_on_canvas(cv_img):
    global tk_img  # 必ずこの画像はグローバルで保存しておく
    global image_id  # 画像アイテムのIDを保存するための変数
    global height
    global width
    global canvas

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



# Button to select video file
select_video_button = ttk.Button(root, text="動画を選択", command=select_video)
select_video_button.grid(row=0, column=0, padx=10, pady=10)

# フォルダ選択ボタン
select_folder_button = ttk.Button(root, text="フォルダを選択", command=select_folder)
select_folder_button.grid(row=0, column=2, padx=10, pady=10)

# Label to display selected video path
video_path = tk.StringVar()
video_path.set("動画は選択されていません。")
video_path_label = ttk.Label(root, textvariable=video_path)
video_path_label.grid(row=0, column=1, padx=10, pady=10)

# Save to csv
#select_csv_button = ttk.Button(root, text="save to the csv file", command=save_csv)
#select_csv_button.grid(row=0, column=2, padx=10, pady=10)

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
large_font = tk.font.Font(family="Helvetica", size=20, weight="bold")
progress_text_label = ttk.Label(frame, textvariable=progress_text,font=large_font)

progress_text_label.grid(row=0, column=1, padx=10, pady=10)
canvas.grid(row=0, column=0, rowspan = 2,padx=5, pady=5)
progress.grid(row=1, column=1, columnspan=1,rowspan=5, padx=10, pady=10)



# Create a list of models
models = ['Face', 'Face without landmarks' ,'Pose -heavy', 'Pose -lite', 'Hand', 'Hand gesture']

# Create a StringVar for currently selected model
current_model = tk.StringVar()

# Create a combobox for model selection
model_menu = ttk.Combobox(root, textvariable=current_model, values=models,state="readonly")
model_menu.grid(row=0, column=4, padx=10, pady=10)


def update_model(*args):
    global face_model_path
    global mode
    mode = current_model.get()


# bind the function to the combobox
current_model.trace('w', update_model)

model_menu.current(0)  # Set the first model as the default


opencv_button = ttk.Button(root, text="詳細", command=show_info)
opencv_button.grid(row=5, column=0, padx=10, pady=10)

start_button = ttk.Button(root, text="開始", command=start_jobs)
start_button.grid(row=5, column=4, padx=10, pady=10)
root.resizable(0,0)
root.mainloop()
