class Progress:

    def __init__(self, progress_bar, photo, name, progress_text):
        self.progress_bar = progress_bar
        self.photo = photo
        self.name = name
        self.progress_text = progress_text
    @property
    def progress_bar(self):
        return self._progress_bar


    @property
    def photo(self):
        return self._photo


    @property
    def name(self):
        return self._name


    @property
    def progress_text(self):
        return self._progress_text
