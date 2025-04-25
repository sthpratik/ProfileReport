from smolagents import LiteLLMModel, CodeAgent


model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:7b", # This model is a bit weak for agentic behaviours though
    api_base="http://localhost:11434", # replace with 127.0.0.1:11434 or remote open-ai compatible server if necessary
    api_key="YOUR_API_KEY", # replace with API key if necessary
    temperature=0.2,
    num_ctx=8192, # ollama default is 2048 which will fail horribly. 8192 works for easy tasks, more is better. Check https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator to calculate how much VRAM this will need for the selected model.
)


agent = CodeAgent(
            tools=[], model=model, add_base_tools=True,
            #tools=[calculate_transport_cost, calculate_tariff],
            max_steps=10,
            additional_authorized_imports=['itertools', 'queue', 'time', 'datetime',
            'random', 'stat', 'unicodedata', 'collections', 
            'math', 're', 'statistics', 'json', 'pickle', 
            'pandas', 'numpy', 'matplotlib', 
            'seaborn','matplotlib.pyplot'],
            verbosity_level=2,
                  )

agent.run(
    "From the data on diabetes_dataset.csv. Answer me how many male and female whose alcohol consumption is heavy has  bmi > 25? ",
)


