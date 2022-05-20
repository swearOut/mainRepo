# Deep Learning-Based Harmful Language In Video Blocking System    : 딥러닝 기반 영상 속 유해 언어 차단 시스템   

## 1. Why did we create this system?
  ### - Intention
   > 본 프로젝트는 영상 속 유해 언어를 필터링하여 새롭게 재가공된 영상을 제공해주는 시스템을 개발에 대한 프로젝트 입니다. 
   > 영상 속 유해 언어의 대한 경각심을 깨우고, 이를 해결하기 위한 하나의 방안을 제시합니다. 
   > 부적절한 표현을 포함하거나 그러한 의미를 가진 **문장 전체** 를 묵음 처리하는 것이 목표이며, 대상 언어는 **한국어** 로 한정하였습니다.    
   ### - Reference / Existing similar technology
   >   <a href="https://github.com/LEEMINJOO/Beeeep--" target="_blank">Beep--</a>
   ### - Result video
   #### * Before
   
   <a href="https://www.youtube.com/watch?v=2XfxteQwF8M" target="_blank">원본 영상: 멜로가 체질</a>
   
   #### * After
   https://user-images.githubusercontent.com/74697898/161960648-a7ee7f50-b17c-48b8-b11d-15c193a6d932.mp4


    
## 2. The techniques we use.
   ### - STT (clova)

   > 이 프로젝트에서는 특정 목소리만 편향되어 인식될 수 있는 문제를 방지하기 위해, 
   > STT 기술을 이용한 음성의 텍스트화가 선행되어야 한다고 판단하였습니다. 
   > 여러 STT 기술의 특성을 고려하였으나,한국어 정확도가 가장 높고, 문장의 시작과 종료 타임 스탬프를 제공하는 
   >  **CLOVA Speech Recognition** 을 사용하게 되었습니다.    
 
   ### - Dataset   

   |번호|이름|링크|
   | :---: | :---: | --- |
   | `1` | 이름 | https://github.com/2runo/Curse-detection-data |
   | `2` | 이름 | https://raw.githubusercontent.com/ZIZUN/korean-malicious-comments-dataset/master/Dataset.csv |
   | `3` | 이름 | https://www.kaggle.com/c/korean-gender-bias-detection/data?select=dev.gender_bias.binary.csv |
  
   ### - Model (CNN)
   
  <p align="center"><img width="453" alt="cnn 텍스트 분류 구조" src="https://user-images.githubusercontent.com/74697898/161954347-c1b66c04-2b45-429b-8d02-22c77aaac134.PNG">  </p>   

  <p align="center"><img width="568"  alt="모델 구조" src="https://user-images.githubusercontent.com/74697898/161954468-6f29a0e6-4fa8-4757-afcb-7aeac7fbf484.PNG"></p>
   
   > 먼저 임베딩 벡터를 생성하고, 1차원의 sequential 데이터를 다루는 Keras의 Conv1D를 합성곱 레이어로 사용합니다. 
   > 세 개의 레이어의 kernel size를 3, 4, 5로 다르게 하여 값을 추출하고,  
   > 합성곱 연산 이후 가중치를 줄이기 위해 맥스 풀링 레이어를 적용합니다.
   > 과적합을 방지하기 위해 dropout과 Dense layer를 사용한 완전 연결 계층(fully-connected)을 쌓고, early stopping을 사용합니다.
   > Dense layer는 활성화 함수로 RELU 함수를 사용하고, 마지막 층에서는 Sigmoid 함수를 사용합니다. . 
   > 모든 레이어를 통과한 후 예측값은 0부터 1까지의 실수로 표현되며, 1에 가까울 수록 유해한 표현이라고 판단할 수 있습니다.       
   ### - Web Server
   ![image](https://user-images.githubusercontent.com/74697898/161416270-8fcf92b8-6704-4083-9565-8cda6dff7d2f.png)
  
   + 사용자가 본페이지로 접속할 때 나타나는 첫 페이지 화면
   + 동영상 업로드 박스 안에서 'Select' 버튼을 클릭할 경우, 사용자는 유해 언어 필터링 변환을 원하는 동영상을 선택 가능
   + 그 후 Submit 버튼을 클릭하여 웹페이지 서버로 요청
   
   ![image](https://user-images.githubusercontent.com/74697898/161416276-78b8f5e7-bdd5-46be-abcf-d0801cfbfa00.png)
   
   + 동영상 필터링이 성공적으로 끝났을 경우에 나타나는 페이지 화면
   + 변환 도중 오류가 발생하면 오류 문구가 출력
   + 이 페이지에서 '업로드 파일 목록' 버튼을 클릭하면 아래의 화면으로 이동
   
   ![image](https://user-images.githubusercontent.com/74697898/161416280-a8549b12-c7f1-4135-8ba3-bc30c5facb1b.png)
   
   + 해당 파일 목록에서 다운받을 필터링 동영상을 클릭하여 원하는 경로로 다운로드 가능   
     
## 3. Directions

https://user-images.githubusercontent.com/68285994/161953255-73657438-7426-4078-bce3-8999b03ff2f1.mp4

## 4. File hierarchy description
   
   <p align="center"><<img src="https://user-images.githubusercontent.com/74697898/161954116-e9411250-3c33-48c6-a242-d41b0944cf7a.PNG" width="700px"></p>
   
 + Banner image 
   + Css
   + inputData - 업로드 된 동영상들을 담아두는 임시 디렉토리
   + outputData - 재가공 된 영상들을 담아두는 임시 디렉토리
   + pythonDIr 
   + Download.php - 다운로드 로직이 담겨 있는 php 파일
   + file_list.php - 다운로드 받을 수 있는 파일을 목록화한 페이지 
   + Upload.php - 업로드 할 수 있는 페이지
   + upload_process.php - 업로드 후 처리 결과를 보여주는 페이지
   
## 5. Current Development Status
  ### - OpenCV Library
   ![subtitlecapture](https://user-images.githubusercontent.com/67897318/162181108-3d114082-6731-425d-b7a5-c33b27902fb1.png)
    
   ### 현 시스템으로는 문장 전체 음소거로 인해 문맥 파악에 어려움이 있어 개선이 필요함
   > 대안 1. 자막 생성 (유해언어 판정 시, 안내 문구 및 자막 처리) 



   > 대안 2. 옵션 선택 (단어 단위 묵음 처리 / 문장 단위 묵음 처리)  












    
   + OpenCV의 VideoCapture 사용하여 동영상에 자막 생성 성공
   + OpenCV VideoCaputure는 waitkey()를 사용해 키보드의 입력이 있어야만 종료 가능
   + OpenCV에서 카메라로부터 전달받은 영상을 저장하기 위해서 VideoWriter 클래스 사용
   + VideoWriter 클래스 인스턴스 생성시 아래와 같은 파라미터 사용 필요
   </br>
   
    ps = video.get(cv2.CAP_PROP_FPS ) #fps는 그대로 가져오기
    vid_size = (round(video.get(cv2.CAP_PROP_FRAME_WIDTH)), round(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X') # avi 코덱
    
    
   + 자막 처리 방식은 OpenCV로 자막 영역에 해당하는 직사각형을 입힌 뒤 putText()를 사용해 안내 문구를 출력함
   </br>
        
    cv2.rectangle(frame, (120, 400), (730, 450), (105, 105, 105), -1)   # 자막 배경 생성
    cv2.putText(frame, str, (170, 430), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))   # 안내문구 출력
    cv2.imshow('Result', cv2.resize(frame, (1300, 800)))
        
   + OpenCV 사용 시 음성처리 불가
   + 자막 처리한 영상을 VideoFileClip()을 이용해 새로운 영상으로 만든 뒤, set_audio()를 사용해 소리를 적용함
   </br>

    newvideoclip = VideoFileClip(data_output + "processed_" + targetname + ".avi")  # 자막 처리 후 비디오 클립으로 생성
    newvideoclip.set_audio(AudioFileClip(data_output + "result_{}.wav".format(targetname)))   # 처리된 비디오에 음성 적용
    newvideoclip.write_videofile(data_output + "result_{}.mp4".format(targetname))  # 자막+음성 적용된 영상으로 가공
