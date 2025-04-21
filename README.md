 Расширение для VS Code


## 📷 Диаграммы проекта

### 📌 Диаграмма активностей (Activity Diagram)

> Отражает логику обработки пользовательского запроса, генерации кода и последующего анализа.

![Диаграмма активностей](diagrami/activity.jpg)

```plantuml
@startuml
title Генерация и проверка кода
start
:Пользователь вводит запрос;
if (Модель загружена?) then (Да)
else (Нет)
  :Загрузить локальную GPT-модель;
endif
:GPT генерирует код;

partition Анализ кода {
  :Парсинг кода в AST;
  if (Есть ошибки?) then (Да)
    :Запросить рефакторинг у GPT;
    :Парсинг кода повторно;
    if (Ошибки остались?) then (Да)
      :Сообщить об ошибке пользователю;
      stop
    endif
  endif
}

:Вывести результат в VS Code;
stop
@enduml
```
---

### 📌 Диаграмма последовательности (Sequence Diagram)

> Показывает взаимодействие между компонентами расширения при генерации кода.

![Диаграмма последовательности](diagrami/sequence.jpg)
```plantuml
@startuml
actor Программист as Dev
participant "VS Code" as VSCode
participant "ExtensionController" as Controller
participant "LocalGPTService" as GPT
participant "CodeAnalyzer" as Analyzer

== Генерация кода ==
Dev -> VSCode : Вводит запрос ("Напиши функцию сортировки")
VSCode -> Controller : onGenerateCode(запрос)
Controller -> GPT : generateCode(запрос)
GPT --> Controller : "def sort(arr):..."
Controller -> Analyzer : parseCode(код)
Analyzer --> Controller : AST (без ошибок)
Controller -> VSCode : Показать сгенерированный код
VSCode --> Dev : Отображает результат

== Визуализация проекта ==
Dev -> VSCode : Запрашивает визуализацию кода
VSCode -> Controller : onRequestCodeMap()
Controller -> Analyzer : analyzeProjectStructure()
Analyzer --> Controller : CodeMap (модули, зависимости, связи)
Controller -> VSCode : Показать карту проекта
VSCode --> Dev : Отображает визуализацию
@enduml

```
---

### 📌 Диаграмма состояний (State Diagram)

> Иллюстрирует переходы между состояниями расширения: ожидание, загрузка, обработка запроса, вывод результата и ошибки.

![Диаграмма состояний](diagrami/state.jpg)
```plantuml
@startuml
[*] --> Idle

Idle --> ModelLoading : Запуск расширения /\nмодель не загружена
ModelLoading --> Idle : ModelReady
ModelLoading --> Error : ErrorOccurred

Idle --> ProcessingRequest : UserRequest
ProcessingRequest --> ModelLoading : Нужна модель
ProcessingRequest --> CodeAnalysis : Нужен анализ кода
ProcessingRequest --> DisplayingResult : Результат готов

CodeAnalysis --> DisplayingResult : AnalysisComplete
DisplayingResult --> Idle : ResultShown

Error --> Idle : Повторная попытка
Error --> [*] : Критическая ошибка
@enduml
```
---

### 📌 Диаграмма классов (Class Diagram)

> Структура основных компонентов расширения и их связи.

![Диаграмма классов](diagrami/classes.jpg)
```plantuml
@startuml
class LocalGPTService {
  -modelPath: string
  +generateCode(prompt: string): string
  +explainCode(code: string): string
  +refactorCode(code: string): string
  +findBugs(code: string): string[]
}

class CodeVisualizer {
  -analyzer: CodeAnalyzer
  +generateDependencyGraph(): Graph
  +renderGraph(): void
}

class CodeAnalyzer {
  -ast: AST
  +parseCode(code: string): void
  +extractDependencies(): Dependency[]
}

class ExtensionController {
  -gpt: LocalGPTService
  -visualizer: CodeVisualizer
  +onGenerateCode(): void
  +onExplainCode(): void
  +onVisualizeArchitecture(): void
}

class "VS Code API" as VSCode {
  +getActiveText(): string
  +showInfoMessage(text: string): void
}

ExtensionController --> LocalGPTService
ExtensionController --> CodeVisualizer
CodeVisualizer --> CodeAnalyzer
ExtensionController --> VSCode
@enduml
```
---

### 📌 Диаграмма вариантов использования (Use Case Diagram)

> Общий обзор взаимодействия пользователя с расширением.

![Диаграмма use case](diagrami/use_case.jpg)
```plantuml
@startuml
left to right direction
actor "Программист" as Dev
actor "VS Code" as IDE

rectangle "Помощник программиста (локальный)" {
  usecase "1. Генерация кода (локально)" as UC1
  usecase "2. Объяснение кода (локально)" as UC2
  usecase "3. Рефакторинг кода (локально)" as UC3
  usecase "4. Поиск ошибок (локально)" as UC4
  usecase "5. Визуализация архитектуры" as UC5
  usecase "6. Ответы на вопросы (локально)" as UC6

  component "Локальная GPT-модель" as GPT {
    (LLM)
  }

  Dev --> UC1
  Dev --> UC2
  Dev --> UC3
  Dev --> UC4
  Dev --> UC5
  Dev --> UC6

  UC3 .> UC4 : extends
  UC1 .> (Подсказки по синтаксису) : includes

  UC1 -- GPT
  UC2 -- GPT
  UC3 -- GPT  
  UC4 -- GPT  
  UC6 -- GPT
  UC5 -- IDE
}
@enduml
```

---

