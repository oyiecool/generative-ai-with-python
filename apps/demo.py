# apps/demo.py     (uv add gradio)
import gradio as gr

from aikit.llm import LLM, Message

llm = LLM()


def respond(message, history):
    msgs = [Message(h["role"], h["content"]) for h in history] + [Message("user", message)]
    partial = ""
    for piece in llm.stream(message):                 # simple single-turn stream for demos
        partial += piece
        yield partial


gr.ChatInterface(respond, type="messages", title="Change Summary Assistant").launch()
