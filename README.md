# ladno-smazan

![kandinsky-download-1727581197737](assets/123.png)

 # :robot: AI Assistant for Advertising Agency Data Search 

### Команда AiRina представляет решение по разработке интеллектуального помощника для рекламных агентств


## :building_construction: Архитектра решения

Интеллектуальный чат-бот с веб-интерфейсом построен на RAG-pipeline, который включает в себя:
- Мультимодальный поиск: Colpali
- Инференс: V-LLM
- Генерацию ответа: Vikhr-2.5-VL-2b-Instruct

### :pencil2: Ввод пользователя и oбработка запроса

Происходит обработка данных

> [!Note] 
> Удалили фон документов,что увеличило точность поиска нужной информации на 5-10%. 

### :mag_right: Поиск запроса по ответам БЗ

Добавили ранжирование в поиск 

> [!Note]
> Для наибольшей релевантности добавили расширенный датасет реальных ответов,что увеличило точность поиска на 5%.

### :bookmark_tabs: Квантизация и дообучении LLM

LLM  не требует больших вычислительных ресурсов,что позволило нам увеличить скорость ответа и сэкономить ресурсы.


### :bulb: Дополнительная проверка на фантазии 

На основании целевых вопросов пользователей, генерируем ответ
> [!Note]
> Но если с фильтрации пришло 0 документов, модель сразу ответит "Я не знаю". Поэтому у модели нет возможности придумывать свои ответ. Ответы всегда будут основываться на БЗ
>

### :bricks: Композиция наглядно
![image_2024-09-29_09-33-29](https://github.com/user-attachments/assets/fffde057-0426-4375-b064-49e51a0ffde0)

 # :rocket: Запуск
Решение упаковано и будет готов к работе через **2 строки**

 **Для запуска нужны**
 - docker
 - docker-compose
 - make

**Запуск инференса LLM**
```
vllm serve --dtype half --max-model-len 16000 -tp 1 Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24 --api-key token-abc123
```
   
**Развертывание**
```
make up
```

 # :computer: Стек технологий
**БД**
- redis (хранилище связей аугментированных вопросов и вопрос из бз)
- chroma (векторное хранилище)

**Код**
- python
- langchain

# :checkered_flag: ## Основные проблемы и решения

## :exploding_head: ### Обработка исходного PDF документа

Одной из ключевых проблем в проекте стала работа с исходным PDF документом, который содержал большое количество изображений. На первых 20 страницах документа было уже 37 графических элементов (изображения, схемы, диаграммы и т.д.). 

## :hugs: ### Проблема интерпретации информации

Важная информация зачастую была представлена как комбинация текста и изображений. Например, числовые данные могли быть отображены на одной картинке, а их пояснения — на другой, либо вообще в текстовой части. Такая разрозненная структура усложняла задачу правильного объединения данных при их обработке и интерпретации.

Изначально я пробовала использовать библиотеку `unstructured` для обработки таких документов, но из-за сложности сопоставления текста и изображений это не дало удовлетворительных результатов. Более подробное описание экспериментов сохранены в ноутбуке с названием `multimodal-rag-unstructured.ipynb`.


## made with ♥️ by AiRina for 
![header-logo c7e8f395](assets/12345.png)



