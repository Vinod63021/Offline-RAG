def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:8b",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("Response Text:")
        print(response.text)
        response.raise_for_status()

    return response.json()["response"]