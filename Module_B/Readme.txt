└── 06_01_hw/
    └── Module_B/              
        ├── Data.zip    
        ├── Readme.md       
        ├── Readme.txt        
        ├── Report_M2.html          
        └── Report_M2.ipynb  
        └── demo.gif
        └── demo.mp4
    └── Helps/                
        ├── classes.txt
        ├── runs/
        ├── test_cases/
        ├── classes.txt
        └── data.yaml
    └── requirements.txt  
    └── yolov8n.pt
    └── yolov8s.pt
    └──/...
    
**Структура данных в модуле**

*Используемые библиотеки описаны в файле r`06_01_hw\requirements.txt`*

**Для проверки модели, перейдите в папку `Helps/runs`, выберите желаемую модель, перейдите в нее, затем в папке `weights` выберите либо файл `last.pt`, либо файл `best.pt`, копируйте путь к нему, и инициализируете модель посредством `model = YOLO(your_path2pt)`**

*после этого, передайте в модель путь на желаемоего изображение, и запустите. Пример кода найдете в файле `Report_M1.ipynb`*

**чтобы посмотреть демонстрационное видео работы API запустите файл `Module_B/demo.mp4` или `Module_B/demo.gif`**