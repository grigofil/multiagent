#!/usr/bin/env python3
"""
Tests for Iteration #5: Practical Usage Examples
Tests specialized agents and example implementations.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import json

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.task_specific_agents import (
    ConfluenceJiraAnalystAgent,
    CodeGenerationAgent,
    IdeaEvaluationAgent,
    ProjectManagementAgent,
    TaskSpecificAgentFactory
)
from agents.base_agent import BaseAgent

# Test fixtures
@pytest.fixture
def mock_api_key():
    return "test-api-key-12345"

@pytest.fixture
def mock_config():
    from agents.base_agent import AgentConfig
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
def confluence_jira_data():
    """Sample Confluence/JIRA data for testing."""
    return {
        "confluence_pages": [
            {
                "id": "page1",
                "title": "Project Overview",
                "content": "This is a test project overview page.",
                "last_modified": "2024-01-15T10:00:00Z",
                "author": "john.doe",
                "views": 150
            },
            {
                "id": "page2",
                "title": "Technical Architecture",
                "content": "System architecture documentation with diagrams.",
                "last_modified": "2024-01-20T14:30:00Z",
                "author": "jane.smith",
                "views": 89
            }
        ],
        "jira_issues": [
            {
                "key": "PROJ-101",
                "summary": "Implement user authentication",
                "status": "In Progress",
                "priority": "High",
                "assignee": "dev1",
                "created": "2024-01-10T09:00:00Z",
                "updated": "2024-01-18T16:45:00Z"
            },
            {
                "key": "PROJ-102",
                "summary": "Fix login bug",
                "status": "Done",
                "priority": "Medium",
                "assignee": "dev2",
                "created": "2024-01-12T11:30:00Z",
                "updated": "2024-01-19T10:15:00Z"
            }
        ]
    }

@pytest.fixture
def sample_code():
    """Sample Python code for testing."""
    return '''
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def process_data(data_list):
    """Process a list of data items."""
    result = []
    for item in data_list:
        if item > 0:
            result.append(item * 2)
    return result
    '''

@pytest.fixture
def sample_ideas():
    """Sample business ideas for testing."""
    return [
        {
            "title": "AI-Powered Code Review Assistant",
            "description": "An AI tool that automatically reviews code changes.",
            "category": "Development Tools",
            "target_audience": "Software Developers",
            "estimated_effort": "6 months",
            "budget_required": "$50,000"
        },
        {
            "title": "Smart Home Energy Management",
            "description": "IoT system for optimizing home energy consumption.",
            "category": "IoT/Smart Home",
            "target_audience": "Homeowners",
            "estimated_effort": "12 months",
            "budget_required": "$200,000"
        }
    ]

class TestConfluenceJiraAnalystAgent:
    """Tests for ConfluenceJiraAnalystAgent."""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self, mock_api_key, mock_config):
        """Test agent creation."""
        agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
        assert agent.config.name == "Test Agent"
        assert agent.config.role == "Test Role"
        assert agent.api_key == mock_api_key
    
    @pytest.mark.asyncio
    async def test_analyze_confluence_data(self, mock_api_key, mock_config, confluence_jira_data):
        """Test Confluence data analysis."""
        agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = "Analysis result: High engagement on technical documentation"
            
            result = await agent.process({
                "confluence_pages": confluence_jira_data["confluence_pages"],
                "data_source": "confluence",
                "analysis_type": "trend_analysis"
            })
            
            assert isinstance(result, str)
            assert "Analysis result" in result
            mock_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_jira_data(self, mock_api_key, mock_config, confluence_jira_data):
        """Test JIRA data analysis."""
        agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = "JIRA Analysis: 2 issues, 1 in progress, 1 completed"
            
            result = await agent.process({
                "jira_issues": confluence_jira_data["jira_issues"],
                "data_source": "jira",
                "analysis_type": "issue_analysis"
            })
            
            assert isinstance(result, str)
            assert "JIRA Analysis" in result
            mock_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_extract_metrics(self, mock_api_key, mock_config, confluence_jira_data):
        """Test metrics extraction."""
        agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
        
        # Test the extract_jira_metrics method
        jira_metrics = agent.extract_jira_metrics({"issues": confluence_jira_data["jira_issues"]})
        
        assert "total_issues" in jira_metrics
        assert jira_metrics["total_issues"] == 2
        assert "by_status" in jira_metrics
        assert "by_priority" in jira_metrics
    
    @pytest.mark.asyncio
    async def test_generate_insights(self, mock_api_key, mock_config, confluence_jira_data):
        """Test insights generation."""
        agent = ConfluenceJiraAnalystAgent(mock_config, mock_api_key)
        
        # Test the extract_confluence_insights method
        confluence_insights = agent.extract_confluence_insights({"pages": confluence_jira_data["confluence_pages"]})
        
        assert "total_pages" in confluence_insights
        assert confluence_insights["total_pages"] == 2
        assert "most_active_authors" in confluence_insights
        assert "popular_topics" in confluence_insights

class TestCodeGenerationAgent:
    """Tests for CodeGenerationAgent."""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self, mock_api_key, mock_config):
        """Test agent creation."""
        agent = CodeGenerationAgent(mock_config, mock_api_key)
        assert agent.config.name == "Test Agent"
        assert agent.config.role == "Test Role"
        assert agent.api_key == mock_api_key
    
    @pytest.mark.asyncio
    async def test_generate_code(self, mock_api_key, mock_config):
        """Test code generation."""
        agent = CodeGenerationAgent(mock_config, mock_api_key)
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = '''
def factorial(n):
    """Calculate factorial of a number."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
            '''
            
            result = await agent.process({
                "task_description": "Generate a function to calculate factorial",
                "code_type": "function",
                "requirements": ["recursive", "input validation"]
            })
            
            assert isinstance(result, str)
            assert "def factorial" in result
            mock_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_code(self, mock_api_key, mock_config, sample_code):
        """Test code validation."""
        agent = CodeGenerationAgent(mock_config, mock_api_key)
        
        # Test the validate_python_code method
        validation_result = agent.validate_python_code(sample_code)
        
        assert isinstance(validation_result, dict)
        assert "is_valid" in validation_result
        assert "complexity_score" in validation_result
        assert "maintainability_score" in validation_result
        assert "errors" in validation_result
    
    @pytest.mark.asyncio
    async def test_improve_code(self, mock_api_key, mock_config, sample_code):
        """Test code improvement."""
        agent = CodeGenerationAgent(mock_config, mock_api_key)
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = '''
from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
            '''
            
            result = await agent.process({
                "task_description": "Add type hints and improve error handling",
                "code_type": "function",
                "requirements": ["type hints", "error handling"]
            })
            
            assert isinstance(result, str)
            assert "from typing import" in result
            assert "List[Union[int, float]]" in result
    
    @pytest.mark.asyncio
    async def test_generate_test_code(self, mock_api_key, mock_config):
        """Test test code generation."""
        agent = CodeGenerationAgent(mock_config, mock_api_key)
        function_code = '''
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
        '''
        
        # Test the generate_test_code method
        test_code = agent.generate_test_code(function_code)
        
        assert isinstance(test_code, str)
        assert len(test_code) > 0

class TestIdeaEvaluationAgent:
    """Tests for IdeaEvaluationAgent."""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self, mock_api_key, mock_config):
        """Test agent creation."""
        agent = IdeaEvaluationAgent(mock_config, mock_api_key)
        assert agent.config.name == "Test Agent"
        assert agent.config.role == "Test Role"
        assert agent.api_key == mock_api_key
    
    @pytest.mark.asyncio
    async def test_evaluate_idea(self, mock_api_key, mock_config, sample_ideas):
        """Test individual idea evaluation."""
        agent = IdeaEvaluationAgent(mock_config, mock_api_key)
        idea = sample_ideas[0]
        
        # Test the evaluate_idea method
        evaluation_result = agent.evaluate_idea(idea)
        
        assert isinstance(evaluation_result, dict)
        assert "feasibility_score" in evaluation_result
        assert "impact_score" in evaluation_result
        assert "cost_score" in evaluation_result
        assert "risk_score" in evaluation_result
        assert "overall_score" in evaluation_result
    
    @pytest.mark.asyncio
    async def test_compare_ideas(self, mock_api_key, mock_config, sample_ideas):
        """Test idea comparison."""
        agent = IdeaEvaluationAgent(mock_config, mock_api_key)
        
        # Test the filter_ideas method
        filter_criteria = {
            "max_budget": 100000,
            "max_effort_months": 12,
            "min_feasibility_score": 7.0
        }
        
        filtered_ideas = agent.filter_ideas(sample_ideas, filter_criteria)
        
        assert isinstance(filtered_ideas, list)
        assert len(filtered_ideas) <= len(sample_ideas)
    
    @pytest.mark.asyncio
    async def test_filter_ideas(self, mock_api_key, mock_config, sample_ideas):
        """Test idea filtering."""
        agent = IdeaEvaluationAgent(mock_config, mock_api_key)
        filter_criteria = {
            "max_budget": 100000,
            "max_effort_months": 12,
            "min_feasibility_score": 7.0
        }
        
        # Test the filter_ideas method
        filtered_ideas = agent.filter_ideas(sample_ideas, filter_criteria)
        
        assert isinstance(filtered_ideas, list)
        assert len(filtered_ideas) <= len(sample_ideas)
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, mock_api_key, mock_config):
        """Test recommendation generation."""
        agent = IdeaEvaluationAgent(mock_config, mock_api_key)
        
        with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = "Recommendation: Focus on AI-powered tools for development teams"
            
            result = await agent.process({
                "company_profile": "Tech startup",
                "team_expertise": ["Python", "AI"],
                "budget_constraints": "$100K"
            })
            
            assert isinstance(result, str)
            assert len(result) > 0

class TestProjectManagementAgent:
    """Tests for ProjectManagementAgent."""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self, mock_api_key, mock_config):
        """Test agent creation."""
        agent = ProjectManagementAgent(mock_config, mock_api_key)
        assert agent.config.name == "Test Agent"
        assert agent.config.role == "Test Role"
        assert agent.api_key == mock_api_key
    
    @pytest.mark.asyncio
    async def test_analyze_project_health(self, mock_api_key, mock_config):
        """Test project health analysis."""
        agent = ProjectManagementAgent(mock_config, mock_api_key)
        project_data = {
            "tasks": [
                {"status": "completed", "priority": "high"},
                {"status": "in_progress", "priority": "medium"},
                {"status": "blocked", "priority": "high"}
            ],
            "team_members": ["dev1", "dev2", "dev3"],
            "timeline": {"start": "2024-01-01", "end": "2024-06-01"}
        }
        
        # Test the analyze_project_health method
        health_result = agent.analyze_project_health(project_data)
        
        assert isinstance(health_result, dict)
        assert "overall_health" in health_result
        assert "schedule_health" in health_result
        assert "budget_health" in health_result
        assert "quality_health" in health_result
        assert "team_health" in health_result
        assert "risks" in health_result
        assert "recommendations" in health_result

class TestTaskSpecificAgentFactory:
    """Tests for TaskSpecificAgentFactory."""
    
    @pytest.mark.asyncio
    async def test_factory_creation(self):
        """Test factory creation."""
        factory = TaskSpecificAgentFactory()
        assert factory is not None
    
    @pytest.mark.asyncio
    async def test_create_confluence_jira_analyst(self, mock_config):
        """Test creating ConfluenceJiraAnalystAgent."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value="test-key"):
            agent = factory.create_agent("confluence_jira_analyst", mock_config, "test-key")
            
            assert isinstance(agent, ConfluenceJiraAnalystAgent)
            assert agent.config.name == "Test Agent"
    
    @pytest.mark.asyncio
    async def test_create_code_generation_agent(self, mock_config):
        """Test creating CodeGenerationAgent."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value="test-key"):
            agent = factory.create_agent("code_generator", mock_config, "test-key")
            
            assert isinstance(agent, CodeGenerationAgent)
            assert agent.config.name == "Test Agent"
    
    @pytest.mark.asyncio
    async def test_create_idea_evaluation_agent(self, mock_config):
        """Test creating IdeaEvaluationAgent."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value="test-key"):
            agent = factory.create_agent("idea_evaluator", mock_config, "test-key")
            
            assert isinstance(agent, IdeaEvaluationAgent)
            assert agent.config.name == "Test Agent"
    
    @pytest.mark.asyncio
    async def test_create_project_management_agent(self, mock_config):
        """Test creating ProjectManagementAgent."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value="test-key"):
            agent = factory.create_agent("project_manager", mock_config, "test-key")
            
            assert isinstance(agent, ProjectManagementAgent)
            assert agent.config.name == "Test Agent"
    
    @pytest.mark.asyncio
    async def test_create_unknown_agent(self, mock_config):
        """Test creating unknown agent type."""
        factory = TaskSpecificAgentFactory()
        
        with pytest.raises(ValueError, match="Неизвестный тип специализированного агента"):
            factory.create_agent("unknown_agent", mock_config, "test-key")

class TestIntegration:
    """Integration tests for Iteration #5 components."""
    
    @pytest.mark.asyncio
    async def test_full_confluence_jira_workflow(self, mock_api_key, mock_config):
        """Test complete Confluence/JIRA analysis workflow."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value=mock_api_key):
            agent = factory.create_agent("confluence_jira_analyst", mock_config, mock_api_key)
            
            # Test data
            data = {
                "confluence_pages": [{"title": "Test", "content": "Test content"}],
                "jira_issues": [{"key": "TEST-1", "summary": "Test issue"}]
            }
            
            # Mock the LLM response
            with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
                mock_response.return_value = "Test analysis result"
                
                # Test that agent can process data
                result = await agent.process(data)
                assert isinstance(result, str)
                assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_full_code_generation_workflow(self, mock_api_key, mock_config):
        """Test complete code generation workflow."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value=mock_api_key):
            agent = factory.create_agent("code_generator", mock_config, mock_api_key)
            
            # Mock the LLM response
            with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
                mock_response.return_value = "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
                
                # Test that agent can process code generation request
                result = await agent.process({
                    "task_description": "Generate a function to calculate factorial",
                    "code_type": "function",
                    "requirements": ["recursive", "input validation"]
                })
                assert isinstance(result, str)
                assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_full_idea_evaluation_workflow(self, mock_api_key, mock_config):
        """Test complete idea evaluation workflow."""
        factory = TaskSpecificAgentFactory()
        
        with patch('agents.task_specific_agents.get_api_key', return_value=mock_api_key):
            agent = factory.create_agent("idea_evaluator", mock_config, mock_api_key)
            
            # Mock the LLM response
            with patch.object(agent, '_generate_response', new_callable=AsyncMock) as mock_response:
                mock_response.return_value = "Idea evaluation: High feasibility, good market potential"
                
                # Test that agent can process idea evaluation request
                result = await agent.process({
                    "idea_title": "AI-Powered Code Review Assistant",
                    "idea_description": "An AI tool that automatically reviews code changes",
                    "evaluation_criteria": ["feasibility", "market_potential", "technical_complexity"]
                })
                assert isinstance(result, str)
                assert len(result) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 