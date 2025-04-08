import threading
import faceOutput
import poseOutput
import handOutput
import gestureOutput
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

class JobThread(threading.Thread):
    def __init__(self, progress,start_button,model_path,csv_paths,video_paths,progress_text, progress_image_update_function, mode,updateList):
        super().__init__()

        self.progress = progress
        self.start_button = start_button
        self.model_path = model_path
        self.csv_paths = csv_paths
        self.video_paths = video_paths
        self.progress_text = progress_text
        self.progress_image_update_function = progress_image_update_function
        self.mode = mode
        self.updateList = updateList

    def run(self):

        if len(self.csv_paths) != len(self.video_paths):
            messagebox.showwarning("Warning", "CSVリストと動画リストの長さがことなっています。")
            self.stop()
            return False

        if not self.video_paths:
            messagebox.showwarning("Warning", "動画を選択してください。")
            self.stop()
            return False

        if not self.csv_paths:
            messagebox.showwarning("Warning", "CSVを選択してください。")
            self.stop()
            return False

        self.start_button.config(state=tk.DISABLED)
        for index in range(len(self.csv_paths)):

            start_time = datetime.now()
            self.updateList(index, str(index) + ":\t" + self.video_paths[index] + " \t<処理中 |\t 開始:" + start_time.strftime("%H:%M:%S"))
            video_path = self.video_paths[index]
            csv_path = self.csv_paths[index]

            print("JobThread started")

            try:
                if self.mode == "Face":
                    faceOutput.extract_face_landmarks_to_csv(video_path=video_path,csv_path=csv_path,model_path=self.model_path,progress_bar=self.progress,progress_text=self.progress_text,progress_image_update_function=self.progress_image_update_function)

                elif self.mode == "Face without landmarks":
                    faceOutput.extract_face_landmarks_to_csv(video_path=video_path, csv_path=csv_path,
                                                             model_path=self.model_path, progress_bar=self.progress,
                                                             progress_text=self.progress_text,
                                                             progress_image_update_function=self.progress_image_update_function,blendShapes_Only= True)

                elif self.mode == "Pose -heavy" or self.mode == "Pose -lite":
                    poseOutput.extract_pose_landmarks_to_csv(video_path=video_path, csv_path=csv_path,
                                                             model_path=self.model_path, progress_bar=self.progress,
                                                             progress_text=self.progress_text,
                                                             progress_image_update_function=self.progress_image_update_function)
                elif self.mode == "Hand":
                    handOutput.extract_hand_landmarks_to_csv(video_path=video_path, csv_path=csv_path,
                                                             model_path=self.model_path, progress_bar=self.progress,
                                                             progress_text=self.progress_text,
                                                             progress_image_update_function=self.progress_image_update_function)
                elif self.mode == "Hand gesture":
                    gestureOutput.extract_gestures_to_csv(video_path=video_path, csv_path=csv_path,
                                                             model_path=self.model_path, progress_bar=self.progress,
                                                             progress_text=self.progress_text,
                                                             progress_image_update_function=self.progress_image_update_function)

            except Exception as e:
                print(e)
                self.updateList(index, str(index) + ":\t" + self.video_paths[index] + "\t!エラー!")
                #次の処理に移る
                #return False
            end_time = datetime.now()  # 処理終了時刻を記録
            elapsed_time = end_time - start_time
            self.updateList(index, str(index) + ":\t" + self.video_paths[index] + "\t[完了] | 経過時間:" + str(elapsed_time))

        # 終了
        self.stop()
        self.progress_text.set("処理が完了しました。")
    def safe_showwarning(self, title, msg):
        root = tk.Tk()
        root.after(0, messagebox.showwarning, title, msg)

    def stop(self):
        print("JobThread stopped")
        self.start_button.config(state=tk.NORMAL)

