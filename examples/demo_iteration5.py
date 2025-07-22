#!/usr/bin/env python3
"""
Demo: Iteration #5 - Practical Usage Examples
Demonstrates the agent templates for specific tasks:
- Data analysis from Confluence/JIRA
- Python code generation and validation
- Idea evaluation and filtering
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
import json

# Import example classes
from examples.confluence_jira_analysis_example import ConfluenceJiraAnalysisExample
from examples.python_code_generation_example import CodeGenerationExample
from examples.idea_evaluation_example import IdeaEvaluationExample

console = Console()

class Iteration5Demo:
    """Demo class for Iteration #5 practical examples."""
    
    def __init__(self):
        self.console = Console()
        
    async def run_demo(self):
        """Run the complete Iteration #5 demo."""
        self.console.print(Panel.fit(
            "[bold blue]Iteration #5: Practical Usage Examples[/bold blue]\n"
            "Demonstrating agent templates for specific real-world tasks\n\n"
            "• Data analysis from Confluence/JIRA\n"
            "• Python code generation and validation\n"
            "• Idea evaluation and filtering",
            border_style="blue"
        ))
        
        # Show menu and get user choice
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                await self.run_confluence_jira_analysis()
            elif choice == "2":
                await self.run_code_generation()
            elif choice == "3":
                await self.run_idea_evaluation()
            elif choice == "4":
                await self.run_all_examples()
            elif choice == "5":
                self.console.print("\n[bold green]Demo completed![/bold green]")
                break
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")
            
            if choice != "5":
                self.console.print("\n" + "="*80)
    
    def show_menu(self):
        """Display the demo menu and get user choice."""
        self.console.print("\n[bold cyan]Available Examples:[/bold cyan]")
        
        table = Table(show_header=False, box=None)
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        table.add_row("1", "Confluence/JIRA Data Analysis")
        table.add_row("2", "Python Code Generation & Validation")
        table.add_row("3", "Idea Evaluation & Filtering")
        table.add_row("4", "Run All Examples")
        table.add_row("5", "Exit Demo")
        
        self.console.print(table)
        
        return Prompt.ask(
            "\n[bold yellow]Select an example to run[/bold yellow]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )
    
    async def run_confluence_jira_analysis(self):
        """Run the Confluence/JIRA analysis example."""
        self.console.print(Panel.fit(
            "[bold blue]Confluence/JIRA Data Analysis Example[/bold blue]\n"
            "Analyzing project data from Confluence and JIRA to extract insights",
            border_style="blue"
        ))
        
        try:
            example = ConfluenceJiraAnalysisExample()
            await example.run_demo()
        except Exception as e:
            self.console.print(f"[red]Error running Confluence/JIRA analysis: {e}[/red]")
    
    async def run_code_generation(self):
        """Run the Python code generation example."""
        self.console.print(Panel.fit(
            "[bold blue]Python Code Generation & Validation Example[/bold blue]\n"
            "Generating, validating, and improving Python code using AI agents",
            border_style="blue"
        ))
        
        try:
            example = CodeGenerationExample()
            await example.run_demo()
        except Exception as e:
            self.console.print(f"[red]Error running code generation: {e}[/red]")
    
    async def run_idea_evaluation(self):
        """Run the idea evaluation example."""
        self.console.print(Panel.fit(
            "[bold blue]Idea Evaluation & Filtering Example[/bold blue]\n"
            "Evaluating, scoring, and filtering business ideas using AI agents",
            border_style="blue"
        ))
        
        try:
            example = IdeaEvaluationExample()
            await example.run_demo()
        except Exception as e:
            self.console.print(f"[red]Error running idea evaluation: {e}[/red]")
    
    async def run_all_examples(self):
        """Run all examples in sequence."""
        self.console.print(Panel.fit(
            "[bold blue]Running All Examples[/bold blue]\n"
            "Executing all three practical examples in sequence",
            border_style="blue"
        ))
        
        examples = [
            ("Confluence/JIRA Analysis", self.run_confluence_jira_analysis),
            ("Code Generation", self.run_code_generation),
            ("Idea Evaluation", self.run_idea_evaluation)
        ]
        
        for i, (name, example_func) in enumerate(examples, 1):
            self.console.print(f"\n[bold cyan]Running Example {i}/3: {name}[/bold cyan]")
            self.console.print("="*60)
            
            try:
                await example_func()
                self.console.print(f"[bold green]✓ {name} completed successfully[/bold green]")
            except Exception as e:
                self.console.print(f"[red]✗ {name} failed: {e}[/red]")
            
            if i < len(examples):
                self.console.print("\n[bold yellow]Press Enter to continue to next example...[/bold yellow]")
                input()
        
        self.console.print("\n[bold green]✓ All examples completed![/bold green]")
    
    def show_iteration5_summary(self):
        """Show a summary of Iteration #5 features."""
        self.console.print(Panel.fit(
            "[bold blue]Iteration #5 Summary[/bold blue]\n\n"
            "[bold cyan]Key Features Implemented:[/bold cyan]\n"
            "• Specialized agents for domain-specific tasks\n"
            "• Practical examples with real-world use cases\n"
            "• Rich console interfaces with progress tracking\n"
            "• Comprehensive error handling and validation\n\n"
            "[bold cyan]Agent Types:[/bold cyan]\n"
            "• ConfluenceJiraAnalystAgent - Data analysis from project tools\n"
            "• CodeGenerationAgent - Python code generation and validation\n"
            "• IdeaEvaluationAgent - Business idea evaluation and filtering\n"
            "• ProjectManagementAgent - Project health analysis\n\n"
            "[bold cyan]Example Applications:[/bold cyan]\n"
            "• Extract insights from Confluence/JIRA data\n"
            "• Generate and validate Python code\n"
            "• Evaluate and rank business ideas\n"
            "• Generate project recommendations",
            border_style="blue"
        ))

async def main():
    """Main function to run the Iteration #5 demo."""
    demo = Iteration5Demo()
    
    try:
        # Show summary first
        demo.show_iteration5_summary()
        
        # Run the interactive demo
        await demo.run_demo()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error running demo: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 