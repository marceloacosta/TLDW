# Ask YouTube
This application allows you to enter the URL of a YouTube video and ask questions about its content. The application uses the video's transcript to search for answers to your questions.

## Description
The Ask YouTube web application is a tool that makes it easier to search for information in YouTube videos. By leveraging the power of the video's transcript and advanced language models, it provides a convenient way to find answers to specific questions about the content without watching the entire video.

## Requirements
To run the application, you will need the following:
<pre>
Python 3.6 or higher
Streamlit
Google API Python Client
YouTube Transcript API
OpenAI API
</pre>
To install the required packages, you can use the following command:

<pre>
pip install streamlit google-api-python-client youtube_transcript_api openai
</pre>
## Setup
Clone the repository or download the source code.
Create a .env file in the project directory with the following content:
<pre>
OPENAI_API_KEY=<your_openai_api_key>
YOUTUBE_API_KEY=<your_youtube_api_key>
</pre>
Replace your_openai_api_key and your_youtube_api_key with your actual API keys for OpenAI and YouTube Data API, respectively.

Run the application using the following command:
<pre>
streamlit run app.py
</pre>
The application will be accessible via your web browser at http://localhost:8501.

## Usage
Enter the URL of the YouTube video you want to ask questions about.
Type your question in the provided input field.
Click "Get answer" to retrieve the answer based on the video's transcript.
If an answer is found, it will be displayed below the input field.
Enjoy exploring YouTube content with Ask YouTube!