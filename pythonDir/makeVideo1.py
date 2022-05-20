import os
import pandas as pd
# from pytube import YouTube
from moviepy.editor import *
import librosa
import soundfile as sf
import numpy as np
import shutil
import logging
import cv2

# 경로 정의
DATA_OUT_PATH = '/var/www/html/webpage/outputData/'
DATA_IN_PATH = '/var/www/html/webpage/inputData/'
PATH_DATA = '/var/www/html/webpage/pythonDir/'
INPUT_DATA = 'clova_result.csv'

test_data = pd.read_csv(PATH_DATA + 'clova_result.csv', header=0)
pred_df = pd.DataFrame({'sentence': test_data['sentence'], 'start': test_data['start'], 'end': test_data['end'],
                        'predict': test_data['results']})

start = []
end = []
result = []

for i in range(len(pred_df)):
    start.append(int(pred_df['start'][i] * 44.1))
    end.append(int(pred_df['end'][i] * 44.1))

    if pred_df['predict'][i] >= 0.7:
        result.append(1)
    else:
        result.append(0)


def make_quiet_wav(wav, result, start, end, output_name):
    quiet, _ = librosa.load(DATA_IN_PATH + 'quiet.wav', sr=44100)  # 무음 파일 로드
    data, _ = librosa.load(wav, sr=44100)  # 변환할 음성 파일 로드
    # data -> samplerate로 나누면 초(s) 단위

    length = len(result)  # 단위 개수
    lenq = len(quiet)  # 694575

    for i in range(0, length):
        tmp = int(end[i] - start[i])
        r = result[i]
        print("for문 : [{}] {} : {}".format(r, start[i] / 44100, end[i] / 44100))
        if (r == 1):
            if tmp > lenq:
                data[end[i] - lenq:end[i]] = quiet[:]
                print("quiet : {}:{}".format((end[i] - lenq) / 44100, end[i] / 44100))
            else:
                data[start[i]:end[i]] = quiet[:tmp] * 1.0
                print("quiet : {}:{}".format(start[i] / 44100, end[i] / 44100))
    sf.write(output_name, data, 44100)

def processVideo():
    video = cv2.VideoCapture(DATA_OUT_PATH + "copied_" + targetname + ".mp4")

    # 프레임의 width와 height가져와서 size로 저장
    fps = video.get(cv2.CAP_PROP_FPS)  # fps는 그대로 가져온다
    vid_size = (round(video.get(cv2.CAP_PROP_FRAME_WIDTH)), round(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # avi 코덱

    out = cv2.VideoWriter(DATA_OUT_PATH + "processed_" + targetname + ".avi", fcc, fps, vid_size)   # avi 확장자로 자막 처리한 영상

    while (True):
        ret, frame = video.read()

        str = "Currently, harmful language has been detected and muted."
        # "현재 유해언어가 감지되어 음소거 처리되었습니다."
        cv2.rectangle(frame, (120, 400), (730, 450), (105, 105, 105), -1)
        cv2.putText(frame, str, (170, 430), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.imshow('Result', cv2.resize(frame, (1300, 800)))
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): # q를 꼭 눌러줘야한다고 안내문 띄우기 (엔터나 다른 걸로)
            video.release()
            out.release()
            cv2.destroyWindow('Result')
            # videoclip = VideoFileClip("C:/Users/llsa0/Downloads/out.avi")  # 자막 처리된 걸 비디오 클립
            # audioclip = AudioFileClip("C:/Users/llsa0/Downloads/resultOserver.mp4")  # 음성 파일은 무음 처리된 음성용
            #
            # videoclip.audio = audioclip  # 자막 처리된 영상에 무음 덮어씌우는거
            # videoclip.write_videofile("C:/Users/llsa0/Downloads/new.mp4")  # 새로운 파일로 만드는 거
            break

def main():
    global targetloc
    global targetname
    if len(sys.argv) < 4:
        targetloc = sys.argv[1]
        targetname = sys.argv[2]

    targetname = targetname[:-4]
    print(targetname)
    video = targetloc

    data_output = DATA_OUT_PATH
    print('\nplease wait! \n')

    # 파일 복사하기 (사본 생성)
    shutil.copy2(video, data_output + "copied_" + targetname + ".mp4")
    print('\nMake copy of video ! \n')

    videoclip = VideoFileClip(data_output + "copied_" + targetname + ".mp4")
    audioclip = videoclip.audio
    audioclip.write_audiofile(data_output + "copy.wav")  # 음성 wav 추출하기
    print('\nChage mp4 to wav ! \n')
    y = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    #      0 1 2 3 4 5 6 7 8 9
    # 0 3~4 6~7

    # 0    1    2  3
    # a   1.0  3.0 아메리카노
    make_quiet_wav(data_output + "copy.wav", result, start, end, data_output + "result_{}.wav".format(targetname))
    # videoclip = videoclip.set_audio(AudioFileClip(data_output + "result_{}.wav".format(targetname)))
    # videoclip.write_videofile(data_output + "result_{}.mp4".format(targetname))

    processVideo()

    newvideoclip = VideoFileClip(data_output + "processed_" + targetname + ".avi")  # 자막 처리된 걸 비디오 클립
    newvideoclip.set_audio(AudioFileClip(data_output + "result_{}.wav".format(targetname)))
    newvideoclip.write_videofile(data_output + "result_{}.mp4".format(targetname))  # 새로운 파일로 만드는 거

    print('\nNow you can check!!! ')


if __name__ == '__main__':
    data_output = DATA_OUT_PATH
    try:
        if not os.path.exists(data_output):
            os.makedirs(data_output)
    except OSError:
        print('Error: Creating directory. ')
        quit()

    main()
    print('\nDone !!! \n')