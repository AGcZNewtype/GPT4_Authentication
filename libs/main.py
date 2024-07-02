import streamlit as st
import tempfile
from pathlib import Path
import base64
import text_unit
import GPT_api
from BERT_model import BertModelWrapper

#临时会话框
@st.experimental_dialog("Please answer the question!",width="large")
def authenticator(ques,ans):
    st.write("请回答以下问题?")
    # st.write(ques,ans)
    evidence_list = []

    #遍历问题和会话框
    for i, question in enumerate(ques):
        st.write(f"问题 {i + 1}: {question}")
        reason = st.text_input(f"回答问题 {i + 1}", key=f"answer_{i}")
        if len(reason) != 0:
            evidence_list.append(reason)

    #提交后进行问题验证
    if st.button("提交回答"):
        if len(evidence_list) == len(ques):
            st.session_state.vote = {"evidence": evidence_list}
            st.success("回答已提交！")
            # st.write(evidence_list)

            #创建bert模型并对结果进行验证
            BertModel = BertModelWrapper()
            total_similarity = []

            for i in range(len(ques)):
                evidence = evidence_list[i]
                total_similarity.append(BertModel.sentence_match(evidence, ans[i]))

            # text_unit.avg_similarity(total_similarity)
            st.write(text_unit.avg_similarity(total_similarity))
            st.rerun()
        else:
            #清空对话框
            evidence_list = []
            st.write("请回答全部问题")



def upload():
    file = st.file_uploader("选择待上传的PDF文件", type=['pdf'])

    #预览上传文件
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(file.getvalue())
            with open(tmp_file.name, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                          f'width="800" height="1000" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

            if st.button("验证作者身份",use_container_width=True):
                # 读取PDF文件
                file = text_unit.extract_text_from_pdf(tmp_file.name)

                # 使用GPT生成问题和答案
                # response = GPT_api.GPT_generation(file)

                # 对GPT回答进行切分归类处理
                # ques, ans = text_unit.response_split(response)
                ques = ["111111","222222"]
                ans = ["1","2"]

                #打开临时会话，回答问题并进行验证(同时传入文件以进行保存)
                authenticator(ques,ans,file)




if __name__ == '__main__':
    st.title('PDF File Uploader')
    upload()