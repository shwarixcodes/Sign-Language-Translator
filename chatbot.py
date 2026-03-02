import streamlit as st
st.set_page_config(page_title="Text to Sign Converter", layout="centered")

st.markdown("""
    <style>
    body, [data-testid="stApp"]{
        background-color: #c6cacf2c;
    }
    .stTextInput > div > div > input {
        background-color: #c4c8cd;
        color: #031418;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 20px;
    }
    .heading p.p1{
        text-align: center;
        margin-top: -70px;
        font-size: 40px;
        color: #5e5252;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .heading p.p2{
        text-align:center;
        margin-top: -20px;
        font-size: 20px;
        color:#6c635d;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .input-msg{
        text-align: left;
        background-color: #32597dc4;
        color: rgb(255, 255, 255);
        padding: 10px;
        font-size: 18px;
        border-radius: 5px;
        margin-top: 50px;
        margin-right: 10px;
        margin-left: 30px;
        float: left;
    }
    .error-msg{
        text-align: right;
        background-color: #11253ac4;
        color: rgb(255, 255, 255);
        padding: 5px;
        font-size: 18px;
        border-radius: 5px;
        margin-top: 80px;
        margin-right: 10px;
        margin-left: 30px;
        float: right;
    }
    .styled-video{
        margin-top: -100px;
        width: 150px;
        height: 200px;
    }
    .input-prompt{
        background-color: #3e3f41;
        color: #ffffff ;
        font-size: 20px;
        margin-bottom: 20px;
    }
    button{
        background-color: #182738   !important;
        color: #efedeb  !important;
        border: none !important;
    }
    /*Hide Streamline header*/
    header, footer, #MainMenu {
            visibility: hidden;
        }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="heading">
        <p class="p1">Text-to-Sign Language Converter </p>
        <p class="p2">Your AI-powered Sign Language Partner</p>
    </div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "has_prompted" not in st.session_state:
    st.session_state.has_prompted = False

for interaction in st.session_state.history:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"<div class='input-msg'>{interaction['input']}</div>", unsafe_allow_html=True)
    with col2:
        if interaction['video']:
            st.markdown("<div class='styled-video'></div>", unsafe_allow_html=True)
            st.video(interaction['video'])
        else:
            st.markdown(f"<div class='error-msg'>{interaction['response']}</div>", unsafe_allow_html=True)

sign_videos = {
    "hello": r"media\hello.mp4",
    "hi": r"media\hello.mp4",
    "hey": r"media\hello.mp4",
    "thank you": r"media\thankyou.mp4",
    "thankyou": r"media\thankyou.mp4",
    "thanks": r"media\thankyou.mp4",
    "thanku": r"media\thankyou.mp4",
    "yes": r"media\yes.mp4",
    "yeah": r"media\yes.mp4",
    "no": r"media\no.mp4",
    "nope": r"media\no.mp4",
    "please": r"media\please.mp4",
    "pls": r"media\please.mp4",
    "plz": r"media\please.mp4",
    "help": r"media\help.mp4",
    "what": r"media\what.mp4",
    "eat": r"media\eat.mp4",
    "more": r"media\more.mp4",
    "how are you": r"media\how_are_you.mp4",
    "how r u": r"media\how_are_you.mp4",
    "i am fine": r"media\im_fine.mp4",
    "i'm fine": r"media\im_fine.mp4",
    "nice to meet you": r"media\nice_to_meet_you.mp4",
    "see you later": r"media\see_you_later.mp4",
    "you are welcome": r"media\welcome.mp4",
    "it's okay": r"media\its_okay.mp4"
}

st.markdown('<div class="input-prompt">', unsafe_allow_html=True)
with st.form(key="chat", clear_on_submit=True):
    cols = st.columns([5, 1])
    user_input = cols[0].text_input("Enter your prompt here:", label_visibility="collapsed")
    submitted = cols[1].form_submit_button("Send")
st.markdown('</div>', unsafe_allow_html=True)

if submitted and user_input.strip() != "":
    st.session_state.has_prompted = True
    found = False
    matched_keyword = ""
    matched_video = ""

    for keyword in sign_videos:
        if keyword in user_input.lower():
            matched_keyword = keyword
            matched_video = sign_videos[keyword]
            found = True
            break

    if found:
        st.session_state.history.append({
            "input": user_input,
            "response": f" {matched_keyword}",
            "video": matched_video
        })
    else:
        st.session_state.history.append({
            "input": user_input,
            "response": "🙁 Sorry, I don’t know that sign yet.",
            "video": None
        })
    st.rerun()