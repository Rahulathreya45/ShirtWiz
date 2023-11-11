from main import sqllm
import streamlit as st
st.title("ShirtWhiz Assistant")

question = st.text_input("Question: ")

if st.button("Get Answer"):
    if question:
        chain = sqllm()
        response = chain.run(question)

        st.header("Answer")
        st.write(response)