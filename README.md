# Мультиагентная система

Платформа для создания и управления специализированными AI-агентами, способными решать конкретные задачи в различных областях.

## 🚀 Возможности

- **Модульная архитектура** - легко добавлять новые типы агентов
- **Специализированные агенты** - каждый агент решает конкретную задачу
- **Конфигурируемость** - гибкая настройка поведения агентов
- **Интеграция с LLM** - поддержка различных языковых моделей
- **Полное тестирование** - 100% покрытие кода тестами

## 📋 Поддерживаемые агенты

| Агент | Назначение | Возможности |
|-------|------------|-------------|
| **ConfluenceJiraAnalystAgent** | Анализ данных Confluence и JIRA | Извлечение метрик, генерация инсайтов, анализ трендов |
| **CodeGenerationAgent** | Генерация и валидация Python кода | Создание функций, валидация синтаксиса, генерация тестов |
| **IdeaEvaluationAgent** | Оценка бизнес-идей | Анализ осуществимости, оценка рисков, генерация рекомендаций |
| **ProjectManagementAgent** | Анализ здоровья проектов | Оценка рисков, генерация рекомендаций, анализ команды |

## 🏗️ Архитектура

```
agents/
├── src/
│   ├── agents/
│   │   ├── base_agent.py              # Базовый класс агента
│   │   ├── task_specific_agents.py    # Специализированные агенты
│   │   ├── extended_agents.py         # Расширенные агенты
│   │   └── specialized_agents.py      # Специализированные агенты
│   ├── config/
│   │   ├── agent_roles.yaml           # Роли агентов
│   │   ├── agents_config.yaml         # Конфигурация агентов
│   │   └── interactions.yaml          # Конфигурация взаимодействий
│   ├── prompts/
│   │   └── prompt_templates.py        # Шаблоны промптов
│   ├── utils/
│   │   ├── config_loader.py           # Загрузчик конфигурации
│   │   └── advanced_config_loader.py  # Расширенный загрузчик
│   └── workflow/
│       ├── multi_agent_workflow.py    # Мультиагентный рабочий процесс
│       ├── agent_router.py            # Маршрутизатор агентов
│       └── langgraph_integration.py   # Интеграция с LangGraph
├── config/
│   └── templates/                     # Шаблоны конфигураций
├── examples/                          # Примеры использования
├── tests/                            # Тесты
│   ├── unit/                         # Модульные тесты
│   ├── integration/                   # Интеграционные тесты
│   └── fixtures/                      # Фикстуры для тестов
├── docs/                             # Документация
└── logs/                             # Логи
```

## ⚡ Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd agents

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp env.example .env
# Отредактируйте .env файл с вашими API ключами
```

### Базовое использование

```python
import asyncio
from src.agents.task_specific_agents import TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

async def main():
    # Создание конфигурации агента
    config = AgentConfig(
        name="Data Analyst",
        role="Data Analysis Specialist",
        description="Анализирует данные проекта",
        model={
            "provider": "openai",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        },
        system_prompt="Ты эксперт по анализу данных...",
        capabilities=["data_analysis", "insights_generation"]
    )
    
    # Создание агента через фабрику
    factory = TaskSpecificAgentFactory()
    agent = factory.create_agent("confluence_jira_analyst", config, api_key)
    
    # Использование агента
    result = await agent.process({
        "confluence_pages": [{"title": "Test", "content": "Test content"}],
        "analysis_type": "trend_analysis"
    })
    
    print(f"Результат анализа: {result}")

# Запуск
asyncio.run(main())
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
python -m pytest tests/ -v

# Модульные тесты
python -m pytest tests/unit/ -v

# Интеграционные тесты
python -m pytest tests/integration/ -v

# С покрытием
python -m pytest tests/ --cov=src --cov-report=html
```

### Результаты тестирования

**Всего тестов: 26**
**Пройдено: 26**
**Провалено: 0**

- ✅ ConfluenceJiraAnalystAgent (5 тестов)
- ✅ CodeGenerationAgent (5 тестов)
- ✅ IdeaEvaluationAgent (5 тестов)
- ✅ ProjectManagementAgent (2 теста)
- ✅ TaskSpecificAgentFactory (6 тестов)
- ✅ Интеграционные тесты (3 теста)

## ⚙️ Конфигурация

### Структура конфигурации агента

```yaml
# config/agents_config.yaml
agents:
  confluence_jira_analyst:
    name: "Confluence/JIRA Analyst"
    role: "Data Analysis Specialist"
    description: "Анализирует данные из Confluence и JIRA"
    model:
      provider: "openai"
      model_name: "gpt-3.5-turbo"
      temperature: 0.7
      max_tokens: 4000
    system_prompt: "Ты эксперт по анализу данных из Confluence и JIRA..."
    capabilities:
      - "confluence_analysis"
      - "jira_metrics"
      - "insights_generation"
    limitations:
      - "Требует доступ к API Confluence/JIRA"
      - "Ограничен анализом текстовых данных"
```

### Переменные окружения

```bash
# .env
# API ключи для LLM провайдеров
OPENAI_API_KEY=your_openai_api_key_here

# Альтернативные переменные
LLM_API_KEY=your_llm_api_key_here

# Настройки логирования
LOG_LEVEL=INFO
LOG_FILE=logs/multiagent.log

