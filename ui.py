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


def predict(fake_or_real):
    model = load_learner('/models/realOrFake_resnet18_224px.pkl')
    model.eval()

    result ,_ , probs = model.predict(fake_or_real)
    print(result, probs)
    return {'ai': float(probs[0]), 'real': float(probs[1])}


@stub.function()
@asgi_app()
def run():
    import gradio as gr
    from gradio.routes import mount_gradio_app

    return mount_gradio_app(
        app=web_app,
        blocks=gr.Interface(fn=predict,
             inputs=gr.Image(type="pil"),
             outputs=gr.Label(num_top_classes=2),
             examples=[
                    ["https://ucarecdn.com/6a1b67e4-24f0-4f2e-9d63-852dcf1e97bd/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/a43f44c3-356d-4f1a-8575-0afc65606357/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/56b1e573-e821-4615-acaa-ab3d9f85c78c/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/eb4375c0-d16b-48fd-898a-c40e56882c83/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/707eafed-8bc8-4724-bd82-655ec8df6109/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/e8ac921d-8bad-4eb5-a575-185f9094fb95/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/491c0bb6-3e12-49b1-8167-5eb6def63cae/-/scale_crop/512x512/smart/"],
                    ["https://ucarecdn.com/af3b1254-5f89-4087-b2ac-370115083d48/-/scale_crop/512x512/smart/"],
             ]),
        path="/",
    )
