import gradio as gr 
from main import query, generate

def handle_query(question):
    chunks = query(question)
    answer = generate(question,chunks)
    sources = "\n".join(set(f"{c['source']}" for c in chunks))
    return answer, sources 

with gr.Blocks(title="GeoSpatial Knowledge Center") as demo:
    gr.Markdown("# GeoSpatial Knowledge Center")
    gr.Markdown("Ask anything about QGIS, Google Earth Engine, GDAL or python for spatial analysis ")
    question_input = gr.Textbox(label="Your Question", placeholder="e.g. How do I reproject a layer in QGIS?")
    submit_btn = gr.Button("Ask")
    answer_output = gr.Textbox(label="Answer", lines=10)
    sources_output = gr.Textbox(label="Sources", lines=3)

    submit_btn.click(handle_query, inputs=question_input, outputs=[answer_output, sources_output])
    question_input.submit(handle_query, inputs=question_input, outputs=[answer_output, sources_output])

demo.launch()