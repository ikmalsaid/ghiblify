import gradio as gr
from atelier_generator import AtelierGenerator
client = AtelierGenerator(gradio=True, wm_text="Ghiblify! by ikmalsaid")

gr_css = """
footer {
    display: none !important;
}

.image-frame.svelte-rrgd5g img {
    height: 640px;
    object-fit: contain;
}

.grid-wrap.svelte-eynlr2.svelte-eynlr2 {
    overflow-y: auto;
}
"""

gr_thm = gr.themes.Default(
            primary_hue=gr.themes.colors.rose,
            secondary_hue=gr.themes.colors.rose,
            neutral_hue=gr.themes.colors.zinc
        )

lora_list = {
    'ikmalsaid/studio-ghibli': 'studio-ghibli',
    'ikmalsaid/anime-plus': 'anime-plus',
    'ikmalsaid/softserve-anime': 'softserve-anime'
}

# Initialize a cache dictionary outside the function
caption_cache = {}

def ghiblify(src, lora, mem, progress = gr.Progress()):
    progress(0.1, "Preparing image (stage 1 of 3)...")
    size, _, _ = client.size_checker(src)

    # Check if the caption is already cached
    if src in caption_cache:      
        prompt = caption_cache[src]
    
    else:
        progress(0.5, f"Processing {size} image (stage 2 of 3)...")
        prompt = client.image_caption(src)
        caption_cache[src] = prompt

    progress(0.8, f"Rendering {size} image (stage 3 of 3)...")
    result = client.image_variation(src, prompt, image_size=size, strength=0.33, lora_flux=lora_list.get(lora))
    
    if result:
        mem.insert(0, result)
        return mem
    else:
        gr.Warning('Something went wrong! Please try again.')
        return mem

with gr.Blocks(analytics_enabled=False, title='Ghiblify by ikmalsaid', css=gr_css, theme=gr_thm) as demo:
    gr.Markdown("## <br><center>Ghiblify - Transform your images to Ghibli style!")
    gr.Markdown("<center>Copyright (C) 2025 Ikmal Said. All rights reserved")
    
    with gr.Row():
        with gr.Column():
            with gr.Column(variant='panel'):
                gr.Markdown("## <center>📸 Upload Your Image!")
                src = gr.Image(type='filepath', label='Source Image', height=640, sources=['upload'])
            
            with gr.Column(variant='panel'):
                lst = gr.Radio(choices=lora_list.keys(), value=list(lora_list.keys())[0], label='Select a style:')
                run = gr.Button("Ghiblify!", variant='stop')

        with gr.Column():    
            with gr.Column(variant='panel'):
                gr.Markdown("## <center>🎨 Ghiblify It!")
                res = gr.Gallery(label='Result Image', height=814.19)
                mem = gr.State([])
   
    gr.Markdown("<br><center>Disclaimer: Due to huge demand, image processing might take longer than expected.<br>")

    run.click(
        inputs=[src, lst, mem],
        outputs=res,
        fn=ghiblify
    )

demo.launch(inbrowser=True)