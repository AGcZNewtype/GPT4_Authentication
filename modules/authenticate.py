import streamlit as st
import tempfile
from pathlib import Path
import base64
from modules import text_unit, GPT_api, web_unit
import os
from modules.BERT_model import BertModelWrapper


# Temporary session box for authentication
@st.experimental_dialog("Please answer the question!", width="large")
def authenticator(ques, ans, tmp_file, original_filename):

    st.write("Please answer the following question?")
    print(ques, ans)
    evidence_list = []

    # Iterate through the questions and display input boxes for answers
    for i, question in enumerate(ques):
        st.write(f"Question {i + 1}: {question}")
        reason = st.text_input(f"Please answer {i + 1}", key=f"answer_{i}")
        if len(reason) != 0:
            evidence_list.append(reason)

    # Verify answers upon submission
    if st.button("Submit"):
        if len(evidence_list) == len(ques):
            st.session_state.vote = {"evidence": evidence_list}
            st.success("Answer submitted!")
            # st.write(evidence_list)

            # Create BERT model and validate the results
            BertModel = BertModelWrapper()
            total_similarity = []

            for i in range(len(ques)):
                evidence = evidence_list[i]
                total_similarity.append(BertModel.sentence_match(evidence, ans[i]))

            similarity = text_unit.avg_similarity(total_similarity)
            # print(text_unit.avg_similarity(total_similarity))

            item_id = hash(original_filename)
            # Save to the database
            web_unit.add_result(item_id, original_filename, st.session_state['username'], similarity)
            # Save and close the temporary file
            save_uploaded_file(tmp_file, original_filename)
            os.remove(tmp_file)
            st.rerun()


        else:
            # Clear the dialog box if not all questions are answered
            evidence_list = []
            st.warning("Please answer all the questions!")

# Method to save the uploaded file
def save_uploaded_file(tmp_file_path, original_filename):
    # Define the save path
    save_dir = Path("upload_files")
    save_dir.mkdir(parents=True, exist_ok=True)

    # Save the uploaded file
    saved_file_path = save_dir / original_filename
    with open(saved_file_path, "wb") as f:
        f.write(Path(tmp_file_path).read_bytes())

# Upload function to handle file upload and processing
def upload():
    file = st.file_uploader("Please choose the file", type=['pdf'])

    # Preview the uploaded file
    if file is not None:
        file_name = file.name

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            fp = Path(tmp_file.name)
            fp.write_bytes(file.getvalue())
            with open(tmp_file.name, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" ' \
                          f'width="800" height="1000" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

            #Start authentication
            if st.button("Authenticate", use_container_width=True):

                # Convert the file to plain text
                file = text_unit.extract_text_from_pdf(tmp_file.name)

                # Use GPT to generate questions and answers
                response = GPT_api.GPT_generation(file)

                # Split and categorize GPT responses
                ques, ans = text_unit.response_split(response)

                ques = ["1", "2"]
                ans = ["1", "2"]
                # Open the temporary session, answer questions, and verify (pass the file for saving)
                authenticator(ques, ans, tmp_file.name, file_name)



