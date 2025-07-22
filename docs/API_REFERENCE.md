# API Reference

## TaskSpecificAgentFactory

### Методы

```python
@staticmethod
def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent

@staticmethod
def get_available_agent_types() -> List[str]
```

**Поддерживаемые типы агентов**:
- `confluence_jira_analyst` - ConfluenceJiraAnalystAgent
- `code_generator` - CodeGenerationAgent
- `idea_evaluator` - IdeaEvaluationAgent
- `project_manager` - ProjectManagementAgent

## BaseAgent

### Конструктор
```python
BaseAgent(config: AgentConfig, api_key: Optional[str] = None)
```

### Методы
```python
async def process(self, input_data: Any) -> str
async def _generate_response(self, input_text: str, template_vars: Dict[str, Any] = None) -> str
def get_capabilities(self) -> List[str]
def get_limitations(self) -> List[str]
def reset_state(self) -> None
def get_info(self) -> Dict[str, Any]
```

## ConfluenceJiraAnalystAgent

### Дополнительные методы
```python
def extract_jira_metrics(self, jira_data: Dict[str, Any]) -> Dict[str, Any]
def extract_confluence_insights(self, confluence_data: Dict[str, Any]) -> Dict[str, Any]
```

## CodeGenerationAgent

### Дополнительные методы
```python
def validate_python_code(self, code: str) -> Dict[str, Any]
def generate_test_code(self, main_code: str) -> str
def _check_pep8(self, code: str) -> List[str]
def _calculate_complexity(self, code: str) -> int
def _calculate_maintainability(self, code: str) -> int
```

## IdeaEvaluationAgent

### Дополнительные методы
```python
def evaluate_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]
def filter_ideas(self, ideas: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]
def _evaluate_feasibility(self, idea_data: Dict[str, Any]) -> float
def _evaluate_impact(self, idea_data: Dict[str, Any]) -> float
def _evaluate_cost(self, idea_data: Dict[str, Any]) -> float
def _evaluate_risks(self, idea_data: Dict[str, Any]) -> float
```

## ProjectManagementAgent

### Дополнительные методы
```python
def analyze_project_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]
def _generate_project_recommendations(self, health_metrics: Dict[str, Any]) -> List[str]
```

## AgentConfig

### Структура
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

### Пример конфигурации
```python
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
``` 