# Примеры использования

## Анализ данных Confluence/JIRA

```python
import asyncio
from src.agents.task_specific_agents import TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

async def analyze_project_data():
    # Создание конфигурации
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
    
    # Создание агента
    factory = TaskSpecificAgentFactory()
    agent = factory.create_agent("confluence_jira_analyst", config, api_key)
    
    # Данные для анализа
    data = {
        "confluence_pages": [
            {"title": "Project Overview", "content": "Project content", "views": 150}
        ],
        "jira_issues": [
            {"key": "PROJ-101", "status": "In Progress", "priority": "High"}
        ]
    }
    
    # Анализ
    result = await agent.process(data)
    print(f"Analysis result: {result}")
    
    # Извлечение метрик
    jira_metrics = agent.extract_jira_metrics({"issues": data["jira_issues"]})
    confluence_insights = agent.extract_confluence_insights({"pages": data["confluence_pages"]})
    
    print(f"JIRA metrics: {jira_metrics}")
    print(f"Confluence insights: {confluence_insights}")

# Запуск
asyncio.run(analyze_project_data())
```

## Генерация и валидация кода

```python
import asyncio
from src.agents.task_specific_agents import TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

async def generate_and_validate_code():
    # Создание конфигурации
    config = AgentConfig(
        name="Code Generator",
        role="Code Generation Specialist",
        description="Генерирует и валидирует код",
        model={
            "provider": "openai",
            "model_name": "gpt-4",
            "temperature": 0.3
        },
        system_prompt="Ты эксперт по Python программированию...",
        capabilities=["code_generation", "code_validation"]
    )
    
    # Создание агента
    factory = TaskSpecificAgentFactory()
    agent = factory.create_agent("code_generator", config, api_key)
    
    # Генерация кода
    result = await agent.process({
        "task_description": "Generate a function to calculate fibonacci numbers",
        "code_type": "function",
        "requirements": ["recursive", "memoization", "type hints"]
    })
    
    print(f"Generated code:\n{result}")
    
    # Валидация кода
    validation = agent.validate_python_code(result)
    print(f"Validation result: {validation}")
    
    # Генерация тестов
    test_code = agent.generate_test_code(result)
    print(f"Test code:\n{test_code}")

# Запуск
asyncio.run(generate_and_validate_code())
```

## Оценка бизнес-идей

```python
import asyncio
from src.agents.task_specific_agents import TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

async def evaluate_business_ideas():
    # Создание конфигурации
    config = AgentConfig(
        name="Idea Evaluator",
        role="Business Strategy Specialist",
        description="Оценивает бизнес-идеи",
        model={
            "provider": "openai",
            "model_name": "gpt-4",
            "temperature": 0.5
        },
        system_prompt="Ты эксперт по бизнес-стратегии...",
        capabilities=["idea_evaluation", "market_analysis"]
    )
    
    # Создание агента
    factory = TaskSpecificAgentFactory()
    agent = factory.create_agent("idea_evaluator", config, api_key)
    
    # Идеи для оценки
    ideas = [
        {
            "title": "AI-Powered Code Review Assistant",
            "description": "An AI tool that automatically reviews code changes",
            "category": "Development Tools",
            "target_audience": "Software Developers",
            "estimated_effort": "6 months",
            "budget_required": "$50,000"
        },
        {
            "title": "Smart Home Energy Management",
            "description": "IoT system for optimizing home energy consumption",
            "category": "IoT/Smart Home",
            "target_audience": "Homeowners",
            "estimated_effort": "12 months",
            "budget_required": "$200,000"
        }
    ]
    
    # Оценка каждой идеи
    for idea in ideas:
        evaluation = agent.evaluate_idea(idea)
        print(f"Idea: {idea['title']}")
        print(f"Overall Score: {evaluation['overall_score']}")
        print(f"Feasibility: {evaluation['feasibility_score']}")
        print(f"Impact: {evaluation['impact_score']}")
        print(f"Cost: {evaluation['cost_score']}")
        print(f"Risk: {evaluation['risk_score']}")
        print("---")
    
    # Фильтрация идей
    filter_criteria = {
        "max_budget": 100000,
        "max_effort_months": 12,
        "min_feasibility_score": 7.0
    }
    
    filtered_ideas = agent.filter_ideas(ideas, filter_criteria)
    print(f"Filtered ideas: {len(filtered_ideas)}")

# Запуск
asyncio.run(evaluate_business_ideas())
```

## Анализ здоровья проекта

```python
import asyncio
from src.agents.task_specific_agents import TaskSpecificAgentFactory
from src.agents.base_agent import AgentConfig

async def analyze_project_health():
    # Создание конфигурации
    config = AgentConfig(
        name="Project Manager",
        role="Project Management Specialist",
        description="Анализирует здоровье проектов",
        model={
            "provider": "openai",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.6
        },
        system_prompt="Ты эксперт по управлению проектами...",
        capabilities=["project_analysis", "risk_assessment"]
    )
    
    # Создание агента
    factory = TaskSpecificAgentFactory()
    agent = factory.create_agent("project_manager", config, api_key)
    
    # Данные проекта
    project_data = {
        "tasks": [
            {"status": "completed", "priority": "high"},
            {"status": "in_progress", "priority": "medium"},
            {"status": "blocked", "priority": "high"}
        ],
        "team_members": ["dev1", "dev2", "dev3"],
        "timeline": {"start": "2024-01-01", "end": "2024-06-01"},
        "budget": {
            "planned": 100000,
            "spent": 75000
        },
        "quality_metrics": {
            "defect_rate": 0.03
        },
        "team_metrics": {
            "satisfaction": 0.8,
            "productivity": 0.85
        }
    }
    
    # Анализ здоровья проекта
    health_result = agent.analyze_project_health(project_data)
    
    print(f"Overall Health: {health_result['overall_health']}")
    print(f"Schedule Health: {health_result['schedule_health']}")
    print(f"Budget Health: {health_result['budget_health']}")
    print(f"Quality Health: {health_result['quality_health']}")
    print(f"Team Health: {health_result['team_health']}")
    
    print("\nRisks:")
    for risk in health_result['risks']:
        print(f"- {risk}")
    
    print("\nRecommendations:")
    for rec in health_result['recommendations']:
        print(f"- {rec}")

# Запуск
asyncio.run(analyze_project_health())
``` 