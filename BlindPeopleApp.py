import streamlit as st
import google.generativeai as genai
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from gtts import gTTS
import pyttsx3


engine = pyttsx3.init()

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  # print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file
  
genai.configure(api_key='AIzaSyAz3mJNeJ4VdEhZZzPaTXaMG03a9GeWxps')

# Create the model
generation_config = {
  "temperature": 0.75,
  "top_p": 0.95,
  "top_k": 40, # 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
  "candidate_count": 1 # ONLY 1 supported for now https://github.com/googleapis/python-aiplatform/issues/3603#issuecomment-2136310600
}


safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }


model_name="gemini-1.5-flash"
# model_name="gemini-1.5-flash-002"

# Initialize a Gemini model appropriate for your use case.
model = genai.GenerativeModel(
  model_name=model_name,
  generation_config=generation_config,
  safety_settings = safety_settings
)

def parse_json_response(response):
  if response.startswith("```json"):
    response = response.replace("```json", "")
  response = response.strip("`").strip()
  return response

def generate_multiple_llm_responses(
    prompt = "How would you invest for retirement? Be brief. Use sections, subsection, bullet points, ect. for clarity and accessibility to people with diverse background/knowledge.",
    candidate_count = 3
):
    chat_session = model.start_chat()
    responses = []
    for i in range(candidate_count or 1):
        if i == 0:
            response = chat_session.send_message(prompt)
            responses.append(response.text)
            continue
        response = chat_session.send_message("Make it better.")
        responses.append(response.text)
    return responses

sample_prompt = "Describe the content of the attached image is very simple sentences."
prompt = [sample_prompt]

st.write("# Blind People Assist")
x = st.camera_input("Take a picture, and let me explain")
if x:
    sample_image = x

    sample_image_file = upload_to_gemini(sample_image, mime_type="image/jpeg")

    prompt.append(sample_image_file)

    responses = generate_multiple_llm_responses(prompt)
    
    st.write(responses[0])
    
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)

    engine.say(responses[0])
    engine.runAndWait()

    
    
    
    
    




