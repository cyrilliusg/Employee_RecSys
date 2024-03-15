## Структура проекта

Проект организован следующим образом:

```
Employee_RecSys/
│
├── data/
│   ├── raw/                         # Initial data
│   │   ├── catalogue.csv            # Source company's catalogue
│   │   └── training/                # Train data
│   │       ├── raw/                 # Raw data
│   │       └── processed/           # Preprocessed data
│   │           ├── stemmed_data/    # Stemmed data
│   │           └── ...              # Other methods
│   │
├── apps/                            # Dictionaries and their data
│   ├── dictionary_creator/          # Dict creating application
│   │   ├── source/                  # Initial app code
│   │   └── db/                      # App's database
│
└── interface/                       # Interface
    └──  source/                     # Initial interface code (PyQt6)
```