# Разработка и расширение

## Создание нового агента

### 1. Структура нового агента

```python
# src/agents/custom_agent.py
from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentConfig

class CustomAgent(BaseAgent):
    """Пользовательский агент для специфических задач"""
    
    def __init__(self, config: AgentConfig, api_key: str = None):
        super().__init__(config, api_key)
        self.specialized_methods = []
    
    async def process(self, input_data: Any) -> str:
        """Основной метод обработки данных"""
        # Предобработка входных данных
        processed_input = self._preprocess_input(input_data)
        
        # Генерация ответа
        response = await self._generate_response(
            str(processed_input),
            {"input_type": type(input_data).__name__}
        )
        
        # Постобработка ответа
        final_response = self._postprocess_response(response)
        
        return final_response
    
    def _preprocess_input(self, input_data: Any) -> Dict[str, Any]:
        """Предобработка входных данных"""
        if isinstance(input_data, dict):
            return input_data
        elif isinstance(input_data, str):
            return {"text": input_data}
        else:
            return {"data": str(input_data)}
    
    def _postprocess_response(self, response: str) -> str:
        """Постобработка ответа"""
        # Добавление метаданных
        return f"CustomAgent Response: {response}"
    
    def get_capabilities(self) -> List[str]:
        """Получение возможностей агента"""
        return self.config.capabilities + ["custom_processing"]
    
    def get_limitations(self) -> List[str]:
        """Получение ограничений агента"""
        return self.config.limitations + ["Limited to custom tasks"]
    
    # Специализированные методы
    def custom_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Специализированный метод агента"""
        # Реализация специфической логики
        return {"processed": True, "result": "custom_result"}
```

### 2. Регистрация агента в фабрике

```python
# Обновление TaskSpecificAgentFactory
class TaskSpecificAgentFactory:
    """Фабрика для создания специализированных агентов"""
    
    _agent_registry = {
        "confluence_jira_analyst": ConfluenceJiraAnalystAgent,
        "code_generator": CodeGenerationAgent,
        "idea_evaluator": IdeaEvaluationAgent,
        "project_manager": ProjectManagementAgent,
        "custom_agent": CustomAgent,  # Добавление нового агента
    }
    
    @classmethod
    def register_agent(cls, agent_type: str, agent_class: type):
        """Регистрация нового типа агента"""
        cls._agent_registry[agent_type] = agent_class
    
    @classmethod
    def get_available_agent_types(cls) -> List[str]:
        """Получение списка доступных типов агентов"""
        return list(cls._agent_registry.keys())
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent:
        """Создание агента указанного типа"""
        if agent_type not in TaskSpecificAgentFactory._agent_registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = TaskSpecificAgentFactory._agent_registry[agent_type]
        return agent_class(config, api_key)

# Регистрация нового агента
TaskSpecificAgentFactory.register_agent("custom_agent", CustomAgent)
```

### 3. Конфигурация нового агента

```yaml
# config/agents_config.yaml
agents:
  custom_agent:
    name: "Custom Agent"
    role: "Custom Task Specialist"
    description: "Специализированный агент для пользовательских задач"
    model:
      provider: "openai"
      model_name: "gpt-4"
      temperature: 0.5
      max_tokens: 2000
    system_prompt: |
      Ты специализированный агент для обработки пользовательских задач.
      Твоя роль - анализировать входные данные и предоставлять точные,
      структурированные ответы. Всегда следуй указанным инструкциям
      и формату ответа.
    capabilities:
      - "custom_processing"
      - "data_analysis"
      - "structured_output"
    limitations:
      - "Ограничен пользовательскими задачами"
      - "Требует специфической конфигурации"
```

## Создание новых промптов

### 1. Шаблоны промптов

