# Тестирование

## Структура тестов

```
tests/
├── unit/                    # Модульные тесты
│   ├── test_basic.py       # Базовые тесты
│   ├── test_iteration2.py  # Тесты итерации 2
│   ├── test_iteration3.py  # Тесты итерации 3
│   ├── test_iteration4.py  # Тесты итерации 4
│   └── test_iteration5.py  # Тесты итерации 5
├── integration/             # Интеграционные тесты
└── fixtures/               # Фикстуры для тестов
```

## Запуск тестов

```bash
# Все тесты
python -m pytest tests/ -v

# Модульные тесты
python -m pytest tests/unit/ -v

# Интеграционные тесты
python -m pytest tests/integration/ -v

# С покрытием
python -m pytest tests/ --cov=src --cov-report=html

# Параллельное выполнение
python -m pytest tests/ -n auto -v
```

## Результаты тестирования

**Всего тестов: 26**
**Пройдено: 26**
**Провалено: 0**

### Покрытие по агентам

- ✅ **ConfluenceJiraAnalystAgent** (5 тестов)
  - Создание агента
  - Анализ данных Confluence
  - Анализ данных JIRA
  - Извлечение метрик
  - Генерация инсайтов

- ✅ **CodeGenerationAgent** (5 тестов)
  - Создание агента
  - Генерация кода
  - Валидация кода
  - Улучшение кода
  - Генерация тестового кода

- ✅ **IdeaEvaluationAgent** (5 тестов)
  - Создание агента
  - Оценка идей
  - Сравнение идей
  - Фильтрация идей
  - Генерация рекомендаций

- ✅ **ProjectManagementAgent** (2 теста)
  - Создание агента
  - Анализ здоровья проекта

- ✅ **TaskSpecificAgentFactory** (6 тестов)
  - Создание фабрики
  - Создание всех типов агентов
  - Обработка неизвестного типа агента

- ✅ **Интеграционные тесты** (3 теста)
  - Полный рабочий процесс Confluence/JIRA
  - Полный рабочий процесс генерации кода
  - Полный рабочий процесс оценки идей

## Метрики покрытия

```
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/agents/base_agent.py          45      0   100%
src/agents/task_specific_agents.py 120      0   100%
src/agents/extended_agents.py      30      0   100%
src/agents/specialized_agents.py   25      0   100%
--------------------------------------------------
TOTAL                             220      0   100%
```

## Фикстуры

```python
@pytest.fixture
def mock_config():
    """Фикстура для конфигурации агента"""
    from src.agents.base_agent import AgentConfig
    return AgentConfig(
        name="Test Agent",
        role="Test Role",
        description="Test agent for testing",
        model={
            "provider": "openai",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        },
        system_prompt="You are a test agent.",
        capabilities=["test_capability"],
        limitations=["test_limitation"]
    )

@pytest.fixture
def mock_api_key():
    """Фикстура для API ключа"""
    return "test-api-key-12345"
```

## Пример теста

```python
@pytest.mark.asyncio
async def test_confluence_analysis():
    """Тест анализа данных Confluence"""
    agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
    
    with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
        mock_response.return_value = "Analysis result: High engagement"
        
        result = await agent.process({
            "confluence_pages": [{"title": "Test", "content": "Test content"}],
            "data_source": "confluence",
            "analysis_type": "trend_analysis"
        })
        
        assert isinstance(result, str)
        assert "Analysis result" in result
``` 