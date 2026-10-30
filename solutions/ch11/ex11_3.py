for seed in (1, 2, 3):
    for steps in (1, 4):
        img = pipe(prompt=PROMPT, num_inference_steps=steps, guidance_scale=0.0,
                   generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        img.save(f"out/seed{seed}_steps{steps}.png")