```python
# src/prompts/custom_prompts.py
from typing import Dict, Any

class CustomPromptTemplates:
    """Шаблоны промптов для пользовательских агентов"""
    
    @staticmethod
    def analysis_prompt(data: Dict[str, Any]) -> str:
        """Промпт для анализа данных"""
        return f"""
        Проанализируй следующие данные:
        
        Тип данных: {data.get('type', 'unknown')}
        Размер данных: {len(str(data.get('content', '')))}
        
        Данные:
        {data.get('content', 'No content provided')}
        
        Предоставь структурированный анализ с:
        1. Основными выводами
        2. Ключевыми метриками
        3. Рекомендациями
        """
    
    @staticmethod
    def processing_prompt(input_data: str, requirements: Dict[str, Any]) -> str:
        """Промпт для обработки данных"""
        return f"""
        Обработай следующие данные согласно требованиям:
        
        Входные данные:
        {input_data}
        
        Требования:
        - Формат вывода: {requirements.get('output_format', 'text')}
        - Уровень детализации: {requirements.get('detail_level', 'medium')}
        - Специальные требования: {requirements.get('special_requirements', 'none')}
        
        Предоставь результат в указанном формате.
        """
    
    @staticmethod
    def validation_prompt(result: str, criteria: Dict[str, Any]) -> str:
        """Промпт для валидации результатов"""
        return f"""
        Проверь следующий результат на соответствие критериям:
        
        Результат:
        {result}
        
        Критерии проверки:
        - Точность: {criteria.get('accuracy', 'high')}
        - Полнота: {criteria.get('completeness', 'required')}
        - Формат: {criteria.get('format', 'standard')}
        
        Предоставь оценку и рекомендации по улучшению.
        """
```

### 2. Интеграция промптов

```python
# Обновление CustomAgent с промптами
class CustomAgent(BaseAgent):
    def __init__(self, config: AgentConfig, api_key: str = None):
        super().__init__(config, api_key)
        self.prompt_templates = CustomPromptTemplates()
    
    async def analyze_data(self, data: Dict[str, Any]) -> str:
        """Анализ данных с использованием специализированного промпта"""
        prompt = self.prompt_templates.analysis_prompt(data)
        return await self._generate_response(prompt)
    
    async def process_with_requirements(self, input_data: str, 
                                     requirements: Dict[str, Any]) -> str:
        """Обработка данных с требованиями"""
        prompt = self.prompt_templates.processing_prompt(input_data, requirements)
        return await self._generate_response(prompt)
    
    async def validate_result(self, result: str, criteria: Dict[str, Any]) -> str:
        """Валидация результата"""
        prompt = self.prompt_templates.validation_prompt(result, criteria)
        return await self._generate_response(prompt)
```

## Создание новых рабочих процессов

### 1. Мультиагентный рабочий процесс

```python
# src/workflow/custom_workflow.py
from typing import Dict, Any, List
import asyncio
from ..agents.base_agent import BaseAgent

class CustomWorkflow:
    """Пользовательский рабочий процесс"""
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        self.workflow_steps = []
        self.results = {}
    
    def add_step(self, step_name: str, agent_name: str, 
                input_mapping: Dict[str, str], output_key: str):
        """Добавление шага в рабочий процесс"""
        self.workflow_steps.append({
            'name': step_name,
            'agent': agent_name,
            'input_mapping': input_mapping,
            'output_key': output_key
        })
    
    async def execute(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение рабочего процесса"""
        current_data = initial_data.copy()
        
        for step in self.workflow_steps:
            # Подготовка входных данных для агента
            agent_input = self._prepare_agent_input(
                current_data, step['input_mapping']
            )
            
            # Выполнение шага
            agent = self.agents[step['agent']]
            result = await agent.process(agent_input)
            
            # Сохранение результата
            current_data[step['output_key']] = result
            self.results[step['name']] = result
            
            print(f"Step '{step['name']}' completed")
        
        return current_data
    
    def _prepare_agent_input(self, data: Dict[str, Any], 
                           mapping: Dict[str, str]) -> Dict[str, Any]:
        """Подготовка входных данных для агента"""
        agent_input = {}
        for agent_key, data_key in mapping.items():
            if data_key in data:
                agent_input[agent_key] = data[data_key]
        return agent_input
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Получение сводки рабочего процесса"""
        return {
            'total_steps': len(self.workflow_steps),
            'completed_steps': len(self.results),
            'step_names': [step['name'] for step in self.workflow_steps],
            'results': self.results
        }

# Пример использования
async def run_custom_workflow():
    """Запуск пользовательского рабочего процесса"""
    
    # Создание агентов
    factory = TaskSpecificAgentFactory()
    config = AgentConfig(...)  # Конфигурация
    
    agents = {
        'analyzer': factory.create_agent('custom_agent', config, api_key),
        'validator': factory.create_agent('code_generator', config, api_key),
        'evaluator': factory.create_agent('idea_evaluator', config, api_key)
    }
    
    # Создание рабочего процесса
    workflow = CustomWorkflow(agents)
    
    # Добавление шагов
    workflow.add_step(
        'data_analysis',
        'analyzer',
        {'data': 'input_data'},
        'analysis_result'
    )
    
    workflow.add_step(
        'validation',
        'validator',
        {'code': 'analysis_result'},
        'validation_result'
    )
    
    workflow.add_step(
        'evaluation',
        'evaluator',
        {'idea': 'validation_result'},
        'final_evaluation'
    )
    
    # Выполнение рабочего процесса
    initial_data = {'input_data': 'Sample data for analysis'}
    result = await workflow.execute(initial_data)
    
    return result
```

