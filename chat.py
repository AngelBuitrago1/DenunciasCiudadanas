import streamlit as st
import random
import time
import requests
import json
import yaml

projects = []
project_ids = []


def load_config():
    with open('config.yaml', 'r') as file:
        config_content = yaml.safe_load(file)
    return config_content


config = load_config()
api_key = config['AAI-Brain']['API-KEY']
api_secret = config['AAI-Brain']['API-Secret']


def clear_session_state():
    st.session_state.messages = []
    print("cleared")


def create_chat(project_id):
    st.session_state.messages = []
    url_create = "https://api.getodin.ai/chat/create"
    payload = json.dumps({'project_id': project_id})
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
        "content-type": "application/json"
    }
    response_create = requests.post(url_create, data=payload, headers=headers)
    conv_id = json.loads(response_create.content)["chat_id"]
    return conv_id


def get_projects():
    url_projects = "https://api.getodin.ai/projects"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
    }

    response_projects = requests.get(url_projects, headers=headers)
    projects_json = json.loads(response_projects.content)
    global projects
    projects = [project for project in projects_json['projects']]
    global project_ids
    project_ids = [project['name'] for project in projects_json['projects']]
    return projects, project_ids


# Call Projects function to fill the select-box element
get_projects()


@st.experimental_fragment
def sidebar_update():
    project_name = st.selectbox(
        "Select Project name",
        project_ids,
        index=None,
        placeholder="Select Project name...",
    )

    for project in projects:
        if project['name'] == project_name:
            project_id_selected = project['id']
            st.session_state["project_id_selected"] = project_id_selected



# Create streaming Object from Response
def response_generator(response_str):
    full_response = ""
    for word in response_str:
        time.sleep(0.01)
        yield word

st.set_page_config(page_title='Denuncias Ciudadanas - Automation Anywhere - AAI Brain', page_icon = 'https://chat-beta.automationanywhere.com/assets/icon/favicon.ico', layout='wide')
st.header("Denuncias Ciudadanas - Automation Anywhere - AAI Brain")
# st.image("https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png")
st.html("""
    <!doctype html>
    <html lang="en">
    <head>
    	<meta charset="utf-8"/>
    <title>AAI Enterprise Knowledge</title>
    </head>
    <body>
    <center> 
    <img src=https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png width=200>
    <br>
    <img src=data:image/jpeg;base64,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 width=250>
    <br>
    <iframe src='https://aa-saleseng-us-4sbx.cloud.automationanywhere.digital/copilot?tags=%5B%5D' name="aari-embedded-app" referrerpolicy="origin" width="100%" height="100%" style="border: none;"></iframe>
    </center>
    </html>
""")

# Create a sidebar using Streamlit's built-in function
with st.sidebar:
    # Call the sidebar_update() function decorator
    sidebar_update()
    # Create a primary button in the sidebar with the label "Create a new Chat"
    if st.button("Create a new Chat", type="primary"):
        clear_session_state()
        clear_session_state()
        # Set the value of the session state variable 'chat_id' to the result of calling create_chat()
        # with the 'project_id_selected' value from the session state
        st.session_state['chat_id'] = create_chat(st.session_state["project_id_selected"])



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get('image', 0) != 0:
            # print(message["image"])
            st.image(message["image"], 'Generated Image(s)')
        else:
            st.markdown(message["content"])
            # pass


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    session_state_test = st.session_state
    # Check if a chat ID has been set in the session state.
    # If not, check if a project ID has been selected.
    if session_state_test.get('chat_id', 0) == 0:
        # If no chat ID, but a project ID has been selected, create a new chat.
        if session_state_test.get('project_id_selected', 0) == 0:
            # Display a toast message prompting the user to select a project.
            st.toast('Select a project first', icon='🚨')
            st.stop()
        else:
            # Create a new chat with the selected project ID and set it as the chat ID.
            st.session_state["chat_id"] = create_chat(st.session_state['project_id_selected'])

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display user message in chat message container
    with st.chat_message("assistant"):
        chat_id = st.session_state["chat_id"]
        project_id = st.session_state["project_id_selected"]
        print(f"chat with project {project_id}")
        url_message = "https://api.getodin.ai/v2/chat/message"
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"agent_type\"\r\n\r\nchat_agent\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"message\"\r\n\r\n{prompt}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"project_id\"\r\n\r\n{project_id}\r\n-----011000010111000001101001--"
        chat_headers = {
            "accept": "application/json",
            "X-API-KEY": api_key,
            "X-API-SECRET": api_secret,
            "content-type": "multipart/form-data; boundary=---011000010111000001101001"
        }

        response = requests.post(url_message, data=payload, headers=chat_headers)

        response_message = st.write_stream(response_generator(json.loads(response.text)['message']['response']))
        images = []
        if (json.loads(response.text)['message']).get('image_urls', 0) != 0:
            print('got an image')
            print(json.loads(response.text)['message']['image_urls'][0])

            for index, image in enumerate(json.loads(response.text)['message']['image_urls'], start=1):
                images.append(image)
            image_message = st.image(images, caption=f'Generated Image(s)')
    if len(images) > 0:
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.session_state.messages.append({"role": "assistant", "image": images})
    else:
        st.session_state.messages.append({"role": "assistant", "content": response_message})


