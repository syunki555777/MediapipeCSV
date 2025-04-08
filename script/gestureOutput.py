import cv2
import mediapipe as mp
import csv
import datetime
import math


def extract_gestures_to_csv(video_path, csv_path, model_path, progress_bar, progress_text,
                            progress_image_update_function):
    """ジェスチャーを検出してCSVに保存する関数（右手・左手やスコアなどの追加情報を出力）"""
    # GestureRecognizerの設定
    base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.VIDEO
    )
    recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

    try:
        # 動画ファイルを開く
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar["maximum"] = total_frames

        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {video_path}")

        # CSV初期化
        with open(csv_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)

            # ヘッダー（順序を明確化）
            header = ["time"]
            for i in range(21):
                header.extend([f"landmark_{i}_x", f"landmark_{i}_y", f"landmark_{i}_z"])  # ランドマーク座標
            header.extend(["gesture_Unrecognized", "gesture_Closed_Fist", "gesture_Open_Palm",
                "gesture_Pointing_Up", "gesture_Thumb_Down", "gesture_Thumb_Up",
                "gesture_Victory", "gesture_ILoveYou", "handedness" ]) # ジェスチャー＋右手/左手)
            csv_writer.writerow(header)

            # フレーム処理開始
            frame_num = 0
            process_start_time = datetime.datetime.now()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_num += 1
                current_time = datetime.datetime.now()

                # プログレス更新
                if frame_num % 10 == 0:
                    fps = frame_num / (current_time - process_start_time).total_seconds()
                    remaining_time = (total_frames - frame_num) / fps
                    remaining_minutes = math.floor(remaining_time / 60)
                    remaining_seconds = round(remaining_time % 60)
                    progress_text.set(
                        f"進捗: {frame_num / total_frames * 100:.2f}% | {fps:.2f} fps |"
                        f" 残り: {remaining_minutes}分{remaining_seconds:02}秒")
                    progress_bar["value"] = frame_num
                    progress_image_update_function(frame)

                # フレームをRGB変換
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

                # ジェスチャー認識を実施
                result = recognizer.recognize_for_video(mp_image, frame_timestamp_ms)

                # データ行の初期化
                row_data = [frame_timestamp_ms / 1000]  # タイムスタンプ

                # ジェスチャースコア初期化
                gesture_scores = {
                    "Unrecognized": 0.0,
                    "Closed_Fist": 0.0,
                    "Open_Palm": 0.0,
                    "Pointing_Up": 0.0,
                    "Thumb_Down": 0.0,
                    "Thumb_Up": 0.0,
                    "Victory": 0.0,
                    "ILoveYou": 0.0,
                }
                handedness = None  # 右手/左手初期化

                # ジェスチャーと右手/左手情報の取得
                if result.gestures and result.hand_landmarks:
                    # スコア情報取得
                    for gesture in result.gestures[0]:
                        if gesture.category_name in gesture_scores:
                            gesture_scores[gesture.category_name] = gesture.score

                    # 右手/左手の情報取得
                    if result.handedness:
                        handedness = result.handedness[0][0].category_name  # "Right" または "Left"

                    # ランドマーク取得
                    for hand_landmarks in result.hand_world_landmarks:
                        for landmark in hand_landmarks:
                            row_data.extend([landmark.x, landmark.y, landmark.z])
                else:
                    # ランドマークがない場合のデフォルト
                    row_data.extend([None] * (21 * 3))

                # ジェスチャーと右手/左手を追加
                row_data.extend(gesture_scores.values())
                row_data.append(handedness)

                # CSV行の順序を一致させて書き込み
                csv_writer.writerow(row_data)

    except Exception as e:
        print(f"エラー: {e}")
    finally:
        # 動画を解放
        cap.release()