### 2. Условные рабочие процессы

```python
# src/workflow/conditional_workflow.py
from typing import Dict, Any, Callable
import asyncio

class ConditionalWorkflow:
    """Рабочий процесс с условной логикой"""
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        self.conditions = {}
        self.steps = []
    
    def add_conditional_step(self, step_name: str, condition: Callable,
                           true_agent: str, false_agent: str,
                           input_mapping: Dict[str, str], output_key: str):
        """Добавление условного шага"""
        self.steps.append({
            'name': step_name,
            'condition': condition,
            'true_agent': true_agent,
            'false_agent': false_agent,
            'input_mapping': input_mapping,
            'output_key': output_key
        })
    
    async def execute(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнение условного рабочего процесса"""
        current_data = initial_data.copy()
        
        for step in self.steps:
            # Проверка условия
            condition_result = step['condition'](current_data)
            
            # Выбор агента на основе условия
            agent_name = step['true_agent'] if condition_result else step['false_agent']
            agent = self.agents[agent_name]
            
            # Подготовка входных данных
            agent_input = self._prepare_agent_input(
                current_data, step['input_mapping']
            )
            
            # Выполнение шага
            result = await agent.process(agent_input)
            current_data[step['output_key']] = result
            
            print(f"Step '{step['name']}' completed with agent '{agent_name}'")
        
        return current_data
    
    def _prepare_agent_input(self, data: Dict[str, Any], 
                           mapping: Dict[str, str]) -> Dict[str, Any]:
        """Подготовка входных данных"""
        agent_input = {}
        for agent_key, data_key in mapping.items():
            if data_key in data:
                agent_input[agent_key] = data[data_key]
        return agent_input

# Примеры условий
def is_complex_data(data: Dict[str, Any]) -> bool:
    """Проверка сложности данных"""
    content = data.get('content', '')
    return len(content) > 1000

def requires_validation(data: Dict[str, Any]) -> bool:
    """Проверка необходимости валидации"""
    return data.get('validation_required', False)

def is_high_priority(data: Dict[str, Any]) -> bool:
    """Проверка приоритета"""
    return data.get('priority', 'low') == 'high'
```

## Тестирование новых компонентов

### 1. Тесты для нового агента

