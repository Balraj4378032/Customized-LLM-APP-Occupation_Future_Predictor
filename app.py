import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

def respond(
    message,
    history,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    system_message = "Welcome to the Occupation Future Predictor! I'm here to provide insights and predictions about future job trends, emerging industries, skill demands, and more. Whether you're looking for advice on career planning, future-proof skills, or industry transformations, feel free to ask. How can I assist you today?"
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response

demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="Welcome to the Occupation Future Predictor!", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
    examples=[
        ["What are the future job trends in technology?"],
        ["Which industries are expected to grow in the next decade?"],
        ["What skills will be in high demand in 2030?"],
        ["How will automation impact job markets?"],
        ["What are the top future-proof careers?"],
        ["How can I prepare for jobs that don't exist yet?"],
        ["What is the future of remote work?"],
        ["What are the emerging industries of the 2020s?"],
        ["How will AI and robotics affect employment?"],
        ["What are the future opportunities in renewable energy?"],
        ["How can I adapt to the changing job landscape?"],
    ],
    title='Occupation Future Predictor 📈'
)

if __name__ == "__main__":
    demo.launch()
