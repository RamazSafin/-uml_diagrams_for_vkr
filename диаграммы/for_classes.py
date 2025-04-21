import os
from typing import List, Dict, Optional
import ast  # Для анализа кода (AST — Abstract Syntax Tree)

# 1. Класс для работы с локальной GPT-моделью
class LocalGPTService:
    def __init__(self, model_path: str = "tinyllama"):
        self.model_path = model_path  # Путь к локальной модели (Ollama/TinyLLama)
    
    def generate_code(self, prompt: str) -> str:
        """Генерация кода по описанию (заглушка — здесь будет вызов Ollama API)"""
        return f"# Сгенерированный код для: {prompt}\ndef example():\n    pass"
    
    def explain_code(self, code: str) -> str:
        """Объяснение кода через GPT"""
        return f"Этот код делает: {code[:50]}..."

# 2. Анализатор кода (для визуализации архитектуры)
class CodeAnalyzer:
    def parse_code(self, code: str) -> ast.AST:
        """Парсинг кода в AST (абстрактное синтаксическое дерево)"""
        return ast.parse(code)
    
    def extract_dependencies(self, code: str) -> Dict[str, List[str]]:
        """Поиск зависимостей между функциями/классами (упрощённо)"""
        tree = self.parse_code(code)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
        return {"imports": imports}

# 3. Визуализатор графа зависимостей 
class CodeVisualizer:
    def __init__(self, analyzer: CodeAnalyzer):
        self.analyzer = analyzer
    
    def generate_graph(self, code: str) -> str:
        """Генерация графа в формате DOT (для GraphViz)"""
        deps = self.analyzer.extract_dependencies(code)
        graph = "digraph G {\n"
        for imp in deps["imports"]:
            graph += f'  "{imp}" -> "current_file";\n'
        graph += "}"
        return graph

# 4. Главный контроллер расширения
class ExtensionController:
    def __init__(self):
        self.gpt = LocalGPTService()
        self.visualizer = CodeVisualizer(CodeAnalyzer())
    
    def on_generate_code(self, prompt: str) -> str:
        """Обработчик команды 'Сгенерировать код'"""
        return self.gpt.generate_code(prompt)
    
    def on_visualize_architecture(self, code: str) -> str:
        """Обработчик команды 'Показать архитектуру'"""
        return self.visualizer.generate_graph(code)

# Пример использования в VS Code
if __name__ == "__main__":
    controller = ExtensionController()
    
    # Пример 1: Генерация кода
    generated_code = controller.on_generate_code("Функция для сортировки списка")
    print("Сгенерированный код:\n", generated_code)
    
    # Пример 2: Визуализация архитектуры
    sample_code = """
    import os
    from typing import List
    def example():
        pass
    """
    graph = controller.on_visualize_architecture(sample_code)
    print("Граф зависимостей:\n", graph)