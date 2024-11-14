
import gradio as gr
from master_agent import MasterAgent

# I am using Gradio for the chat interface


def answer(message, history):
    return MasterAgent().process(message, history)


chat = gr.ChatInterface(answer, type="messages", theme=gr.themes.Citrus(), title="OpenAI Function Calls")

if __name__ == '__main__':
    chat.launch()
