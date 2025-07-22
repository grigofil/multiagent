#!/usr/bin/env python3
"""
Example: Idea Evaluation and Filtering
Demonstrates the IdeaEvaluationAgent for evaluating, scoring, and filtering ideas.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.task_specific_agents import IdeaEvaluationAgent, TaskSpecificAgentFactory
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import json
from typing import List, Dict, Any

console = Console()

class IdeaEvaluationExample:
    """Example demonstrating idea evaluation and filtering."""
    
    def __init__(self):
        self.console = Console()
        self.factory = TaskSpecificAgentFactory()
        
    async def run_demo(self):
        """Run the complete idea evaluation demo."""
        self.console.print(Panel.fit(
            "[bold blue]Idea Evaluation and Filtering Demo[/bold blue]\n"
            "Demonstrating AI-powered idea evaluation, scoring, and filtering",
            border_style="blue"
        ))
        
        # Create the idea evaluation agent
        agent = await self.factory.create_agent("idea_evaluation")
        
        # Example 1: Evaluate individual ideas
        await self.example_evaluate_ideas(agent)
        
        # Example 2: Compare multiple ideas
        await self.example_compare_ideas(agent)
        
        # Example 3: Filter ideas by criteria
        await self.example_filter_ideas(agent)
        
        # Example 4: Generate recommendations
        await self.example_generate_recommendations(agent)
        
        self.console.print("\n[bold green]✓ Idea Evaluation Demo Completed![/bold green]")
    
    async def example_evaluate_ideas(self, agent: IdeaEvaluationAgent):
        """Example: Evaluate individual ideas."""
        self.console.print("\n[bold cyan]Example 1: Individual Idea Evaluation[/bold cyan]")
        
        # Sample ideas to evaluate
        ideas = [
            {
                "title": "AI-Powered Code Review Assistant",
                "description": "An AI tool that automatically reviews code changes, identifies potential bugs, suggests improvements, and ensures code quality standards.",
                "category": "Development Tools",
                "target_audience": "Software Developers",
                "estimated_effort": "6 months",
                "budget_required": "$50,000"
            },
            {
                "title": "Smart Home Energy Management System",
                "description": "IoT-based system that optimizes home energy consumption using machine learning, reducing bills by 30% while maintaining comfort.",
                "category": "IoT/Smart Home",
                "target_audience": "Homeowners",
                "estimated_effort": "12 months",
                "budget_required": "$200,000"
            },
            {
                "title": "Virtual Reality Training Platform",
                "description": "VR platform for employee training in hazardous environments, reducing training costs and improving safety outcomes.",
                "category": "Education/Training",
                "target_audience": "Corporate Training Departments",
                "estimated_effort": "18 months",
                "budget_required": "$500,000"
            }
        ]
        
        for i, idea in enumerate(ideas, 1):
            self.console.print(f"\n[bold yellow]Evaluating Idea {i}: {idea['title']}[/bold yellow]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Evaluating idea...", total=None)
                
                evaluation = await agent.evaluate_idea(idea)
                progress.update(task, completed=True)
            
            if evaluation.success:
                self.display_idea_evaluation(evaluation, idea)
            else:
                self.console.print(f"[red]Error evaluating idea: {evaluation.error}[/red]")
    
    async def example_compare_ideas(self, agent: IdeaEvaluationAgent):
        """Example: Compare multiple ideas."""
        self.console.print("\n[bold cyan]Example 2: Idea Comparison[/bold cyan]")
        
        # Sample ideas for comparison
        ideas = [
            {
                "title": "Mobile App for Local Business Discovery",
                "description": "App that helps users discover local businesses with reviews, ratings, and special offers.",
                "category": "Mobile App",
                "target_audience": "General Consumers",
                "estimated_effort": "8 months",
                "budget_required": "$100,000"
            },
            {
                "title": "SaaS Platform for Project Management",
                "description": "Cloud-based project management tool with collaboration features, time tracking, and reporting.",
                "category": "SaaS",
                "target_audience": "Small to Medium Businesses",
                "estimated_effort": "10 months",
                "budget_required": "$150,000"
            },
            {
                "title": "E-commerce Marketplace for Artisans",
                "description": "Online marketplace connecting local artisans with customers, featuring handmade products.",
                "category": "E-commerce",
                "target_audience": "Artisans and Craft Enthusiasts",
                "estimated_effort": "12 months",
                "budget_required": "$200,000"
            }
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Comparing ideas...", total=None)
            
            comparison = await agent.compare_ideas(ideas)
            progress.update(task, completed=True)
        
        if comparison.success:
            self.display_idea_comparison(comparison, ideas)
        else:
            self.console.print(f"[red]Error comparing ideas: {comparison.error}[/red]")
    
    async def example_filter_ideas(self, agent: IdeaEvaluationAgent):
        """Example: Filter ideas by criteria."""
        self.console.print("\n[bold cyan]Example 3: Idea Filtering[/bold cyan]")
        
        # Sample ideas for filtering
        ideas = [
            {
                "title": "AI Chatbot for Customer Support",
                "description": "Intelligent chatbot that handles customer inquiries 24/7, reducing support costs.",
                "category": "AI/Customer Service",
                "target_audience": "E-commerce Businesses",
                "estimated_effort": "4 months",
                "budget_required": "$75,000"
            },
            {
                "title": "Blockchain-based Supply Chain Tracker",
                "description": "Transparent supply chain tracking system using blockchain technology.",
                "category": "Blockchain",
                "target_audience": "Manufacturing Companies",
                "estimated_effort": "15 months",
                "budget_required": "$300,000"
            },
            {
                "title": "Fitness Tracking Wearable",
                "description": "Smart wearable device with health monitoring and fitness tracking capabilities.",
                "category": "Hardware/Wearables",
                "target_audience": "Fitness Enthusiasts",
                "estimated_effort": "20 months",
                "budget_required": "$800,000"
            },
            {
                "title": "Online Learning Platform",
                "description": "Platform for creating and selling online courses with interactive features.",
                "category": "EdTech",
                "target_audience": "Educators and Students",
                "estimated_effort": "9 months",
                "budget_required": "$120,000"
            }
        ]
        
        # Filter criteria
        filter_criteria = {
            "max_budget": 200000,
            "max_effort_months": 12,
            "min_feasibility_score": 7.0,
            "categories": ["AI/Customer Service", "EdTech", "Mobile App"],
            "target_audience": ["E-commerce Businesses", "Educators and Students"]
        }
        
        self.console.print(Panel(
            f"[bold]Filter Criteria:[/bold]\n"
            f"Max Budget: ${filter_criteria['max_budget']:,}\n"
            f"Max Effort: {filter_criteria['max_effort_months']} months\n"
            f"Min Feasibility Score: {filter_criteria['min_feasibility_score']}\n"
            f"Categories: {', '.join(filter_criteria['categories'])}\n"
            f"Target Audience: {', '.join(filter_criteria['target_audience'])}",
            title="[bold blue]Filtering Criteria[/bold blue]",
            border_style="blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Filtering ideas...", total=None)
            
            filtered_result = await agent.filter_ideas(ideas, filter_criteria)
            progress.update(task, completed=True)
        
        if filtered_result.success:
            self.display_filtered_ideas(filtered_result, ideas)
        else:
            self.console.print(f"[red]Error filtering ideas: {filtered_result.error}[/red]")
    
    async def example_generate_recommendations(self, agent: IdeaEvaluationAgent):
        """Example: Generate recommendations based on idea analysis."""
        self.console.print("\n[bold cyan]Example 4: Recommendation Generation[/bold cyan]")
        
        # Context for recommendations
        context = {
            "company_profile": "Tech startup with 10 employees, $500K funding",
            "team_expertise": ["Python", "JavaScript", "Machine Learning", "Web Development"],
            "market_focus": "B2B SaaS solutions",
            "timeline": "12-18 months",
            "budget_constraints": "$200K maximum",
            "risk_tolerance": "Medium"
        }
        
        self.console.print(Panel(
            f"[bold]Company Context:[/bold]\n"
            f"Profile: {context['company_profile']}\n"
            f"Expertise: {', '.join(context['team_expertise'])}\n"
            f"Market Focus: {context['market_focus']}\n"
            f"Timeline: {context['timeline']}\n"
            f"Budget: {context['budget_constraints']}\n"
            f"Risk Tolerance: {context['risk_tolerance']}",
            title="[bold blue]Company Context[/bold blue]",
            border_style="blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Generating recommendations...", total=None)
            
            recommendations = await agent.generate_recommendations(context)
            progress.update(task, completed=True)
        
        if recommendations.success:
            self.display_recommendations(recommendations)
        else:
            self.console.print(f"[red]Error generating recommendations: {recommendations.error}[/red]")
    
    def display_idea_evaluation(self, evaluation, idea):
        """Display individual idea evaluation results."""
        # Create evaluation table
        table = Table(title=f"Evaluation Results: {idea['title']}")
        table.add_column("Criteria", style="cyan", no_wrap=True)
        table.add_column("Score", style="magenta")
        table.add_column("Weight", style="blue")
        table.add_column("Weighted Score", style="green")
        
        total_score = 0
        for criterion, score in evaluation.scores.items():
            weight = evaluation.weights.get(criterion, 1.0)
            weighted_score = score * weight
            total_score += weighted_score
            
            table.add_row(
                criterion,
                f"{score:.2f}",
                f"{weight:.2f}",
                f"{weighted_score:.2f}"
            )
        
        table.add_row("", "", "[bold]Total[/bold]", f"[bold]{total_score:.2f}[/bold]")
        self.console.print(table)
        
        # Display insights
        if evaluation.insights:
            self.console.print("\n[bold yellow]Key Insights:[/bold yellow]")
            for insight in evaluation.insights:
                self.console.print(f"• {insight}")
        
        # Display recommendations
        if evaluation.recommendations:
            self.console.print("\n[bold green]Recommendations:[/bold green]")
            for rec in evaluation.recommendations:
                self.console.print(f"• {rec}")
    
    def display_idea_comparison(self, comparison, ideas):
        """Display idea comparison results."""
        # Create comparison table
        table = Table(title="Idea Comparison Results")
        table.add_column("Idea", style="cyan", no_wrap=True)
        table.add_column("Overall Score", style="magenta")
        table.add_column("Rank", style="green")
        table.add_column("Strengths", style="white")
        table.add_column("Weaknesses", style="white")
        
        for i, result in enumerate(comparison.comparison_results, 1):
            idea_title = ideas[i-1]['title']
            strengths = ", ".join(result.strengths[:2]) if result.strengths else "N/A"
            weaknesses = ", ".join(result.weaknesses[:2]) if result.weaknesses else "N/A"
            
            table.add_row(
                idea_title,
                f"{result.overall_score:.2f}",
                str(result.rank),
                strengths,
                weaknesses
            )
        
        self.console.print(table)
        
        # Display ranking
        self.console.print("\n[bold blue]Final Ranking:[/bold blue]")
        for i, result in enumerate(comparison.comparison_results, 1):
            idea_title = ideas[result.rank-1]['title']
            self.console.print(f"{i}. {idea_title} (Score: {result.overall_score:.2f})")
    
    def display_filtered_ideas(self, filtered_result, original_ideas):
        """Display filtered ideas results."""
        if not filtered_result.filtered_ideas:
            self.console.print("[yellow]No ideas match the filter criteria.[/yellow]")
            return
        
        table = Table(title="Filtered Ideas")
        table.add_column("Idea", style="cyan", no_wrap=True)
        table.add_column("Category", style="blue")
        table.add_column("Budget", style="magenta")
        table.add_column("Effort", style="green")
        table.add_column("Feasibility Score", style="yellow")
        
        for idea_result in filtered_result.filtered_ideas:
            original_idea = next((idea for idea in original_ideas if idea['title'] == idea_result.title), None)
            if original_idea:
                table.add_row(
                    idea_result.title,
                    original_idea['category'],
                    original_idea['budget_required'],
                    original_idea['estimated_effort'],
                    f"{idea_result.feasibility_score:.2f}"
                )
        
        self.console.print(table)
        
        self.console.print(f"\n[bold green]Found {len(filtered_result.filtered_ideas)} ideas matching criteria[/bold green]")
    
    def display_recommendations(self, recommendations):
        """Display generated recommendations."""
        if not recommendations.recommendations:
            self.console.print("[yellow]No recommendations generated.[/yellow]")
            return
        
        for i, rec in enumerate(recommendations.recommendations, 1):
            self.console.print(Panel(
                f"[bold]{rec.title}[/bold]\n\n"
                f"[italic]{rec.description}[/italic]\n\n"
                f"[bold]Priority:[/bold] {rec.priority}\n"
                f"[bold]Estimated Effort:[/bold] {rec.estimated_effort}\n"
                f"[bold]Expected ROI:[/bold] {rec.expected_roi}\n\n"
                f"[bold]Key Benefits:[/bold]\n" + "\n".join(f"• {benefit}" for benefit in rec.key_benefits),
                title=f"[bold blue]Recommendation {i}[/bold blue]",
                border_style="blue"
            ))

async def main():
    """Main function to run the idea evaluation example."""
    example = IdeaEvaluationExample()
    
    try:
        await example.run_demo()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error running demo: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 