```python
# tests/unit/test_custom_agent.py
import pytest
from unittest.mock import AsyncMock, patch
from src.agents.custom_agent import CustomAgent
from src.agents.base_agent import AgentConfig

@pytest.fixture
def custom_agent_config():
    """Фикстура для конфигурации пользовательского агента"""
    return AgentConfig(
        name="Test Custom Agent",
        role="Test Role",
        description="Test custom agent",
        model={
            "provider": "openai",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        },
        system_prompt="You are a test custom agent.",
        capabilities=["custom_processing"],
        limitations=["test_limitation"]
    )

@pytest.fixture
def custom_agent(custom_agent_config):
    """Фикстура для пользовательского агента"""
    return CustomAgent(custom_agent_config, "test-api-key")

class TestCustomAgent:
    """Тесты для пользовательского агента"""
    
    @pytest.mark.asyncio
    async def test_custom_agent_creation(self, custom_agent):
        """Тест создания пользовательского агента"""
        assert custom_agent is not None
        assert isinstance(custom_agent, CustomAgent)
    
    @pytest.mark.asyncio
    async def test_custom_agent_process(self, custom_agent):
        """Тест обработки данных пользовательским агентом"""
        with patch.object(custom_agent, '_generate_response', 
                         new_callable=AsyncMock) as mock_response:
            mock_response.return_value = "Test response"
            
            result = await custom_agent.process({"test": "data"})
            
            assert isinstance(result, str)
            assert "CustomAgent Response" in result
            assert "Test response" in result
    
    @pytest.mark.asyncio
    async def test_custom_agent_analysis(self, custom_agent):
        """Тест анализа данных пользовательским агентом"""
        with patch.object(custom_agent, '_generate_response', 
                         new_callable=AsyncMock) as mock_response:
            mock_response.return_value = "Analysis result"
            
            result = await custom_agent.analyze_data({
                "type": "text",
                "content": "Sample content"
            })
            
            assert result == "Analysis result"
    
    def test_custom_agent_capabilities(self, custom_agent):
        """Тест возможностей пользовательского агента"""
        capabilities = custom_agent.get_capabilities()
        
        assert "custom_processing" in capabilities
        assert "custom_processing" in custom_agent.config.capabilities
    
    def test_custom_agent_limitations(self, custom_agent):
        """Тест ограничений пользовательского агента"""
        limitations = custom_agent.get_limitations()
        
        assert "Limited to custom tasks" in limitations
        assert "test_limitation" in custom_agent.config.limitations
    
    def test_custom_method(self, custom_agent):
        """Тест специализированного метода"""
        result = custom_agent.custom_method({"test": "data"})
        
        assert isinstance(result, dict)
        assert result["processed"] is True
        assert result["result"] == "custom_result"
```

### 2. Тесты для рабочих процессов

```python
# tests/unit/test_custom_workflow.py
import pytest
from unittest.mock import AsyncMock, patch
from src.workflow.custom_workflow import CustomWorkflow
from src.agents.base_agent import BaseAgent

class MockAgent(BaseAgent):
    """Мок-агент для тестирования"""
    def __init__(self, name: str):
        self.name = name
    
    async def process(self, input_data):
        return f"Processed by {self.name}: {input_data}"

@pytest.fixture
def mock_agents():
    """Фикстура для мок-агентов"""
    return {
        'analyzer': MockAgent('analyzer'),
        'validator': MockAgent('validator'),
        'evaluator': MockAgent('evaluator')
    }

@pytest.fixture
def custom_workflow(mock_agents):
    """Фикстура для пользовательского рабочего процесса"""
    workflow = CustomWorkflow(mock_agents)
    
    # Добавление тестовых шагов
    workflow.add_step(
        'step1',
        'analyzer',
        {'data': 'input_data'},
        'step1_result'
    )
    
    workflow.add_step(
        'step2',
        'validator',
        {'data': 'step1_result'},
        'step2_result'
    )
    
    return workflow

class TestCustomWorkflow:
    """Тесты для пользовательского рабочего процесса"""
    
    @pytest.mark.asyncio
    async def test_workflow_creation(self, custom_workflow):
        """Тест создания рабочего процесса"""
        assert custom_workflow is not None
        assert len(custom_workflow.workflow_steps) == 2
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self, custom_workflow):
        """Тест выполнения рабочего процесса"""
        initial_data = {'input_data': 'test data'}
        
        result = await custom_workflow.execute(initial_data)
        
        assert 'step1_result' in result
        assert 'step2_result' in result
        assert 'Processed by analyzer' in result['step1_result']
        assert 'Processed by validator' in result['step2_result']
    
    @pytest.mark.asyncio
    async def test_workflow_summary(self, custom_workflow):
        """Тест сводки рабочего процесса"""
        initial_data = {'input_data': 'test data'}
        await custom_workflow.execute(initial_data)
        
        summary = custom_workflow.get_workflow_summary()
        
        assert summary['total_steps'] == 2
        assert summary['completed_steps'] == 2
        assert 'step1' in summary['step_names']
        assert 'step2' in summary['step_names']
        assert len(summary['results']) == 2
    
    def test_workflow_input_preparation(self, custom_workflow):
        """Тест подготовки входных данных"""
        data = {'input_data': 'test', 'other_data': 'ignored'}
        mapping = {'data': 'input_data'}
        
        prepared = custom_workflow._prepare_agent_input(data, mapping)
        
        assert prepared == {'data': 'test'}
        assert 'other_data' not in prepared
```

