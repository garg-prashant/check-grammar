import streamlit as st
import openai
from openai.error import AuthenticationError, RateLimitError


def is_key_loaded(openai_api_key):
    st.session_state["openai_api_key"] = openai_api_key
    st.session_state["loaded"] = True
    return True


def rectify_grammar(openai_api_key, original_text):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f'Rephrase, rectify the Grammar and Typos in the message delimited by triple backticks ```{original_text}```',
        max_tokens=1000,
        temperature=0,
        stream=False,
    )
    return response["choices"][0]["text"]


def main():
    st.title("Grammar Rectification Application")
    st.sidebar.title("OpenAI API Key")
    api_settings_message = "You can get this key from OpenAI settings. (https://platform.openai.com/account/api-keys)\n Example: sk-**************************"
    openai_api_key = st.sidebar.text_input(api_settings_message, type="password")
    api_load_button = st.sidebar.button("Load API Key")
    
    st.session_state["loaded"] = False

    if api_load_button:
        is_key_loaded(openai_api_key)

    if st.session_state.get("openai_api_key") and st.session_state.get("loaded"):
        st.sidebar.info("OpenAI API key provided is loaded")

    original_text = st.text_area("Input your text", max_chars=2000, height=300)
    st.write("---")
    check_grammar_button = st.button("Check Grammar")

    try:
        if check_grammar_button:

            word_count = len(original_text.split())
            st.write("Number of words:", word_count)
            
            if not original_text:
                st.error("No text provided to be rectified")
                return
            
            if not st.session_state.get("openai_api_key") and not st.session_state.get("loaded"):
                st.error("No valid OpenAI API key provided")
                return 

            with st.spinner("Rectifying original text"):
                response = rectify_grammar(openai_api_key, original_text)

            if response:
                st.header("Corrected Text")
                st.text_area("Corrected text with grammar and typo mistakes", value=response.replace("```", ""), height=300, disabled=True, key="ct")
    except AuthenticationError as err:
        st.error(f"Invalid OpenAI API key provided: {err}")
    except RateLimitError as err:
        st.error(f"OpenAI API key rate limit exceeded: {err}")
    except Exception as err:
        st.error(f"Issues while rephrasing and correcting the grammar: {err}")


if __name__ == "__main__":
    main()