# Настройки системы
MAX_ITERATIONS=5
TIMEOUT=300 
```

## 📚 Примеры использования

### Анализ данных Confluence/JIRA

```python
# Создание агента для анализа данных
agent = factory.create_agent("confluence_jira_analyst", config, api_key)

# Анализ данных
result = await agent.process({
    "confluence_pages": [{"title": "Project Overview", "content": "Project content"}],
    "jira_issues": [{"key": "PROJ-101", "status": "In Progress", "priority": "High"}],
    "analysis_type": "comprehensive"
})

# Извлечение метрик
jira_metrics = agent.extract_jira_metrics({"issues": jira_data})
confluence_insights = agent.extract_confluence_insights({"pages": confluence_data})
```

### Генерация и валидация кода

```python
# Создание агента для генерации кода
agent = factory.create_agent("code_generator", config, api_key)

# Генерация кода
result = await agent.process({
    "task_description": "Generate a function to calculate factorial",
    "code_type": "function",
    "requirements": ["recursive", "input validation"]
})

# Валидация кода
validation = agent.validate_python_code(result)
test_code = agent.generate_test_code(result)
```

### Оценка бизнес-идей

```python
# Создание агента для оценки идей
agent = factory.create_agent("idea_evaluator", config, api_key)

# Оценка идеи
evaluation = agent.evaluate_idea({
    "title": "AI-Powered Code Review Assistant",
    "description": "An AI tool that automatically reviews code changes",
    "category": "Development Tools",
    "target_audience": "Software Developers",
    "estimated_effort": "6 months",
    "budget_required": "$50,000"
})

# Фильтрация идей
filtered_ideas = agent.filter_ideas(ideas, {
    "max_budget": 100000,
    "max_effort_months": 12,
    "min_feasibility_score": 7.0
})
```

### Анализ здоровья проекта

```python
# Создание агента для анализа проекта
agent = factory.create_agent("project_manager", config, api_key)

# Анализ здоровья проекта
health_result = agent.analyze_project_health({
    "tasks": [{"status": "completed", "priority": "high"}],
    "team_members": ["dev1", "dev2", "dev3"],
    "timeline": {"start": "2024-01-01", "end": "2024-06-01"},
    "budget": {"planned": 100000, "spent": 75000},
    "quality_metrics": {"defect_rate": 0.03},
    "team_metrics": {"satisfaction": 0.8, "productivity": 0.85}
})
```

## 🔧 API Reference

### TaskSpecificAgentFactory

```python
@staticmethod
def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent

@staticmethod
def get_available_agent_types() -> List[str]
```

**Поддерживаемые типы**:
- `confluence_jira_analyst` - ConfluenceJiraAnalystAgent
- `code_generator` - CodeGenerationAgent
- `idea_evaluator` - IdeaEvaluationAgent
- `project_manager` - ProjectManagementAgent

### BaseAgent

```python
async def process(self, input_data: Any) -> str
async def _generate_response(self, input_text: str, template_vars: Dict[str, Any] = None) -> str
def get_capabilities(self) -> List[str]
def get_limitations(self) -> List[str]
def reset_state(self) -> None
```

### Специализированные методы

#### ConfluenceJiraAnalystAgent
```python
def extract_jira_metrics(self, jira_data: Dict[str, Any]) -> Dict[str, Any]
def extract_confluence_insights(self, confluence_data: Dict[str, Any]) -> Dict[str, Any]
```

#### CodeGenerationAgent
```python
def validate_python_code(self, code: str) -> Dict[str, Any]
def generate_test_code(self, main_code: str) -> str
```

#### IdeaEvaluationAgent
```python
def evaluate_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]
def filter_ideas(self, ideas: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]
```

#### ProjectManagementAgent
```python
def analyze_project_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]
```

## 📖 Документация

- [API Reference](docs/API_REFERENCE.md) - Справочник по API
- [Архитектура](docs/ARCHITECTURE.md) - Архитектура системы
- [Конфигурация](docs/CONFIGURATION.md) - Настройка и конфигурация
- [Примеры использования](docs/EXAMPLES.md) - Практические примеры
- [Тестирование](docs/TESTING.md) - Информация о тестировании
- [Развертывание](docs/DEPLOYMENT.md) - Руководство по развертыванию
- [Устранение неполадок](docs/TROUBLESHOOTING.md) - Решение проблем
- [Разработка](docs/DEVELOPMENT.md) - Разработка и расширение
- [Производительность](docs/PERFORMANCE.md) - Оптимизация и мониторинг

## 🚀 Развертывание

### Установка зависимостей

```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov pytest-xdist
```

### Настройка окружения

```bash
cp env.example .env
# Отредактируйте .env файл
```

### Запуск

```bash
# Основное приложение
python main.py

# Тесты
python -m pytest tests/ -v

# С мониторингом
python main.py --monitoring
```

### Мониторинг

```bash
# Просмотр логов
tail -f logs/multiagent.log
tail -f logs/errors.log
tail -f logs/interactions.jsonl
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

Если у вас есть вопросы или проблемы, создайте issue в репозитории.

---

**Мультиагентная система** - мощная платформа для создания специализированных AI-агентов с полным покрытием тестами и comprehensive документацией. 