## Интеграция с внешними системами

### 1. API интеграция

```python
# src/integrations/external_api.py
import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

class ExternalAPIIntegration:
    """Интеграция с внешними API"""
    
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    async def make_request(self, endpoint: str, method: str = 'GET',
                         data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Выполнение запроса к внешнему API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                async with self.session.get(url) as response:
                    return await response.json()
            elif method.upper() == 'POST':
                async with self.session.post(url, json=data) as response:
                    return await response.json()
            else:
                raise ValueError(f"Unsupported method: {method}")
                
        except Exception as e:
            self.logger.error(f"API request failed: {e}")
            return None
    
    async def batch_request(self, requests: list) -> list:
        """Пакетные запросы"""
        tasks = []
        for req in requests:
            task = self.make_request(req['endpoint'], req['method'], req.get('data'))
            tasks.append(task)
        
        return await asyncio.gather(*tasks, return_exceptions=True)

# Пример использования
async def integrate_with_external_api():
    """Пример интеграции с внешним API"""
    api_config = {
        'base_url': 'https://api.example.com',
        'api_key': 'your-api-key'
    }
    
    async with ExternalAPIIntegration(**api_config) as api:
        # Одиночный запрос
        result = await api.make_request('/data', 'GET')
        
        # Пакетные запросы
        requests = [
            {'endpoint': '/users', 'method': 'GET'},
            {'endpoint': '/posts', 'method': 'GET'},
            {'endpoint': '/create', 'method': 'POST', 'data': {'name': 'test'}}
        ]
        
        results = await api.batch_request(requests)
        return results
```

### 2. База данных интеграция

```python
# src/integrations/database.py
import asyncpg
import asyncio
from typing import Dict, Any, List, Optional
import logging

class DatabaseIntegration:
    """Интеграция с базой данных"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None
        self.logger = logging.getLogger(__name__)
    
    async def connect(self):
        """Подключение к базе данных"""
        self.pool = await asyncpg.create_pool(self.connection_string)
        self.logger.info("Connected to database")
    
    async def disconnect(self):
        """Отключение от базы данных"""
        if self.pool:
            await self.pool.close()
            self.logger.info("Disconnected from database")
    
    async def execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Выполнение запроса"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def execute_command(self, command: str, *args) -> str:
        """Выполнение команды"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(command, *args)
            return result
    
    async def save_agent_result(self, agent_name: str, input_data: Dict[str, Any],
                              output: str, execution_time: float) -> int:
        """Сохранение результата агента"""
        query = """
        INSERT INTO agent_results (agent_name, input_data, output, execution_time, created_at)
        VALUES ($1, $2, $3, $4, NOW())
        RETURNING id
        """
        
        result = await self.execute_query(
            query, agent_name, input_data, output, execution_time
        )
        
        return result[0]['id'] if result else None
    
    async def get_agent_history(self, agent_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Получение истории агента"""
        query = """
        SELECT * FROM agent_results 
        WHERE agent_name = $1 
        ORDER BY created_at DESC 
        LIMIT $2
        """
        
        return await self.execute_query(query, agent_name, limit)
    
    async def create_tables(self):
        """Создание таблиц"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS agent_results (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(100) NOT NULL,
            input_data JSONB,
            output TEXT,
            execution_time FLOAT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_agent_results_agent_name ON agent_results(agent_name);
        CREATE INDEX IF NOT EXISTS idx_agent_results_created_at ON agent_results(created_at);
        """
        
        await self.execute_command(create_table_query)

# Пример использования
async def setup_database_integration():
    """Настройка интеграции с базой данных"""
    db_config = {
        'connection_string': 'postgresql://user:password@localhost/agents_db'
    }
    
    db = DatabaseIntegration(**db_config)
    await db.connect()
    await db.create_tables()
    
    return db
```

