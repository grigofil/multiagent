# Конфигурация

## Структура конфигурации

### Конфигурация агентов

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
      top_p: 0.9
    system_prompt: "Ты эксперт по анализу данных из Confluence и JIRA..."
    capabilities:
      - "confluence_analysis"
      - "jira_metrics"
      - "insights_generation"
    limitations:
      - "Требует доступ к API Confluence/JIRA"
      - "Ограничен анализом текстовых данных"
```

### Конфигурация ролей

```yaml
# config/agent_roles.yaml
roles:
  data_analyst:
    name: "Data Analyst"
    description: "Специалист по анализу данных"
    capabilities:
      - "data_analysis"
      - "metrics_extraction"
      - "insights_generation"
    required_skills:
      - "statistics"
      - "data_visualization"
      - "sql"
    tools:
      - "pandas"
      - "numpy"
      - "matplotlib"
```

### Конфигурация взаимодействий

```yaml
# config/interactions.yaml
interactions:
  data_analysis_workflow:
    name: "Data Analysis Workflow"
    description: "Рабочий процесс анализа данных"
    agents:
      - "confluence_jira_analyst"
      - "data_processor"
      - "insights_generator"
    steps:
      - name: "data_collection"
        agent: "confluence_jira_analyst"
        input: "raw_data"
        output: "processed_data"
        timeout: 300
        retries: 3
    error_handling:
      strategy: "retry"
      max_retries: 3
      backoff_factor: 2
    monitoring:
      enabled: true
      metrics:
        - "execution_time"
        - "success_rate"
        - "error_rate"
```

## Переменные окружения

### Основные переменные

```bash
# .env
# API Keys
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# System Configuration
AGENT_SYSTEM_ENV=development
LOG_LEVEL=DEBUG
DEBUG_MODE=true

# Database
DATABASE_URL=postgresql://user:password@localhost/agents_db

# Monitoring
MONITORING_ENABLED=true
METRICS_ENDPOINT=http://localhost:9090

# Cache
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# LangGraph
LANGGRAPH_ENDPOINT=http://localhost:8123
CHECKPOINT_DIR=./checkpoints
```

### Загрузка переменных

```python
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Получение переменных
openai_api_key = os.getenv("OPENAI_API_KEY")
system_env = os.getenv("AGENT_SYSTEM_ENV", "development")
log_level = os.getenv("LOG_LEVEL", "INFO")
```

## Поддерживаемые провайдеры LLM

### OpenAI
```yaml
model:
  provider: "openai"
  model_name: "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 4000
```

### Anthropic Claude
```yaml
model:
  provider: "anthropic"
  model_name: "claude-3-sonnet"
  temperature: 0.7
  max_tokens: 4000
```

### Google Gemini
```yaml
model:
  provider: "google"
  model_name: "gemini-pro"
  temperature: 0.7
  max_tokens: 4000
```

## Параметры модели

| Параметр | Описание | Значение по умолчанию |
|----------|----------|----------------------|
| `provider` | Провайдер LLM | "openai" |
| `model_name` | Название модели | "gpt-3.5-turbo" |
| `temperature` | Температура (креативность) | 0.7 |
| `max_tokens` | Максимальное количество токенов | 4000 |
| `top_p` | Параметр top_p | 0.9 |

## Шаблоны конфигурации

### Базовый агент
```yaml
# config/templates/base_agent.yaml
base_agent_template:
  name: "Base Agent"
  role: "General Purpose"
  description: "Базовый агент для общих задач"
  model:
    provider: "openai"
    model_name: "gpt-3.5-turbo"
    temperature: 0.7
    max_tokens: 4000
  system_prompt: "Ты полезный AI-ассистент."
  capabilities:
    - "general_assistance"
    - "text_processing"
  limitations:
    - "Общие ограничения"
```

### Специализированный агент
```yaml
# config/templates/specialized_agent.yaml
specialized_agent_template:
  name: "Specialized Agent"
  role: "Domain Specialist"
  description: "Специализированный агент для конкретной области"
  model:
    provider: "openai"
    model_name: "gpt-4"
    temperature: 0.5
    max_tokens: 6000
  system_prompt: |
    Ты эксперт в области [DOMAIN].
    Твоя задача - [SPECIFIC_TASK].
  capabilities:
    - "domain_specific_task"
    - "expert_analysis"
  limitations:
    - "Специализирован на конкретную область"
```

## Валидация конфигурации

### Схема валидации

```python
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional

class ModelConfig(BaseModel):
    provider: str
    model_name: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(gt=0, le=8000)
    top_p: float = Field(ge=0.0, le=1.0)

class AgentConfig(BaseModel):
    name: str
    role: str
    description: str
    model: ModelConfig
    system_prompt: str
    prompt_template: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v

    @validator('system_prompt')
    def validate_system_prompt(cls, v):
        if len(v) < 10:
            raise ValueError('System prompt too short')
        return v
```

### Функция валидации

```python
import yaml
from pathlib import Path
from typing import Dict, Any

def validate_config(config_path: Path) -> Dict[str, Any]:
    """
    Валидирует конфигурационный файл
    """
    try:
        # Загрузка YAML
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # Валидация агентов
        if 'agents' in config_data:
            for agent_name, agent_config in config_data['agents'].items():
                AgentConfig(**agent_config)
        
        print(f"✅ Конфигурация {config_path} валидна")
        return config_data
        
    except Exception as e:
        print(f"❌ Ошибка валидации {config_path}: {e}")
        raise

# Использование
config_path = Path("config/agents_config.yaml")
validated_config = validate_config(config_path)
```

## Проверка конфигурации

```python
def check_configuration():
    """
    Проверяет все конфигурационные файлы
    """
    config_files = [
        "config/agents_config.yaml",
        "config/agent_roles.yaml",
        "config/interactions.yaml"
    ]
    
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            try:
                validate_config(config_path)
            except Exception as e:
                print(f"Ошибка в {config_file}: {e}")
        else:
            print(f"⚠️ Файл {config_file} не найден")

# Запуск проверки
check_configuration()
``` 