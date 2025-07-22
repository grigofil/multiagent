# Архитектура системы

## Обзор архитектуры

Мультиагентная система построена на принципах модульности, расширяемости и конфигурируемости. Система использует паттерн Factory для создания агентов и поддерживает различные LLM провайдеры.

## Структура проекта

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

## Диаграмма архитектуры

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Конфигурация  │    │   Базовый агент │    │  Специализирован│
│                 │    │                 │    │  ные агенты     │
│ - agent_roles   │───▶│ - BaseAgent     │───▶│ - Confluence    │
│ - agents_config │    │ - AgentConfig   │    │ - CodeGen       │
│ - interactions  │    │ - AgentState    │    │ - IdeaEval      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Фабрика       │    │   Рабочий       │    │   Интеграция    │
│   агентов       │    │   процесс       │    │   с LangGraph   │
│                 │    │                 │    │                 │
│ - TaskSpecific  │    │ - MultiAgent    │    │ - LangGraph     │
│   AgentFactory  │    │   Workflow      │    │   Integration   │
│ - AgentRouter   │    │ - AgentRouter   │    │ - Checkpointer  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Основные компоненты

### 1. Базовый агент (BaseAgent)

Базовый класс для всех агентов в системе. Предоставляет общую функциональность для инициализации, работы с LLM и управления состоянием.

#### Ключевые особенности:
- Абстрактный базовый класс
- Интеграция с различными LLM провайдерами
- Управление состоянием агента
- Логирование и мониторинг

#### Структура:
```python
class BaseAgent(ABC):
    def __init__(self, config: AgentConfig, api_key: Optional[str] = None)
    async def process(self, input_data: Any) -> str
    async def _generate_response(self, input_text: str, template_vars: Dict[str, Any] = None) -> str
    def get_capabilities(self) -> List[str]
    def get_limitations(self) -> List[str]
    def reset_state(self) -> None
```

### 2. Специализированные агенты

#### ConfluenceJiraAnalystAgent
- **Назначение**: Анализ данных из Confluence и JIRA
- **Возможности**: Извлечение метрик, генерация инсайтов, анализ трендов
- **Методы**: `extract_jira_metrics()`, `extract_confluence_insights()`

#### CodeGenerationAgent
- **Назначение**: Генерация и валидация Python кода
- **Возможности**: Создание функций, валидация синтаксиса, генерация тестов
- **Методы**: `validate_python_code()`, `generate_test_code()`

#### IdeaEvaluationAgent
- **Назначение**: Оценка бизнес-идей
- **Возможности**: Анализ осуществимости, оценка рисков, генерация рекомендаций
- **Методы**: `evaluate_idea()`, `filter_ideas()`

#### ProjectManagementAgent
- **Назначение**: Анализ здоровья проектов
- **Возможности**: Оценка рисков, генерация рекомендаций, анализ команды
- **Методы**: `analyze_project_health()`, `_generate_project_recommendations()`

### 3. Фабрика агентов (TaskSpecificAgentFactory)

Паттерн Factory для создания специализированных агентов. Позволяет создавать агенты различных типов с единым интерфейсом.

#### Структура:
```python
class TaskSpecificAgentFactory:
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent
    @staticmethod
    def get_available_agent_types() -> List[str]
```

#### Поддерживаемые типы:
- `confluence_jira_analyst` - ConfluenceJiraAnalystAgent
- `code_generator` - CodeGenerationAgent
- `idea_evaluator` - IdeaEvaluationAgent
- `project_manager` - ProjectManagementAgent

### 4. Конфигурационная система

#### AgentConfig
Pydantic модель для конфигурации агентов:
```python
class AgentConfig(BaseModel):
    name: str
    role: str
    description: str
    model: Dict[str, Any]
    system_prompt: str
    prompt_template: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
```

#### Конфигурационные файлы
- `agents_config.yaml` - конфигурация агентов
- `agent_roles.yaml` - роли и возможности
- `interactions.yaml` - рабочие процессы

### 5. Система логирования и мониторинга

#### Логирование
- Структурированные логи в JSON формате
- Разделение по уровням (DEBUG, INFO, WARNING, ERROR)
- Ротация логов

#### Мониторинг
- Метрики производительности
- Отслеживание использования API
- Мониторинг состояния агентов

## Паттерны проектирования

### 1. Factory Pattern
Используется для создания агентов различных типов:
```python
agent = TaskSpecificAgentFactory.create_agent("confluence_jira_analyst", config, api_key)
```

### 2. Strategy Pattern
Различные стратегии обработки для разных типов агентов:
```python
async def process(self, input_data: Any) -> str:
    # Специфичная логика обработки для каждого агента
    pass
```

### 3. Template Method Pattern
Базовый класс определяет общую структуру, подклассы реализуют специфичную логику:
```python
class BaseAgent(ABC):
    async def process(self, input_data: Any) -> str:
        # Общая логика
        result = await self._process_specific(input_data)
        # Общая логика
        return result
    
    @abstractmethod
    async def _process_specific(self, input_data: Any) -> str:
        pass
```

### 4. Configuration Pattern
Использование внешних конфигураций для настройки поведения:
```python
config = AgentConfig(
    name="Agent Name",
    model={"provider": "openai", "model_name": "gpt-3.5-turbo"},
    system_prompt="System prompt"
)
```

## Интеграция с внешними системами

### 1. LLM провайдеры
- **OpenAI**: GPT-3.5-turbo, GPT-4
- **Anthropic**: Claude-3-sonnet
- **Google**: Gemini-pro

### 2. Системы мониторинга
- Prometheus метрики
- Grafana дашборды
- ELK стек для логов

### 3. Базы данных
- PostgreSQL для хранения состояния
- Redis для кэширования
- MongoDB для документов

## Масштабируемость

### 1. Горизонтальное масштабирование
- Статичные агенты без состояния
- Возможность запуска множества экземпляров
- Балансировка нагрузки

### 2. Вертикальное масштабирование
- Оптимизация производительности агентов
- Кэширование результатов
- Асинхронная обработка

### 3. Модульность
- Независимые компоненты
- Легкое добавление новых агентов
- Плагинная архитектура

## Безопасность

### 1. Управление API ключами
- Переменные окружения
- Шифрование чувствительных данных
- Ротация ключей

### 2. Валидация входных данных
- Pydantic модели
- Схемы валидации
- Санитизация данных

### 3. Логирование безопасности
- Аудит действий
- Мониторинг подозрительной активности
- Сохранение логов безопасности

## Производительность

### 1. Асинхронность
- asyncio для неблокирующих операций
- Параллельная обработка задач
- Эффективное использование ресурсов

### 2. Кэширование
- Redis для кэширования результатов
- TTL для автоматической очистки
- Стратегии кэширования

### 3. Оптимизация LLM вызовов
- Батчинг запросов
- Сжатие контекста
- Переиспользование соединений 