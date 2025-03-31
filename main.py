import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from g4f.client import Client
from tqdm import tqdm
import threading
from typing import Dict, List


client = Client()
lock = threading.Lock()


def get_response(prompt: str) -> str:
    """Получает ответ от модели gpt-4o по заданному промпту."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )
    return response.choices[0].message.content.strip()


def process_prompt(item: Dict[str, str]) -> bool:
    """Обрабатывает один элемент: получает ответ и записывает его в словарь."""
    item['answer'] = get_response(item['prompt'])
    return True


def load_prompts(file_path: str) -> List[Dict[str, str]]:
    """Загружает список промптов из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_prompts(data: List[Dict[str, str]], file_path: str) -> None:
    """Сохраняет список словарей с ответами в JSON-файл."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_answers(input_file: str, output_file: str, max_workers: int = 10) -> None:
    """Генерирует ответы для промптов из входного файла и сохраняет результат."""
    data = load_prompts(input_file)
    total = len(data)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_prompt, item): item for item in data}
        for _ in tqdm(as_completed(futures), total=total, desc="Обработка промптов"):
            pass

    save_prompts(data, output_file)
    print(f"Обработано и сохранено {total} промптов в файл '{output_file}'")


if __name__ == "__main__":
    generate_answers("diet_prompts.json", "diet_prompts_with_answers.json", max_workers=10)
