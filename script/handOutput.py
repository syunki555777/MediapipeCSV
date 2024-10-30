import cv2
import mediapipe as mp
import numpy as np
import csv
import time
from tkinter import ttk
import math
import datetime

from fontTools.ttx import process


def extract_hand_landmarks_to_csv(video_path, csv_path, model_path, progress_bar,progress_text, progress_image_update_function):
    # FaceLandmarkerのオプションを設定
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
        running_mode=mp.tasks.vision.RunningMode.VIDEO)

    # FaceLandmarkerインスタンスを生成
    landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)



    try:
        # 動画ファイルを開く
        cap = cv2.VideoCapture(video_path)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar["maximum"] = total_frames
        fps = cap.get(cv2.CAP_PROP_FPS)  # フレームレートを取得

        if fps == 0:
            print("fps is 0")

        frame_num = 0
        print(str(total_frames) + "frames video detected.")
        print("videoPath:" + video_path + "csv_path: " + csv_path + "total_frames:" + str(total_frames) + "fps:" + str(fps) )
        # 出力CSVファイルの設定
        with open(csv_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            start_time = time.time()
            #ヘッダー出力
            header = ["time"]
            for i in range(0, 21):
                header.append(str(i)+"_x")
                header.append(str(i)+"_y")
                header.append(str(i)+"_z")
            for i in ["Handedness"]:
                header.append(i + "_x")

            csv_writer.writerow(header)

            startProcess = datetime.datetime.now()
            updateTime = datetime.datetime.now()
            process_fps = 0
            mean_fps = 0

            if not cap.isOpened():
                raise ValueError("Unable to open video file: " + video_path)
            # ビデオからフレームを読み取る
            while cap.isOpened():

                frame_num += 1
                time_diff = datetime.datetime.now() - updateTime

                if time_diff.total_seconds() > 1:
                    process_fps = math.ceil((frame_num - process_fps)*100 / time_diff.total_seconds())/100
                    if not mean_fps == 0:
                        mean_fps = process_fps
                    mean_fps = mean_fps * 0.9 + process_fps * 0.1
                    progress_text.set(str(str(math.ceil(frame_num*10000/total_frames)/100) + "%\t" + str(process_fps) + "fps\t残り"+ str(math.floor((total_frames-frame_num)/mean_fps/60))+ "分" +f"{math.ceil((total_frames-frame_num)/mean_fps)%60:02}" +"秒").expandtabs(9))
                    updateTime = datetime.datetime.now()
                    process_fps = frame_num
                    progress_image_update_function(frame)
                    print(cap.get(cv2.CAP_PROP_POS_MSEC))

                if frame_num % 10 == 0:
                    progress_bar["value"] = frame_num

                ret, frame = cap.read()
                if not ret:
                    break

                # OpenCVからMediaPipeのImageオブジェクトへ変換
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

                # 現在のフレームのタイムスタンプを計算
                frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

                # 顔のランドマーキングを実行
                face_landmarker_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

                if face_landmarker_result.hand_landmarks:
                    # ランドマークデータの取得と整形
                    landmarks = []
                    for pose_landmark in face_landmarker_result.hand_world_landmarks[0]:
                        landmarks.append(pose_landmark.x)
                        landmarks.append(pose_landmark.y)
                        landmarks.append(pose_landmark.z)
                    if face_landmarker_result.handedness:
                        landmarks.append(face_landmarker_result.handedness[0][0].category_name)
                    csv_writer.writerow([cap.get(cv2.CAP_PROP_POS_MSEC) / 1000] + landmarks)

                else:
                    csv_writer.writerow([cap.get(cv2.CAP_PROP_POS_MSEC) / 1000])


    except Exception as e:
        raise e
    finally:
        cap.release()


# 使用例
#model_path = 'path_to_your_model'  # モデルのパスを適切に設定
#video_path = 'path_to_your_video.mp4'  # ビデオのパスを設定
#csv_path = 'output_data.csv'  # CSVファイルのパスを設定
#extract_face_landmarks_to_csv(video_path, csv_path, model_path)
