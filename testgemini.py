import google.generativeai as genai

genai.configure(api_key="AIzaSyABrmXSZGw7uWZB6-xZJmtBUC7aVIf_7kE")
for model in genai.list_models():
    print(model.name)
