from pydub import AudioSegment


class Audio:
    def __init__(self, sound_path, dir_path):
        self.dir_path = dir_path
        self.sound = AudioSegment.from_file(sound_path)

    def create(self, start, end, name):
        cut = self.sound[start*1000:end*1000]
        cut.export(f'{self.dir_path}{name}.mp3', format="mp3")
