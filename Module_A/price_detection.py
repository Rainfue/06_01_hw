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
# Инициализация моделей
# модель детекции
model = YOLO(r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Helps\runs\detect\price_detection_v42\weights\best.pt')

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
    thickness = 100 # толщина линий креста

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

    image = cv2.imread(img_dir)
    res = det_model(image)
    
    image_ocr = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image_ocr, 100, 255, cv2.THRESH_BINARY)


    image_ocr = cv2.equalizeHist(binary_image)

    prices = []

    for result in res:
        boxes = result.boxes.xyxy.cpu().numpy()
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            correct = (x2-x1)*0.28
            print(correct)
            x2 = int(x2-correct)
            crop = image_ocr[y1:y2, x1:x2]

            # --------------------------------------------

            # plt.figure(figsize=(5, 5))
            # plt.imshow(crop, cmap='gray')
            # plt.title("Cropped Image")               # отображение обрезанной части картинки
            # plt.axis('off')
            # plt.show()

            # --------------------------------------------

            ocr_res = ocr.readtext(crop, allowlist='0123456789')

            price = None 

            for detection in ocr_res:
                price = detection[1]
                confidence = detection[2]

                match = search(r'\d+[\.,]?\d*', price)

                if match:
                    price = match.group()
                    print(f'Price: {price}\nConfidence: {confidence:.2f}')
                    break
            if price is not None:
                cv2.rectangle(image, (x1,y1), (x2+int(correct),y2), (255, 97, 0), 2)  # выделение изначального бокса
                cv2.rectangle(image, (x1,y1), (x2,y2), (97, 255, 0), 2)     # выделение инпута в ocr
                cv2.putText(image, price + 'rub', (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 97, 0), 2)
                prices.append(price)

    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    if not prices:
        img_rgb = draw_cross(img_rgb)

    return img_rgb, prices

#-----------------------------------------------------------------
# API
st.title('Распознавание цены товара с фотографии')

with open(r'D:\Helper\MLBazyak\homework\06_01\06_01_hw\Module_V\presentation.pdf', 'rb') as file:
    st.download_button(
        label='Справка',
        data=file,
        file_name='Справка.pdf',
        mime='application/pdf'
    )

uploaded_file = st.file_uploader('Chose a file:', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # сохраняем загруженное изображение
    with open('temp_image.jpg', 'wb') as f:
        f.write(uploaded_file.getbuffer())

    img_rgb, prices = rec_price(img_dir='temp_image.jpg')

    st.image(img_rgb,
             caption='Обнаруженные ценники',
             use_container_width=True
             )
    if prices:
        st.write('Найденные цены: ')
        for price in prices:
            st.write(f'- {price} руб.')
    else:
        st.write('Ценники не найден')
