class HotSOSError(Exception):

    def __init__(self, value, traceback):
        self.value = value
        self.traceback = traceback

    def __str__(self):
        return repr(self.value) + " > " + repr(self.traceback)
