"""
Специализированные агенты для конкретных задач (Итерация №5)
Агенты для работы с Confluence/JIRA, генерации кода и оценки идей
"""
from typing import Any, Dict, List, Optional
import json
import re
import os
from datetime import datetime
from .base_agent import BaseAgent, AgentConfig
from loguru import logger


def get_api_key() -> Optional[str]:
    """Получить API ключ из переменных окружения"""
    return os.getenv("OPENAI_API_KEY")


class ConfluenceJiraAnalystAgent(BaseAgent):
    """Агент для анализа данных из Confluence/JIRA"""
    
    async def process(self, input_data: Any) -> str:
        """Анализ данных из Confluence/JIRA"""
        if isinstance(input_data, dict):
            template_vars = {
                "data_source": input_data.get("data_source", "confluence"),
                "content_type": input_data.get("content_type", "pages"),
                "query": input_data.get("query", ""),
                "date_range": input_data.get("date_range", "last_30_days"),
                "analysis_type": input_data.get("analysis_type", "trend_analysis"),
                "context": input_data.get("context", "Анализ данных из Confluence/JIRA"),
                "metrics": input_data.get("metrics", ["engagement", "activity", "collaboration"])
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "data_source": "confluence",
                "content_type": "pages",
                "query": str(input_data),
                "date_range": "last_30_days",
                "analysis_type": "trend_analysis",
                "context": "Анализ данных из Confluence/JIRA",
                "metrics": ["engagement", "activity", "collaboration"]
            }
            return await self._generate_response("", template_vars)
    
    def extract_jira_metrics(self, jira_data: Dict[str, Any]) -> Dict[str, Any]:
        """Извлечение метрик из данных JIRA"""
        metrics = {
            "total_issues": len(jira_data.get("issues", [])),
            "by_status": {},
            "by_priority": {},
            "by_assignee": {},
            "avg_resolution_time": 0,
            "sprint_velocity": 0
        }
        
        # Анализ статусов
        for issue in jira_data.get("issues", []):
            status = issue.get("status", "Unknown")
            metrics["by_status"][status] = metrics["by_status"].get(status, 0) + 1
            
            priority = issue.get("priority", "Unknown")
            metrics["by_priority"][priority] = metrics["by_priority"].get(priority, 0) + 1
            
            assignee = issue.get("assignee", "Unassigned")
            metrics["by_assignee"][assignee] = metrics["by_assignee"].get(assignee, 0) + 1
        
        return metrics
    
    def extract_confluence_insights(self, confluence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Извлечение инсайтов из данных Confluence"""
        insights = {
            "total_pages": len(confluence_data.get("pages", [])),
            "total_comments": 0,
            "most_active_authors": {},
            "popular_topics": {},
            "collaboration_score": 0,
            "content_quality_score": 0
        }
        
        # Анализ страниц и комментариев
        for page in confluence_data.get("pages", []):
            insights["total_comments"] += len(page.get("comments", []))
            
            author = page.get("author", "Unknown")
            insights["most_active_authors"][author] = insights["most_active_authors"].get(author, 0) + 1
            
            # Анализ тегов/меток
            for tag in page.get("tags", []):
                insights["popular_topics"][tag] = insights["popular_topics"].get(tag, 0) + 1
        
        return insights


class CodeGenerationAgent(BaseAgent):
    """Агент для генерации и проверки Python-кода"""
    
    async def process(self, input_data: Any) -> str:
        """Генерация и проверка Python-кода"""
        if isinstance(input_data, dict):
            template_vars = {
                "task_description": input_data.get("task_description", ""),
                "code_type": input_data.get("code_type", "function"),
                "requirements": input_data.get("requirements", []),
                "framework": input_data.get("framework", "standard"),
                "testing_required": input_data.get("testing_required", True),
                "documentation_required": input_data.get("documentation_required", True),
                "context": input_data.get("context", "Генерация Python-кода")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "task_description": str(input_data),
                "code_type": "function",
                "requirements": [],
                "framework": "standard",
                "testing_required": True,
                "documentation_required": True,
                "context": "Генерация Python-кода"
            }
            return await self._generate_response("", template_vars)
    
    def validate_python_code(self, code: str) -> Dict[str, Any]:
        """Валидация Python-кода"""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": [],
            "complexity_score": 0,
            "maintainability_score": 0
        }
        
        # Проверка синтаксиса
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Синтаксическая ошибка: {e}")
        
        # Проверка PEP 8
        pep8_issues = self._check_pep8(code)
        validation_result["warnings"].extend(pep8_issues)
        
        # Анализ сложности
        validation_result["complexity_score"] = self._calculate_complexity(code)
        validation_result["maintainability_score"] = self._calculate_maintainability(code)
        
        return validation_result
    
    def _check_pep8(self, code: str) -> List[str]:
        """Проверка соответствия PEP 8"""
        issues = []
        
        # Проверка длины строк
        for i, line in enumerate(code.split('\n'), 1):
            if len(line) > 79:
                issues.append(f"Строка {i}: превышена максимальная длина (79 символов)")
        
        # Проверка отступов
        if not code.startswith('    ') and not code.startswith('\t'):
            if any(line.startswith(' ') for line in code.split('\n')[1:] if line.strip()):
                issues.append("Несогласованные отступы")
        
        return issues
    
    def _calculate_complexity(self, code: str) -> int:
        """Расчет сложности кода"""
        complexity = 0
        
        # Подсчет условных операторов
        complexity += len(re.findall(r'\bif\b|\belse\b|\belif\b', code))
        
        # Подсчет циклов
        complexity += len(re.findall(r'\bfor\b|\bwhile\b', code))
        
        # Подсчет исключений
        complexity += len(re.findall(r'\btry\b|\bexcept\b|\bfinally\b', code))
        
        return complexity
    
    def _calculate_maintainability(self, code: str) -> int:
        """Расчет поддерживаемости кода"""
        score = 100
        
        # Штраф за длинные функции
        lines = code.split('\n')
        if len(lines) > 50:
            score -= 20
        
        # Штраф за сложность
        complexity = self._calculate_complexity(code)
        if complexity > 10:
            score -= 30
        
        # Штраф за отсутствие документации
        if not re.search(r'""".*"""', code, re.DOTALL):
            score -= 15
        
        return max(0, score)
    
    def generate_test_code(self, main_code: str) -> str:
        """Генерация тестового кода"""
        # Извлекаем функции из основного кода
        functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):', main_code)
        
        test_code = """import pytest
from unittest.mock import Mock, patch

"""
        
        for func_name in functions:
            test_code += f"""
def test_{func_name}():
    \"\"\"Тест для функции {func_name}\"\"\"
    # TODO: Добавить тестовые случаи
    assert True
"""
        
        return test_code


class IdeaEvaluationAgent(BaseAgent):
    """Агент для оценки и фильтрации идей"""
    
    async def process(self, input_data: Any) -> str:
        """Оценка и фильтрация идей"""
        if isinstance(input_data, dict):
            template_vars = {
                "idea_description": input_data.get("idea_description", ""),
                "evaluation_criteria": input_data.get("evaluation_criteria", ["feasibility", "impact", "cost"]),
                "market_context": input_data.get("market_context", ""),
                "technical_constraints": input_data.get("technical_constraints", []),
                "business_goals": input_data.get("business_goals", []),
                "context": input_data.get("context", "Оценка идеи")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "idea_description": str(input_data),
                "evaluation_criteria": ["feasibility", "impact", "cost"],
                "market_context": "",
                "technical_constraints": [],
                "business_goals": [],
                "context": "Оценка идеи"
            }
            return await self._generate_response("", template_vars)
    
    def evaluate_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексная оценка идеи"""
        evaluation = {
            "overall_score": 0,
            "feasibility_score": 0,
            "impact_score": 0,
            "cost_score": 0,
            "risk_score": 0,
            "recommendation": "",
            "detailed_analysis": {},
            "next_steps": []
        }
        
        # Оценка реализуемости
        evaluation["feasibility_score"] = self._evaluate_feasibility(idea_data)
        
        # Оценка влияния
        evaluation["impact_score"] = self._evaluate_impact(idea_data)
        
        # Оценка стоимости
        evaluation["cost_score"] = self._evaluate_cost(idea_data)
        
        # Оценка рисков
        evaluation["risk_score"] = self._evaluate_risks(idea_data)
        
        # Общий балл
        evaluation["overall_score"] = (
            evaluation["feasibility_score"] * 0.3 +
            evaluation["impact_score"] * 0.4 +
            evaluation["cost_score"] * 0.2 +
            evaluation["risk_score"] * 0.1
        )
        
        # Рекомендация
        if evaluation["overall_score"] >= 8:
            evaluation["recommendation"] = "Сильно рекомендуется к реализации"
        elif evaluation["overall_score"] >= 6:
            evaluation["recommendation"] = "Рекомендуется к реализации"
        elif evaluation["overall_score"] >= 4:
            evaluation["recommendation"] = "Требует доработки"
        else:
            evaluation["recommendation"] = "Не рекомендуется к реализации"
        
        # Следующие шаги
        evaluation["next_steps"] = self._generate_next_steps(evaluation)
        
        return evaluation
    
    def _evaluate_feasibility(self, idea_data: Dict[str, Any]) -> float:
        """Оценка реализуемости идеи"""
        score = 5.0  # Базовый балл
        
        # Техническая реализуемость
        technical_complexity = idea_data.get("technical_complexity", "medium")
        if technical_complexity == "low":
            score += 2
        elif technical_complexity == "high":
            score -= 2
        
        # Наличие ресурсов
        resources_available = idea_data.get("resources_available", False)
        if resources_available:
            score += 1
        
        # Опыт команды
        team_experience = idea_data.get("team_experience", "medium")
        if team_experience == "high":
            score += 1
        elif team_experience == "low":
            score -= 1
        
        return min(10, max(0, score))
    
    def _evaluate_impact(self, idea_data: Dict[str, Any]) -> float:
        """Оценка влияния идеи"""
        score = 5.0  # Базовый балл
        
        # Потенциальная аудитория
        audience_size = idea_data.get("audience_size", "medium")
        if audience_size == "large":
            score += 2
        elif audience_size == "small":
            score -= 1
        
        # Бизнес-ценность
        business_value = idea_data.get("business_value", "medium")
        if business_value == "high":
            score += 2
        elif business_value == "low":
            score -= 1
        
        # Инновационность
        innovation_level = idea_data.get("innovation_level", "medium")
        if innovation_level == "high":
            score += 1
        elif innovation_level == "low":
            score -= 1
        
        return min(10, max(0, score))
    
    def _evaluate_cost(self, idea_data: Dict[str, Any]) -> float:
        """Оценка стоимости реализации"""
        score = 5.0  # Базовый балл
        
        # Размер инвестиций
        investment_size = idea_data.get("investment_size", "medium")
        if investment_size == "low":
            score += 2
        elif investment_size == "high":
            score -= 2
        
        # Время реализации
        implementation_time = idea_data.get("implementation_time", "medium")
        if implementation_time == "short":
            score += 1
        elif implementation_time == "long":
            score -= 1
        
        # ROI потенциал
        roi_potential = idea_data.get("roi_potential", "medium")
        if roi_potential == "high":
            score += 2
        elif roi_potential == "low":
            score -= 1
        
        return min(10, max(0, score))
    
    def _evaluate_risks(self, idea_data: Dict[str, Any]) -> float:
        """Оценка рисков"""
        score = 5.0  # Базовый балл
        
        # Технические риски
        technical_risks = idea_data.get("technical_risks", "medium")
        if technical_risks == "low":
            score += 1
        elif technical_risks == "high":
            score -= 2
        
        # Рыночные риски
        market_risks = idea_data.get("market_risks", "medium")
        if market_risks == "low":
            score += 1
        elif market_risks == "high":
            score -= 2
        
        # Конкурентные риски
        competitive_risks = idea_data.get("competitive_risks", "medium")
        if competitive_risks == "low":
            score += 1
        elif competitive_risks == "high":
            score -= 1
        
        return min(10, max(0, score))
    
    def _generate_next_steps(self, evaluation: Dict[str, Any]) -> List[str]:
        """Генерация следующих шагов"""
        steps = []
        
        if evaluation["overall_score"] >= 8:
            steps.extend([
                "Создать детальный план реализации",
                "Сформировать команду проекта",
                "Подготовить презентацию для стейкхолдеров",
                "Начать прототипирование"
            ])
        elif evaluation["overall_score"] >= 6:
            steps.extend([
                "Доработать концепцию",
                "Провести дополнительное исследование рынка",
                "Оценить ресурсы и бюджет",
                "Создать MVP план"
            ])
        elif evaluation["overall_score"] >= 4:
            steps.extend([
                "Пересмотреть концепцию",
                "Изучить альтернативные подходы",
                "Провести анализ конкурентов",
                "Определить ключевые риски"
            ])
        else:
            steps.extend([
                "Пересмотреть идею полностью",
                "Изучить другие возможности",
                "Провести анализ причин низкой оценки"
            ])
        
        return steps
    
    def filter_ideas(self, ideas: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Фильтрация идей по критериям"""
        filtered_ideas = []
        
        min_score = criteria.get("min_score", 6.0)
        required_criteria = criteria.get("required_criteria", [])
        excluded_criteria = criteria.get("excluded_criteria", [])
        
        for idea in ideas:
            evaluation = self.evaluate_idea(idea)
            
            # Проверка минимального балла
            if evaluation["overall_score"] < min_score:
                continue
            
            # Проверка обязательных критериев
            if required_criteria:
                idea_meets_requirements = True
                for criterion in required_criteria:
                    if not self._check_criterion(idea, criterion):
                        idea_meets_requirements = False
                        break
                if not idea_meets_requirements:
                    continue
            
            # Проверка исключающих критериев
            if excluded_criteria:
                idea_should_be_excluded = False
                for criterion in excluded_criteria:
                    if self._check_criterion(idea, criterion):
                        idea_should_be_excluded = True
                        break
                if idea_should_be_excluded:
                    continue
            
            filtered_ideas.append({
                "idea": idea,
                "evaluation": evaluation
            })
        
        # Сортировка по общему баллу
        filtered_ideas.sort(key=lambda x: x["evaluation"]["overall_score"], reverse=True)
        
        return filtered_ideas
    
    def _check_criterion(self, idea: Dict[str, Any], criterion: str) -> bool:
        """Проверка соответствия критерию"""
        if criterion == "high_feasibility":
            return idea.get("technical_complexity", "medium") == "low"
        elif criterion == "high_impact":
            return idea.get("business_value", "medium") == "high"
        elif criterion == "low_cost":
            return idea.get("investment_size", "medium") == "low"
        elif criterion == "innovative":
            return idea.get("innovation_level", "medium") == "high"
        return False


class ProjectManagementAgent(BaseAgent):
    """Агент для управления проектами на основе анализа данных"""
    
    async def process(self, input_data: Any) -> str:
        """Управление проектами"""
        if isinstance(input_data, dict):
            template_vars = {
                "project_data": input_data.get("project_data", {}),
                "team_data": input_data.get("team_data", {}),
                "progress_data": input_data.get("progress_data", {}),
                "analysis_type": input_data.get("analysis_type", "project_health"),
                "context": input_data.get("context", "Управление проектом")
            }
            return await self._generate_response("", template_vars)
        else:
            template_vars = {
                "project_data": {},
                "team_data": {},
                "progress_data": {},
                "analysis_type": "project_health",
                "context": "Управление проектом"
            }
            return await self._generate_response("", template_vars)
    
    def analyze_project_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ здоровья проекта"""
        health_metrics = {
            "overall_health": 0,
            "schedule_health": 0,
            "budget_health": 0,
            "quality_health": 0,
            "team_health": 0,
            "risks": [],
            "recommendations": []
        }
        
        # Анализ расписания
        schedule_progress = project_data.get("schedule_progress", 0)
        schedule_planned = project_data.get("schedule_planned", 0)
        
        if schedule_planned > 0:
            schedule_variance = (schedule_progress - schedule_planned) / schedule_planned
            if abs(schedule_variance) <= 0.1:
                health_metrics["schedule_health"] = 90
            elif abs(schedule_variance) <= 0.2:
                health_metrics["schedule_health"] = 70
            else:
                health_metrics["schedule_health"] = 40
                health_metrics["risks"].append("Отставание от графика")
        
        # Анализ бюджета
        budget_spent = project_data.get("budget_spent", 0)
        budget_planned = project_data.get("budget_planned", 0)
        
        if budget_planned > 0:
            budget_variance = (budget_spent - budget_planned) / budget_planned
            if abs(budget_variance) <= 0.1:
                health_metrics["budget_health"] = 90
            elif abs(budget_variance) <= 0.2:
                health_metrics["budget_health"] = 70
            else:
                health_metrics["budget_health"] = 40
                health_metrics["risks"].append("Превышение бюджета")
        
        # Анализ качества
        quality_metrics = project_data.get("quality_metrics", {})
        if quality_metrics:
            defect_rate = quality_metrics.get("defect_rate", 0)
            if defect_rate <= 0.05:
                health_metrics["quality_health"] = 90
            elif defect_rate <= 0.1:
                health_metrics["quality_health"] = 70
            else:
                health_metrics["quality_health"] = 40
                health_metrics["risks"].append("Высокий уровень дефектов")
        
        # Анализ команды
        team_metrics = project_data.get("team_metrics", {})
        if team_metrics:
            team_satisfaction = team_metrics.get("satisfaction", 0)
            team_productivity = team_metrics.get("productivity", 0)
            
            health_metrics["team_health"] = (team_satisfaction + team_productivity) / 2
            
            if team_satisfaction < 0.7:
                health_metrics["risks"].append("Низкая удовлетворенность команды")
            if team_productivity < 0.7:
                health_metrics["risks"].append("Низкая продуктивность команды")
        
        # Общий показатель здоровья
        health_metrics["overall_health"] = (
            health_metrics["schedule_health"] * 0.3 +
            health_metrics["budget_health"] * 0.3 +
            health_metrics["quality_health"] * 0.2 +
            health_metrics["team_health"] * 0.2
        )
        
        # Генерация рекомендаций
        health_metrics["recommendations"] = self._generate_project_recommendations(health_metrics)
        
        return health_metrics
    
    def _generate_project_recommendations(self, health_metrics: Dict[str, Any]) -> List[str]:
        """Генерация рекомендаций по проекту"""
        recommendations = []
        
        if health_metrics["schedule_health"] < 70:
            recommendations.append("Пересмотреть график проекта и приоритизировать задачи")
        
        if health_metrics["budget_health"] < 70:
            recommendations.append("Провести анализ затрат и оптимизировать бюджет")
        
        if health_metrics["quality_health"] < 70:
            recommendations.append("Усилить процессы контроля качества")
        
        if health_metrics["team_health"] < 70:
            recommendations.append("Провести ретроспективу команды и улучшить коммуникацию")
        
        if health_metrics["overall_health"] < 60:
            recommendations.append("Требуется вмешательство руководства проекта")
        
        return recommendations


# Фабрика для создания специализированных агентов
class TaskSpecificAgentFactory:
    """Фабрика для создания специализированных агентов задач"""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, api_key: str = None) -> BaseAgent:
        """Создать специализированного агента"""
        
        agent_classes = {
            "confluence_jira_analyst": ConfluenceJiraAnalystAgent,
            "code_generator": CodeGenerationAgent,
            "idea_evaluator": IdeaEvaluationAgent,
            "project_manager": ProjectManagementAgent
        }
        
        if agent_type not in agent_classes:
            raise ValueError(f"Неизвестный тип специализированного агента: {agent_type}")
        
        agent_class = agent_classes[agent_type]
        return agent_class(config, api_key)
    
    @staticmethod
    def get_available_agent_types() -> List[str]:
        """Получить список доступных типов специализированных агентов"""
        return [
            "confluence_jira_analyst",
            "code_generator", 
            "idea_evaluator",
            "project_manager"
        ] 