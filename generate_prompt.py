import itertools
import random
import json
from typing import List, Dict, Tuple

genders = ["мужской", "женский"]
height_weight = {
    "мужской": {"рост": list(range(160, 201, 5)), "вес": list(range(55, 121, 5))},
    "женский": {"рост": list(range(150, 186, 5)), "вес": list(range(45, 101, 5))}
}

goals = ["похудение", "набор массы", "поддержание веса", "здоровое питание"]

meals = ["3", "3 + 1 перекус", "3 + 2 перекуса", "5", "6"]

dietary_restrictions = [
    "безглютеновая диета", "безлактозная диета", "вегетарианство", "низкоуглеводная диета",
    "гипоаллергенная диета", "щадящая диета при гастрите", "нет ограничений"
]

allergy_list = [
    "аллергия на орехи", "аллергия на арахис", "аллергия на молочные продукты", "аллергия на яйца",
    "аллергия на рыбу", "аллергия на морепродукты", "аллергия на сою", "аллергия на глютен",
    "аллергия на горчицу", "аллергия на сельдерей", "аллергия на люпин", "аллергия на кунжут",
    "аллергия на сульфиты", "аллергия на клубнику", "аллергия на мёд", "аллергия на цитрусовые",
    "аллергия на томаты", "аллергия на бобовые"
]

time_limits = [
    {"завтрак": 10, "обед": 20, "ужин": 15},
    {"завтрак": 15, "обед": 30, "ужин": 20},
    {"завтрак": 30, "обед": 60, "ужин": 45},
    {"завтрак": 60, "обед": 60, "ужин": 60},
]

budgets = [500, 750, 1000, 1500, 2000, 3000, 5000]

prompt_template = """Составь рацион питания на 1 день с учетом следующих параметров:

- Пол: {gender}
- Рост: {height} см
- Вес: {weight} кг
- Цель питания: {goal}
- Количество приемов пищи: {meals}
- Диетические ограничения: {restriction}
- Аллергии: {allergy}
- Максимальное время на приготовление каждого приема пищи:
  – Завтрак: до {breakfast} минут
  – Обед: до {lunch} минут
  – Ужин: до {dinner} минут
- Бюджет на весь рацион: до {budget} рублей

Ответ дай строго в следующем текстовом шаблоне без дополнительного текста:

Прием пищи: [название приема пищи]
Название блюда: [название]
Ингредиенты: [ингредиент] – [граммы], ...
Калорийность: [число] ккал
БЖУ: белки [число] г, жиры [число] г, углеводы [число] г
Стоимость: [число] руб
Время приготовления: [число] мин
[повторяется для каждого приема пищи]

Итого за день:
- Общая калорийность: [число] ккал
- Общая стоимость: [число] руб
- Общее время приготовления: [число] мин
"""


def sample_allergies() -> str:
    probs = [0.7, 0.2, 0.08, 0.02]
    k = random.choices([0, 1, 2, 3], weights=probs)[0]
    if k == 0:
        return "нет аллергий"
    return ", ".join(random.sample(allergy_list, k))


def generate_combinations() -> List[Tuple]:
    return [
        (gender, height, weight, goal, meal, restriction,
         time["завтрак"], time["обед"], time["ужин"], budget)
        for gender in genders
        for height in height_weight[gender]["рост"]
        for weight in height_weight[gender]["вес"]
        for goal, meal, restriction, time, budget in itertools.product(
            goals, meals, dietary_restrictions, time_limits, budgets
        )
    ]


def render_prompt(comb: Tuple) -> str:
    return prompt_template.format(
        gender=comb[0], height=comb[1], weight=comb[2], goal=comb[3],
        meals=comb[4], restriction=comb[5], allergy=sample_allergies(),
        breakfast=comb[6], lunch=comb[7], dinner=comb[8], budget=comb[9]
    ).strip()


def save_prompts(prompts: List[Dict[str, str]], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)


def generate_prompts(output_file: str = "diet_prompts.json") -> None:
    all_combinations = generate_combinations()
    max_comb = len(all_combinations)
    print(f"Максимальное число комбинаций: {max_comb}")

    try:
        n = int(input(f"Введите количество промптов (максимум {max_comb}): "))
        if n <= 0:
            print("Число должно быть больше нуля.")
            return
    except ValueError:
        print("Ошибка: введите целое число.")
        return

    selected = all_combinations if n >= max_comb else random.sample(all_combinations, n)
    prompts = [{"prompt": render_prompt(c), "answer": ""} for c in selected]

    for p in prompts:
        print(f"\n{p['prompt']}\n")

    save_prompts(prompts, output_file)
    print(f"Сохранено {len(prompts)} промптов в файл: {output_file}")


if __name__ == "__main__":
    generate_prompts()
