import requests
import json
import pandas as pd
import sys
import os


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/1428/033d0c63fe88517b2873ae2338de0c3d31d6c82b80b148ae5ed1533446e1808a'
    # Clova Speech secret key
    secret = 'c97b05ce69694ad0b0a4e47cb103150d'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'))

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
            
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response

def main():
    global targetloc 
    
    if len(sys.argv) < 3:
       targetloc = sys.argv[1]

    res = ClovaSpeechClient().req_upload(file=targetloc, completion='sync')

    with open('clovatest.json', 'w', encoding='UTF-8') as f:
        f.write(res.text)

    with open("clovatest.json", "r", encoding="utf8") as f:
        contents = f.read() # string 

    json_d = json.loads(res.text)
    sentence = []
    start = []
    end = []

    for i in range(0, len(json_d["segments"])):
        sentence.append(json_d["segments"][i]['text'])
        start.append(json_d["segments"][i]['start'])
        end.append(json_d["segments"][i]['end'])
    
    df = pd.DataFrame({'sentence':sentence, 
                 'start' : start,
                 'end' : end})

    # df.to_csv('./csvData/STTResult_'+ targetname+'.csv', ',' ,index=False)
    df.to_csv('./csvData/STTResult.csv', ',' ,index=False)
    
if __name__ == '__main__':
    main()
   
    