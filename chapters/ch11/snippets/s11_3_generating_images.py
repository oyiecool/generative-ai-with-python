import base64
from openai import OpenAI

client = OpenAI()
img = client.images.generate(
    model=s.image_model,          # your provider's current image model
    prompt="Flat vector illustration of a server rack with a green shield, "
           "corporate blue palette, no text",
    size="1024x1024",
)
Path("out/security_banner.png").write_bytes(base64.b64decode(img.data[0].b64_json))
