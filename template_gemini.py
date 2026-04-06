import os
import time
from typing import Any, Callable
from dotenv import load_dotenv

# Import thư viện chính chủ mới nhất của Google
from google import genai
from google.genai import types

# Tải biến môi trường từ file .env
load_dotenv()

# ---------------------------------------------------------------------------
# Cấu hình Gemini
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Khởi tạo client Google GenAI
client = genai.Client(api_key=GEMINI_API_KEY)

# Chi phí ước tính cho Gemini 1.5 (USD per 1K output tokens)
COST_PER_1K_OUTPUT_TOKENS = {
    "gemini-2.5-flash": 0.00125,   # $1.25 per 1M
    "gemini-2.5-flash-lite": 0.0003,  # $0.30 per 1M
}

OPENAI_MODEL = "gemini-2.5-flash"
OPENAI_MINI_MODEL = "gemini-2.5-flash-lite"


# ---------------------------------------------------------------------------
# Task 1 — Call Gemini (Pro)
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """Mặc dù tên hàm là call_openai để pass bài tập, nhưng bên trong gọi Gemini"""
    start_time = time.time()
    
    # Cấu hình tham số cho Gemini
    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
    )
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config
    )
    
    latency = time.time() - start_time
    return response.text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call Gemini (Flash)
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    return call_openai(
        prompt, 
        model=OPENAI_MINI_MODEL, 
        temperature=temperature, 
        top_p=top_p, 
        max_tokens=max_tokens
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare Pro vs Flash
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    res4o, lat4o = call_openai(prompt)
    res_mini, lat_mini = call_openai_mini(prompt)
    
    # Ước tính chi phí: (số từ / 0.75) = số tokens xấp xỉ
    tokens_est = len(res4o.split()) / 0.75
    cost_est = (tokens_est / 1000) * COST_PER_1K_OUTPUT_TOKENS[OPENAI_MODEL]
    
    return {
        "gpt4o_response": res4o,
        "mini_response": res_mini,
        "gpt4o_latency": lat4o,
        "mini_latency": lat_mini,
        "gpt4o_cost_estimate": cost_est
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    history = []
    print("AI: Hello! How can I help you today? (type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        # Gemini sử dụng role là 'user' và 'model' (thay vì 'assistant')
        history.append({"role": "user", "parts": [{"text": user_input}]})
        
        # Giữ lại 3 lượt hội thoại cuối (3 lượt x 2 role = 6 messages)
        context = history[-6:]
        
        try:
            stream = client.models.generate_content_stream(
                model=OPENAI_MINI_MODEL,
                contents=context
            )
            
            print("AI: ", end="", flush=True)
            full_reply = ""
            for chunk in stream:
                if chunk.text: # Kiểm tra tránh chunk bị rỗng
                    print(chunk.text, end="", flush=True)
                    full_reply += chunk.text
            print()
            
            history.append({"role": "model", "parts": [{"text": full_reply}]})
        except Exception as e:
            print(f"\n[Lỗi Gọi API]: {e}")


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            print(f"Error occurred. Retrying in {delay:.2f}s...")
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    results = []
    for p in prompts:
        res = compare_models(p)
        res["prompt"] = p
        results.append(res)
    return results



# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    # Bắt buộc phải có đúng các chữ "Prompt", "GPT-4o", và "Mini" ở Header
    table = f"{'Prompt':<30} | {'GPT-4o Response':<40} | {'Mini Response':<40} | {'Lat 4o':<8} | {'Lat Mini':<8}\n"
    table += "-" * 135 + "\n"
    
    for r in results:
        # Cắt chuỗi nếu quá dài để bảng không bị vỡ
        p = (r['prompt'][:27] + "..") if len(r['prompt']) > 27 else r['prompt']
        r_p = (r['gpt4o_response'][:37].replace('\n', ' ') + "..") if len(r['gpt4o_response']) > 37 else r['gpt4o_response']
        r_f = (r['mini_response'][:37].replace('\n', ' ') + "..") if len(r['mini_response']) > 37 else r['mini_response']
        
        # Format các cột tương ứng
        table += f"{p:<30} | {r_p:<40} | {r_f:<40} | {r['gpt4o_latency']:<8.2f} | {r['mini_latency']:<8.2f}\n"
        
    return table


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment.")
    else:
        test_prompt = "Explain the difference between temperature and top_p in one sentence."
        print("=== Comparing models ===")
        result = compare_models(test_prompt)
        for key, value in result.items():
            if "response" in key:
                print(f"{key}: {value[:100]}...")
            else:
                print(f"{key}: {value}")

        print("\n=== Starting chatbot ===")
        streaming_chatbot()