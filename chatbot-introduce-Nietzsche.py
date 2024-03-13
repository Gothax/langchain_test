from langchain.callbacks.base import BaseCallbackHandler
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_api_key")[1:-1]
MODEL='gpt-3.5-turbo'

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

want_to = """너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
프리드리히 빌헬름 니체(독일어: Friedrich Wilhelm Nietzsche, 1844년 10월 15일 ~ 1900년 8월 25일)는 독일의 철학자[1]이다. 서구의 전통을 깨고 새로운 가치를 세우고자 했기 때문에 '망치를 든 철학자'라는 별명이 있다. 그는 그리스도교 도덕과 합리주의의 기원을 밝히려는 작업에 매진하였고, 이성적인 것들은 실제로는 비이성과 광기로부터 기원했다고 주장했다. 실제로 그는 안티크리스트에서 유대인들이 그들의 망상으로 도덕이나 종교, 문화, 역사 등을 복구가 불가능할 정도로 왜곡했다고 말했다. 이는 유대인 혐오의 근거가 되기도 했는데, 니체에 의하면 유대인은 세계의 외면은 물론 내면도 포함해 모든 것을 사기날조로 전복하는 운명적 민족이자 노예 혹은 약자로서 중요성이 있으며 귀족 같은 정신을 가진 고귀한 자들의 진정한 적이다. 그러나 니체는 강자의 입장을 찬양하면서도 때때로 약자의 도덕 등을 칭송하기도 해서 모순도 있다. 관념론과 기독교는, 세계를 두 개로 구분짓는다. 이를테면 기독교는 이승 이외에도 하늘나라가 있다고 가르친다. 또한 플라톤은 세계를 현상계와 이데아계로 이분한다. 니체는 이러한 구분에 반대하며 '대지에서의 삶을 사랑할 것'을 주창하였다. 또한 현실에서의 삶을 비방하는 자들을 가리켜 퇴락한 인간[2]이라 부르며 비판하였다. 이렇듯, '영원한 세계'나 '절대적 가치'를 인정하지 않는다는 점에서 니체는 관념론적 형이상학에 반대한다. 니체는 기독교 신자들이 예수의 가르침과 달리, 안 믿으면 지옥 간다는 멸망적 교리만을 전했다며 기독교를 비판했다[3]

니체는 전체주의, 민족주의, 국가주의, 반유대주의 등을 비판했다. 그러나 그의 사상이 파시스트들에게 왜곡되기도 했다. 진리의 가치를 묻는 그의 질문은 해석상의 문제를 제기했다.
니체는 1844년 10월 15일 예전의 프로이센 (독일)의 작센 지방의 작은 마을인 뢰켄(Röcken)에서 루터교 목사의 아들로 태어났다. 그의 이름은 프러시아의 왕인 프리드리히 빌헬름 4세에게서 빌려온 것으로, 빌헬름 4세는 니체가 태어나던 날에 나이가 49세를 넘어있었다(니체는 훗날 그의 이름에서 가운데에 있던 "빌헬름"을 빼 버렸다.[4]) 니체의 아버지인 카를 빌헬름 루트비히 니체(1813-1849)는 루터교회 목사이자 전직 교사이었고, 프란치스카 욀러(1826~1897)와 1843년에 결혼하였다. 그의 여동생인 엘리자베스 니체는 1846년에 태어났고, 뒤를 이어 남동생인 루드비히 요셉이 1848년에 태어났다. 니체의 아버지는 뇌 질환으로 1849년에 세상을 떠났다. 그의 어린 남동생은 1850년에 죽었다. 그 후 가족은 나움부르크로 이사를 갔고, 그곳에서 니체의 할머니와 어머니 프란치스카, 아버지의 결혼하지 않은 두 자매, 두 하녀들과 함께 살며 어린시절을 보냈다. 니체의 할머니가 1856년에 세상을 하직하자, 가족은 그들의 집으로 이사했다.

{}
"""

content={}

st.info("니체와 관련된 된 내용을 알아볼 수 있는 Q&A 로봇입니다.")
st.info("You can ask questions about Friedrich Nietzsche")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="어떤 내용이 궁금하신가요?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=api_key, streaming=True, callbacks=[stream_handler], model_name=MODEL)
        response = llm([ ChatMessage(role="system", content=want_to.format(content))]+st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))