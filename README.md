---

# Определение цены на ценниках

Этот репозиторий представляет собой решение задачи автоматического распознавания и определения цены на ценниках с использованием методов компьютерного зрения и машинного обучения. Задача разделена на три модуля: А, Б и В.

---

## **Структура проекта**

### **Модуль А: Разработка модели машинного обучения**
- **Цель**: Найти и локализовать ценники на изображении, и распознать на них цену продукта
- **Методы**:
  - Использование предобученных моделей для детекции объектов (например, YOLO).
- **Входные данные**: Изображение с ценниками, разметка для этих изображений
- **Выходные данные**: Координаты bounding box'ов для каждого обнаруженного ценника, распознанная цена.

---

### **Модуль Б: Тестирование разработанной модели**
- **Цель**: Потестировать работу алгоритма на 7 тест-кейсах.
- **Методы**:
  - Использование алгоритма разработанного в прошлом модуле, для тестирование его в новых ситуациях.
- **Входные данные**: 7 различных тест кейсов.
- **Выходные данные**: Координаты bounding box'ов для каждого обнаруженного ценника, распознанная цена.

---

### **Модуль В: Презентация решения**
- **Цель**: Подготовить презентацию для защиты своего решения.
- **Методы**:
  - Используя веб версию PowerPoint сделать презентацию.
- **Входные данные**: Отчеты по прошлым модулям.
- **Выходные данные**: Презентация в формате .pptx.

---

## **Установка и запуск**

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/Rainfue/06_01_hw.git
   ```

2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Пример использования**

1. Загрузите изображение с ценниками.
2. Запустите Модуль А или Б для обнаружения ценников, в качестве документации просмотрите `Readme` файлы в модулях.

*Видео демонастрация:*

![гифка](https://github.com/Rainfue/06_01_hw/blob/main/Module_B/demo.gif?raw=true)

---

## **Требования**
- Python 3.8+
- Установленные библиотеки: `opencv-python`, `easyocr`, `matplotlib`, `ultralytics` и другие (см. `requirements.txt`).

---

## **Автор**
- Зотеев А.А.
- alzotey@mail.ru
- [телеграмм](https://t.me/Wab_aqua_silente_caveW)

---

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь по контактам выше.

---