## Документация кода

### 1. Docstring стандарты

```python
# Примеры документации для новых компонентов

class CustomAgent(BaseAgent):
    """
    Пользовательский агент для обработки специфических задач.
    
    Этот агент предоставляет базовую функциональность для создания
    специализированных агентов с пользовательской логикой обработки.
    
    Attributes:
        specialized_methods (List[str]): Список специализированных методов
        prompt_templates (CustomPromptTemplates): Шаблоны промптов
    
    Example:
        >>> config = AgentConfig(...)
        >>> agent = CustomAgent(config, api_key)
        >>> result = await agent.process({"data": "test"})
    """
    
    def __init__(self, config: AgentConfig, api_key: str = None):
        """
        Инициализация пользовательского агента.
        
        Args:
            config (AgentConfig): Конфигурация агента
            api_key (str, optional): API ключ для LLM
        
        Raises:
            ValueError: Если конфигурация некорректна
        """
        super().__init__(config, api_key)
        self.specialized_methods = []
    
    async def process(self, input_data: Any) -> str:
        """
        Обработка входных данных агентом.
        
        Args:
            input_data (Any): Входные данные для обработки
        
        Returns:
            str: Результат обработки
        
        Raises:
            ProcessingError: Если обработка не удалась
        
        Example:
            >>> result = await agent.process({"text": "Hello world"})
            >>> print(result)
            "CustomAgent Response: Processed text"
        """
        # Реализация обработки
        pass
    
    def custom_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Специализированный метод агента.
        
        Args:
            data (Dict[str, Any]): Входные данные
        
        Returns:
            Dict[str, Any]: Результат обработки
        
        Note:
            Этот метод предназначен для специфической обработки данных
            и может быть переопределен в подклассах.
        """
        return {"processed": True, "result": "custom_result"}
```

### 2. Type hints

```python
# Примеры типизации для новых компонентов
from typing import Union, Optional, Callable, TypeVar, Generic

T = TypeVar('T')

class WorkflowStep(Generic[T]):
    """Типизированный шаг рабочего процесса"""
    
    def __init__(self, name: str, processor: Callable[[T], T]):
        self.name = name
        self.processor = processor
    
    def process(self, data: T) -> T:
        """Обработка данных шагом"""
        return self.processor(data)

class AgentResult:
    """Результат работы агента"""
    
    def __init__(self, 
                 success: bool,
                 output: str,
                 execution_time: float,
                 metadata: Optional[Dict[str, Any]] = None):
        self.success = success
        self.output = output
        self.execution_time = execution_time
        self.metadata = metadata or {}

class WorkflowResult:
    """Результат выполнения рабочего процесса"""
    
    def __init__(self, 
                 steps_results: Dict[str, AgentResult],
                 total_time: float,
                 success: bool):
        self.steps_results = steps_results
        self.total_time = total_time
        self.success = success
```

Этот документ предоставляет comprehensive руководство по разработке и расширению мультиагентной системы, включая создание новых агентов, рабочих процессов, тестирование и интеграцию с внешними системами. 