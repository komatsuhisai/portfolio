import streamlit as st
import requests
import base64
import time
import re
import datetime
from concurrent.futures import ThreadPoolExecutor

# 音声合成の最小文字数。小さすぎると安定しない場合があります。
SPLIT_THRESHOLD = 4
# 息継ぎの秒数（s）
TIME_BUFFER = 0.1
# 待機中の実行スパン（s）
SLEEP_ITER = 0.2
# APIのそれぞれのURL
CHATBOT_ENDPOINT = 'http://localhost:8000/chat'
TTS_ENDPOINT = 'http://localhost:8000/tts'


def split_text(text:str):
    text_list = re.split('[\n、。]+', text)
    text_list_ = []
    for text in text_list:
        if text == '':
            continue
        if len(text) < SPLIT_THRESHOLD:
            try:
                text_list_[-1] = text_list_[-1] + '。' + text
            except IndexError:
                text_list_.append(text)
        else:
            text_list_.append(text)
    if len(text_list[0]) < SPLIT_THRESHOLD and len(text_list_) > 1:
        text_list_[1] = text_list[0] + '。' + text_list_[1]
        text_list_ = text_list_[1:]
    return text_list_

def get_tts_sound(text:str, url=TTS_ENDPOINT):
    params = {'text': text}
    response = requests.get(url, params=params)
    return response.content, datetime.datetime.now()

def sound_player(response_content:str):
    # 参考：https://qiita.com/kunishou/items/a0a1a26449293634b7a0
    audio_placeholder = st.empty()
    audio_str = "data:audio/ogg;base64,%s"%(base64.b64encode(response_content).decode())
    audio_html = """
                    <audio autoplay=True>
                    <source src="%s" type="audio/ogg" autoplay=True>
                    Your browser does not support the audio element.
                    </audio>
                """ %audio_str

    audio_placeholder.empty()
    time.sleep(0.5)
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

def get_chat_response(text:str, url=CHATBOT_ENDPOINT):
    params = {'text': text}
    response = requests.get(url, params=params)
    return response.text

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    query = st.text_input('質問を入力してください')
    button = st.button('実行')

    if button:
        # チャットボットの返信を取得
        response_text = get_chat_response(query)
        st.write(f'回答：{response_text}')

        # 返信を分割
        split_response = split_text(response_text)
        executor = ThreadPoolExecutor(max_workers=2)
        futures = []
        
        # 並行処理として音声合成へ
        for sq_text in split_response:
            future = executor.submit(get_tts_sound, sq_text)
            futures.append(future)
        
        block_time_list = [datetime.timedelta() for i in range(len(futures))]
        current_time = datetime.datetime.now()
        # 結果をwaitし、再生可能時間になり次第再生する
        res_index = 0
        gap_time = datetime.timedelta()
        while res_index < len(futures):
            future = futures[res_index]
            if future.done():
                if res_index==0:
                    base_time = datetime.datetime.now()
                if datetime.datetime.now() >  base_time + block_time_list[res_index]:
                    for i in range(len(block_time_list)):
                        if i > res_index:
                            # 音声長を計算。音声は32bitの16000Hz、base64エンコードの結果は1文字6bitの情報であるため、下記の計算で算出できます
                            block_time_list[i] += datetime.timedelta(seconds=(len(future.result()[0])*6/32/16000)+gap_time.total_seconds()+TIME_BUFFER)
                    st.write(f'　実行完了：{split_response[res_index]}')
                    st.write(f'　実行時間：{(future.result()[1] - current_time).total_seconds():.3f}s')
                    st.write(f'　音声の長さ：{len(future.result()[0])*6/32/16000:.3f}s')
                    sound_player(future.result()[0])
                    res_index += 1
                    gap_time = datetime.timedelta()
            elif res_index!=0:
                gap_time += datetime.timedelta(seconds=SLEEP_ITER)
            time.sleep(SLEEP_ITER)
        executor.shutdown()