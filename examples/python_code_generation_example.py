#!/usr/bin/env python3
"""
Example: Python Code Generation and Validation
Demonstrates the CodeGenerationAgent for generating, validating, and improving Python code.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.task_specific_agents import CodeGenerationAgent, TaskSpecificAgentFactory
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
import json

console = Console()

class CodeGenerationExample:
    """Example demonstrating Python code generation and validation."""
    
    def __init__(self):
        self.console = Console()
        self.factory = TaskSpecificAgentFactory()
        
    async def run_demo(self):
        """Run the complete code generation demo."""
        self.console.print(Panel.fit(
            "[bold blue]Python Code Generation and Validation Demo[/bold blue]\n"
            "Demonstrating AI-powered code generation, validation, and improvement",
            border_style="blue"
        ))
        
        # Create the code generation agent
        agent = await self.factory.create_agent("code_generation")
        
        # Example 1: Generate a simple function
        await self.example_generate_function(agent)
        
        # Example 2: Generate a class with methods
        await self.example_generate_class(agent)
        
        # Example 3: Code validation and improvement
        await self.example_validate_and_improve(agent)
        
        # Example 4: Generate test code
        await self.example_generate_tests(agent)
        
        self.console.print("\n[bold green]✓ Code Generation Demo Completed![/bold green]")
    
    async def example_generate_function(self, agent: CodeGenerationAgent):
        """Example: Generate a simple function."""
        self.console.print("\n[bold cyan]Example 1: Function Generation[/bold cyan]")
        
        prompt = """
        Generate a Python function that:
        - Takes a list of numbers as input
        - Returns the sum of all even numbers in the list
        - Includes proper type hints
        - Has a docstring explaining the function
        - Handles edge cases (empty list, no even numbers)
        """
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Generating function...", total=None)
            
            result = await agent.generate_code(prompt)
            progress.update(task, completed=True)
        
        if result.success:
            self.console.print(Panel(
                Syntax(result.generated_code, "python", theme="monokai"),
                title="[bold green]Generated Function[/bold green]",
                border_style="green"
            ))
            
            # Validate the generated code
            validation = await agent.validate_code(result.generated_code)
            self.display_validation_results(validation)
        else:
            self.console.print(f"[red]Error generating code: {result.error}[/red]")
    
    async def example_generate_class(self, agent: CodeGenerationAgent):
        """Example: Generate a class with methods."""
        self.console.print("\n[bold cyan]Example 2: Class Generation[/bold cyan]")
        
        prompt = """
        Generate a Python class called 'DataProcessor' that:
        - Has methods to load, process, and save data
        - Uses proper error handling
        - Includes type hints
        - Has comprehensive docstrings
        - Follows PEP 8 style guidelines
        """
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Generating class...", total=None)
            
            result = await agent.generate_code(prompt)
            progress.update(task, completed=True)
        
        if result.success:
            self.console.print(Panel(
                Syntax(result.generated_code, "python", theme="monokai"),
                title="[bold green]Generated Class[/bold green]",
                border_style="green"
            ))
            
            # Validate the generated code
            validation = await agent.validate_code(result.generated_code)
            self.display_validation_results(validation)
        else:
            self.console.print(f"[red]Error generating code: {result.error}[/red]")
    
    async def example_validate_and_improve(self, agent: CodeGenerationAgent):
        """Example: Validate and improve existing code."""
        self.console.print("\n[bold cyan]Example 3: Code Validation and Improvement[/bold cyan]")
        
        # Sample code with issues
        sample_code = '''
def calculate_average(numbers):
    total=0
    count=0
    for num in numbers:
        total+=num
        count+=1
    return total/count

def process_data(data_list):
    result=[]
    for item in data_list:
        if item>0:
            result.append(item*2)
    return result
        '''
        
        self.console.print(Panel(
            Syntax(sample_code, "python", theme="monokai"),
            title="[bold yellow]Original Code (with issues)[/bold yellow]",
            border_style="yellow"
        ))
        
        # Validate the code
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Validating code...", total=None)
            
            validation = await agent.validate_code(sample_code)
            progress.update(task, completed=True)
        
        self.display_validation_results(validation)
        
        # Improve the code
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Improving code...", total=None)
            
            improvement = await agent.improve_code(sample_code, "Fix PEP 8 issues, add type hints, and improve error handling")
            progress.update(task, completed=True)
        
        if improvement.success:
            self.console.print(Panel(
                Syntax(improvement.improved_code, "python", theme="monokai"),
                title="[bold green]Improved Code[/bold green]",
                border_style="green"
            ))
            
            # Validate the improved code
            improved_validation = await agent.validate_code(improvement.improved_code)
            self.display_validation_results(improved_validation, "Improved Code Validation")
        else:
            self.console.print(f"[red]Error improving code: {improvement.error}[/red]")
    
    async def example_generate_tests(self, agent: CodeGenerationAgent):
        """Example: Generate test code."""
        self.console.print("\n[bold cyan]Example 4: Test Code Generation[/bold cyan]")
        
        # Sample function to test
        function_to_test = '''
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
        '''
        
        self.console.print(Panel(
            Syntax(function_to_test, "python", theme="monokai"),
            title="[bold blue]Function to Test[/bold blue]",
            border_style="blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Generating tests...", total=None)
            
            result = await agent.generate_test_code(function_to_test, "pytest")
            progress.update(task, completed=True)
        
        if result.success:
            self.console.print(Panel(
                Syntax(result.test_code, "python", theme="monokai"),
                title="[bold green]Generated Test Code[/bold green]",
                border_style="green"
            ))
        else:
            self.console.print(f"[red]Error generating tests: {result.error}[/red]")
    
    def display_validation_results(self, validation, title="Code Validation Results"):
        """Display code validation results in a formatted table."""
        table = Table(title=title)
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Score", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Details", style="white")
        
        # Add validation metrics
        for metric, value in validation.metrics.items():
            if isinstance(value, (int, float)):
                score = f"{value:.2f}"
                status = "✅" if value >= 8.0 else "⚠️" if value >= 6.0 else "❌"
            else:
                score = str(value)
                status = "✅" if value else "❌"
            
            details = validation.details.get(metric, "")
            table.add_row(metric, score, status, details)
        
        self.console.print(table)
        
        # Display suggestions if any
        if validation.suggestions:
            self.console.print("\n[bold yellow]Improvement Suggestions:[/bold yellow]")
            for i, suggestion in enumerate(validation.suggestions, 1):
                self.console.print(f"{i}. {suggestion}")

async def main():
    """Main function to run the code generation example."""
    example = CodeGenerationExample()
    
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