# Импортирование библиотек
# библиотека для API
import streamlit as st

# библиотеки для работы с картинками
import cv2
from PIL import Image

# библиотеки для моделей
from ultralytics import YOLO
import easyocr

# библиотека с регулярными выражениями
from re import search

#-----------------------------------------------------------------
# Инициализация дефолтных аргументов функции
# модель детекции
model = YOLO(r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Helps\runs\detect\price_detection_v3\weights\best.pt')

# модель распознавания
ocr = easyocr.Reader(['en', 'ru'])

# тестовое фото
img = r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\data\test\images\original_five_46_v3_jpg.rf.c7116ee8d61a05af245a81865ddb3fef.jpg'

#-----------------------------------------------------------------
# Функции
# функция рисования креста на не отработанной картинке
def draw_cross(image):
    '''
    Рисует крест на изображении.
    
    Args:
        - image: Изображение в формате numpy array.
    
    Returns:
        Изображение с нарисованным крестом.
    '''

    height, width = image.shape[:2]
    color = (255,0,0) # красный цвет креста
    thickness = 50 # толщина линий креста

    # рисуем крест
    cv2.line(image, (0,0), (width,height), color, thickness)
    cv2.line(image, (width, 0), (0, height), color, thickness)

    return image

def rec_price(det_model: YOLO = model, 
              ocr: easyocr.Reader = ocr, 
              img_dir: str = img):
    
    '''
        Процедура для обнаружения и распознавания цен на изображении.

    Args:
        - det_model (YOLO): Модель YOLO для обнаружения bounding box'ов цен.
        - ocr (easyocr.Reader): Модель OCR для распознавания текста.
        - img_dir (str): Путь к изображению, на котором нужно найти цену.

    Returns:
        list: Функция отображает изображение с обнаруженными ценами и возвращает список с определенными ценами
    '''    
    # проверки на правильный тип данных в модели
    if not isinstance(det_model,YOLO):                                   
        raise TypeError('det_model должена быть объектом YOLO')

    if not isinstance(ocr, easyocr.Reader):
        raise TypeError('ocr должена быть объектом easyocr.Reader')

    if not isinstance(img_dir,str):
        raise TypeError('img_dir должен быть путем к фотографии типа str')

    # загружаем фотографии для модели детекции
    image = cv2.imread(img_dir)
    res = det_model(image)
    
    # а также создаем отдельное черно-белое контрастное фото, для более точного распознавания цены OCR моделью
    image_ocr = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)


    # список, куда будут сохраняться цены с изображения
    prices = []

    # проходимся по результатами модели
    for result in res:
        boxes = result.boxes.xyxy.cpu().numpy()
        for box in boxes:
            # находим x и y боксов, которые определила модель детекции
            x1, y1, x2, y2 = map(int, box)

            # корректируем x2 для более точного определения цены (не захватывая копейки)
            correct = (x2-x1)*0.28
            x2 = int(x2-correct)

            # обрезаем фотографию по найденным иксам
            crop = image_ocr[y1:y2, x1:x2]

            # читаем обрезанную фотографию OCR моделью
            ocr_res = ocr.readtext(crop, allowlist='0123456789')

            price = None 

            # выводим логи в виде цены и уверенности в ней
            for detection in ocr_res:
                price = detection[1]
                confidence = detection[2]

                match = search(r'\d+[\.,]?\d*', price)

                if match:
                    price = match.group()
                    print(f'Price: {price}\nConfidence: {confidence:.2f}')
                    break
            # для каждой детекции, рисуем bb's и сохраняем распознанную цену
            if price is not None:
                cv2.rectangle(image, (x1,y1), (x2+int(correct),y2), (255, 97, 0), 2)  # выделение изначального бокса
                cv2.rectangle(image, (x1,y1), (x2,y2), (97, 255, 0), 2)     # выделение инпута в ocr
                cv2.putText(image, price + 'rub', (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 97, 0), 2)
                prices.append(price)

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # если список с ценами остался пустым, значит применяем функцию с рисованием креста
    if not prices:
        img_rgb = draw_cross(img_rgb)

    # возвращаем rgb изображение и список с ценами
    return img_rgb, prices

#-----------------------------------------------------------------
# API
# тайтл к странице приложения
st.title('Распознавание цены товара с фотографии')

# кнопка для скачивания справки по приложению
with open(r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Module_A\Documentation2API.pdf', 'rb') as file:
    st.download_button(
        label='Справка',
        data=file,
        file_name='Справка.pdf',
        mime='application/pdf'
    )

# форма для загрузки фотографии
uploaded_file = st.file_uploader('Chose a file:', type=['jpg', 'jpeg', 'png'])

# если файл загружен, то обрабатываем его нашими функциями
if uploaded_file is not None:
    # сохраняем загруженное изображение
    with open('temp_image.jpg', 'wb') as f:
        f.write(uploaded_file.getbuffer())

    img_rgb, prices = rec_price(img_dir='temp_image.jpg')

    # выводим изображение с найденными (или не найденными) ценниками
    st.image(img_rgb,
             caption='Обнаруженные ценники',
             use_container_width=True
             )
    # если есть цены, то выводим их
    if prices:
        st.write('Найденные цены: ')
        for price in prices:
            st.write(f'- {price} руб.')
            
    # если цен нет, то выводим это
    else:
        st.write('Ценники не найдены')
