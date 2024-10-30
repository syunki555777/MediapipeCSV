import threading

import JobThread as jt


class JobQueue(threading.Thread):

    def __init__(self, progress,start_button,model_path,csv_paths,video_paths,progress_text, progress_image_update_function, mode, updateList):
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
        if len(self.csv_paths) == len(self.video_paths):
            for index in range(len(self.csv_paths)):
                self.updateList(index, str(index) + ":" + self.video_paths[index] + " <処理中")
                thread = jt.JobThread(self.progress, self.start_button, self.model_path, self.csv_paths[index], self.file_path[index], self.progress_text,
                                      self.progress_image_update_function, self.mode)
                thread.start()


