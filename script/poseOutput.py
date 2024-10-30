import cv2
import mediapipe as mp
import numpy as np
import csv
import time
from tkinter import ttk
import math
import datetime


def extract_pose_landmarks_to_csv(video_path, csv_path, model_path, progress_bar,progress_text, progress_image_update_function):
    # FaceLandmarkerのオプションを設定
    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
        running_mode=mp.tasks.vision.RunningMode.VIDEO)

    # FaceLandmarkerインスタンスを生成
    landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(options)


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
            for i in ["nose"
                ,"left_eye_(inner)"
                ,"left_eye"
                ,"left_eye_(outer)"
                ,"right_eye_(inner)"
                ,"right_eye"
                ,"right_eye_(outer)"
                ,"left_ear"
                ,"right_ear"
                ,"mouth_(left)"
                ,"mouth_(right)"
                ,"left_shoulder"
                ,"right_shoulder"
                ,"left_elbow"
                ,"right_elbow"
                ,"left_wrist"
                ,"right_wrist"
                ,"left_pinky"
                ,"right_pinky"
                ,"left_index"
                ,"right_index"
                ,"left_thumb"
                ,"right_thumb"
                ,"left_hip"
                ,"right_hip"
                ,"left_knee"
                ,"right_knee"
                ,"left_ankle"
                ,"right_ankle"
                ,"left_heel"
                ,"right_heel"
                ,"left_foot_index"
                ,"right_foot_index"]:
                header.append(i + "_x")
                header.append(i + "_y")
                header.append(i + "_z")

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
                    progress_text.set(str(str(math.ceil(frame_num * 10000 / total_frames) / 100) + "%\t" + str(
                        process_fps) + "fps\t残り" + str(math.floor((total_frames - frame_num) / mean_fps / 60)) + "分" + f"{math.ceil((total_frames - frame_num) / mean_fps) % 60:02}" + "秒").expandtabs(9))

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

                if face_landmarker_result.pose_world_landmarks:
                    # ランドマークデータの取得と整形
                    landmarks = []
                    for pose_landmark in face_landmarker_result.pose_world_landmarks[0]:
                        face_landmarker_result.pose_world_landmarks[0]
                        landmarks.append(pose_landmark.x)
                        landmarks.append(pose_landmark.y)
                        landmarks.append(pose_landmark.z)

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
