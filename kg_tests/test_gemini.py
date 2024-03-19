from kg_core.llm import get_model

def test_gemini_pro():
    model = get_model('gemini-pro')
    response = model.generate("Say this is a test")
    # print(response)
    print(model.unwrap_response(response))
    print(model.unwrap_usage(response))

def test_gemini_ultra():
    model = get_model('gemini-ultra')
    response = model.generate("Say this is a test")
    # print(response)
    print(model.unwrap_response(response))
    print(model.unwrap_usage(response))