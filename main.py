import os
from VideoObject import Video
from AudioObject import Audio

# This program is to extract text and split audio from an english video.
# To use it, create a directory in /Video/Result/ and put your video inside.
# Copy the path to your video, and run the program.
# It will ask you to paste the path and to enter some config.
#
# Package needing are :
#           opencv-python
#           pytesseract
#           numpy
#           Pillow Image
#           matplotlib
#           pydub


if __name__ == '__main__':
    print('Welcome to Video extract prog !!!')

    # video_path = input('Entrer le lien vers la video : ')
    video_path = input('Enter path to your video : ')
    dir_path = os.path.dirname(video_path)+'/'

    i = ''
    while True:
        try:
            data_path = dir_path+f'data{i}/'
            os.mkdir(data_path)
            break
        except:
            i += '-bis'
            print(f'pb : {i}')
    cut = int(input('From how many second Start the video ? : '))   # Start analyse on video from here
    breaker = input('Enter breaker : ')                             # Start chapter characters
    error = float(input('Enter Error : '))                                 # Error filter image

    # Create video and Audio instance
    my_video = Video(video_path, breaker, error)
    my_video.cutter(cut)
    my_video.cropper()
    #my_video.auto_crop(0.1, 0.1, 0.1, 0.1)

    my_audio = Audio(video_path, data_path)

    # Create all init data
    last_chapter = 0
    last_start_time = my_video.current_frame/my_video.fps
    ret = True
    while ret:
        ret, new, chapter, text, second = my_video.get()

        # Test if getting information from video
        if ret and new:
            if last_chapter != chapter:
                text = '\n\n'+str(chapter)+' - '+text
                last_chapter += 1
                my_audio.create(last_start_time, second, chapter)
                last_start_time = second

            # Writting text into data.txt
            with open(f'{dir_path}data{i}.txt', 'a+') as file:
                file.write(text)
                file.write('\n')
                file.close()
