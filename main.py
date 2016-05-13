#!/usr/bin/env python3
import wave
import json
import speech_recognition as sr
import os
import time
import webbrowser
from os import path  # obtain path to "english.wav" in the same folder as this script

length, frames, frameRate = 0, 0, 1


def divide_video():
    global length, frames, frameRate
    print("Starting the splitting part...")
    origAudio = wave.open('son.wav', 'r')
    frameRate = origAudio.getframerate()
    nChannels = origAudio.getnchannels()
    sampWidth = origAudio.getsampwidth()
    frames = origAudio.getnframes()

    length = frames / float(frameRate)
    # print (int(length/8))

    for (k, i) in enumerate(range(0, int(length), 8)):

        start = float(i)
        end = float(start + 10)

        if end >= length:
            end = length

        # print(start,end)

        origAudio.setpos(int(start * frameRate))
        chunkData = origAudio.readframes(int((end - start) * frameRate))

        chunkAudio = wave.open('nlp_{}.wav'.format(k), 'w')
        chunkAudio.setnchannels(nChannels)
        chunkAudio.setsampwidth(sampWidth)
        chunkAudio.setframerate(frameRate)
        chunkAudio.writeframes(chunkData)
        chunkAudio.close()

    print("Finishing the splitting part...")


def sound_to_text():
    NEWS = []
    for i in range(int(length / 8)):

        WAV_FILE = path.join(path.dirname(path.realpath(__file__)), 'nlp_' + str(i) + '.wav')

        # use "english.wav" as the audio source
        r = sr.Recognizer()
        with sr.WavFile(WAV_FILE) as source:
            audio = r.record(source)  # read the entire WAV file
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print(i, ". part: ", r.recognize_google(audio,language="tr"))

            NEWS.append(r.recognize_google(audio,language="tr"))

        except sr.UnknownValueError:
            # print("Google Speech Recognition could not understand audio")
            pass
        except sr.RequestError as e:
            # print("Could not request results from Google Speech Recognition service; {0}".format(e))
            pass

    return NEWS


def write_json(data):
    print("Starting the dumping part...")
    json_str = json.dumps(data , ensure_ascii=False)

    with open('video_content.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
        # print(r.recognize_google(audio), file=fp)
    print(data)
    print("Finishing the dumping part...")


def find_news(keyword, exact_search=False):
    if exact_search:
        keyword = " " + keyword + " "
    with open('topic_detection.json', 'r') as f:
        data = json.load(f)

    most_relevant_news = None

    for haber in data['haber']:
        counter = 0
        # print(haber)
        for i in haber['content']:
            if i.lower().count(keyword.lower()) > 0:
                haber_id = haber['id']
                time_start = haber['begin']
                time_finish = haber['end']
                counter += i.lower().count(keyword.lower())
        haber['keyword_count'] = counter
        if most_relevant_news is None or haber['keyword_count'] > most_relevant_news['keyword_count']:
            most_relevant_news = haber
            # print("Found in", i, "# of", most_relevant_news['id'])
    most_relevant_news['keyword'] = keyword
    most_relevant_news['youtube'] = data['youtube']
    print(
        "You search for '{0}'.Result is: The news with id {1}, # of '{0}' are {2} which starts at {3}, finishes at {4}.".format(
            most_relevant_news['keyword'], most_relevant_news['id'], most_relevant_news['keyword_count'],
            most_relevant_news['begin'],
            most_relevant_news['end']))
    return most_relevant_news


# function call stack
#divide_video()  # only for video splitting

'''
data = {
    'id': 1,
    'content': sound_to_text(),
    'begin': '00:00',
    'end': frames / float(frameRate)
}
'''


#write_json(data)


most_relevant_news = find_news("kobani")
try:

	begin_time = most_relevant_news['begin'].split(':')
	hour = int(begin_time[0])
	minute = int(begin_time[1])
	second = int(begin_time[2])
	video_link = "https://www.youtube.com/watch?v={0}&t={1}h{2}m{3}s".format(most_relevant_news['youtube'],hour,minute,second)

except:
	begin_time = most_relevant_news['begin'].split(':')
	minute = int(begin_time[0])
	second = int(begin_time[1])
	video_link = "https://www.youtube.com/watch?v={0}&t={1}s".format(most_relevant_news['youtube'], minute*60+second)

controller = webbrowser.get()
controller.open(video_link)


print ("video opened")

# os.system("start C:\\Users\\Ayse\\Desktop\\videolar\\Yeniklasör\\uzun_haber.mp4")    #localde açmak
