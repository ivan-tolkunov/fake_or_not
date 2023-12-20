import gradio as gr
from dataclasses import dataclass, field
from fastai.vision.all import *

from fastapi import FastAPI
from modal import Image, Secret, Stub, asgi_app

image = (
    Image.debian_slim(python_version="3.9")
    .pip_install(
        "gradio",
        "fastai",
        "fastapi",
    )
    .copy_local_dir('models', '/models')
)

stub = Stub(name="fake-or-not", image=image)

web_app = FastAPI()


def predict(inp):
    model = load_learner('/models/realOrFake_resnet18_224px.pkl')
    model.eval()

    result ,_ , probs = model.predict(inp)
    print(result, probs)
    return {'ai': float(probs[0]), 'real': float(probs[1])}


@stub.function()
@asgi_app()
def run():
    from gradio.routes import mount_gradio_app

    return mount_gradio_app(
        app=web_app,
        blocks=gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=3),
             examples=[]),
        path="/",
    )
