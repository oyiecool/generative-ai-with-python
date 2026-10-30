# uv add diffusers transformers accelerate torch
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
).to("cuda")

image = pipe(
    prompt="isometric illustration of a data centre at night, soft lighting",
    num_inference_steps=4, guidance_scale=0.0,   # turbo models need very few steps
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]
image.save("out/datacentre.png")
