import json


ages = []
for i in range(1, 121):
    age_data = {
        "model": "RecipeHub.Age",  #
        "pk": i,
        "fields": {
            "years": i
        }
    }
    ages.append(age_data)


with open('years.json', 'w', encoding='utf-8') as f:
    json.dump(ages, f, ensure_ascii=False, indent=4)
