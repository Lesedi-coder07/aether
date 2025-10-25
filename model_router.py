"""
AI Model Router - Routes prompts to appropriate models based on analysis
"""

from typing import Dict, List, Optional, Any, Protocol, Union
from enum import Enum
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import json
import os
from dotenv import load_dotenv

load_dotenv()


class ModelCapability(Enum):
    """Model capabilities for routing decisions"""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    CREATIVE_WRITING = "creative_writing"
    TECHNICAL_WRITING = "technical_writing"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    QUESTION_ANSWERING = "question_answering"


class ComplexityLevel(Enum):
    """Complexity levels for routing"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXPERT = "expert"


class ModelInterface(Protocol):
    """Protocol for model implementations"""
    def get_capabilities(self) -> List[ModelCapability]:
        """Return list of model capabilities"""
        ...
    
    def get_max_tokens(self) -> int:
        """Return maximum tokens supported"""
        ...
    
    def get_cost_per_token(self) -> float:
        """Return cost per token"""
        ...
    
    def get_response_time_ms(self) -> int:
        """Return expected response time in milliseconds"""
        ...
    
    def can_handle_complexity(self, complexity: ComplexityLevel) -> bool:
        """Check if model can handle given complexity level"""
        ...


@dataclass
class ModelLimitation:
    """Defines limitations for a model"""
    max_tokens: int
    capabilities: List[ModelCapability]
    complexity_threshold: ComplexityLevel
    cost_per_token: float
    response_time_ms: int


@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    name: str
    model_id: str
    provider: str
    limitations: ModelLimitation
    description: str


class CustomModel:
    """Base class for custom model implementations"""
    
    def __init__(self, name: str, model_id: str, provider: str, 
                 max_tokens: int, capabilities: List[ModelCapability],
                 complexity_threshold: ComplexityLevel, cost_per_token: float,
                 response_time_ms: int, description: str = ""):
        self.name = name
        self.model_id = model_id
        self.provider = provider
        self.max_tokens = max_tokens
        self.capabilities = capabilities
        self.complexity_threshold = complexity_threshold
        self.cost_per_token = cost_per_token
        self.response_time_ms = response_time_ms
        self.description = description
    
    def get_capabilities(self) -> List[ModelCapability]:
        return self.capabilities
    
    def get_max_tokens(self) -> int:
        return self.max_tokens
    
    def get_cost_per_token(self) -> float:
        return self.cost_per_token
    
    def get_response_time_ms(self) -> int:
        return self.response_time_ms
    
    def can_handle_complexity(self, complexity: ComplexityLevel) -> bool:
        complexity_order = {
            ComplexityLevel.LOW: 1,
            ComplexityLevel.MEDIUM: 2,
            ComplexityLevel.HIGH: 3,
            ComplexityLevel.EXPERT: 4
        }
        return complexity_order[self.complexity_threshold] >= complexity_order[complexity]


class PromptAnalyzer:
    """Analyzes prompts to determine routing requirements"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=openai_api_key,
            temperature=0.1
        )
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a prompt analyzer for an AI model router. 
            Analyze the given prompt and determine:
            1. Required capabilities (text_generation, code_generation, analysis, creative_writing, technical_writing, translation, summarization, question_answering)
            2. Complexity level (low, medium, high, expert)
            3. Estimated token count
            4. Priority requirements (speed, accuracy, cost)
            
            Respond with a JSON object containing:
            {
                "capabilities": ["capability1", "capability2"],
                "complexity": "low|medium|high|expert",
                "estimated_tokens": number,
                "priority": "speed|accuracy|cost",
                "reasoning": "brief explanation"
            }"""),
            ("human", "{prompt}")
        ])
    
    async def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze a prompt and return routing requirements"""
        try:
            response = await self.llm.ainvoke(
                self.analysis_prompt.format_messages(prompt=prompt)
            )
            
            # Parse JSON response
            analysis = json.loads(response.content)
            return analysis
        except Exception as e:
            # Fallback analysis
            return {
                "capabilities": ["text_generation"],
                "complexity": "medium",
                "estimated_tokens": len(prompt.split()) * 2,
                "priority": "accuracy",
                "reasoning": f"Fallback analysis due to error: {str(e)}"
            }


class ModelRouter:
    """Main router class that routes prompts to appropriate models"""
    
    def __init__(self, openai_api_key: str, custom_models: Optional[Dict[str, ModelInterface]] = None):
        self.analyzer = PromptAnalyzer(openai_api_key)
        self.models = self._initialize_models()
        
        # Add custom models if provided
        if custom_models:
            self.add_custom_models(custom_models)
        
        self.routing_history = []
    
    def _initialize_models(self) -> Dict[str, ModelInterface]:
        """Initialize default models with their configurations"""
        return {
            "gpt-3.5-turbo": CustomModel(
                name="GPT-3.5 Turbo",
                model_id="gpt-3.5-turbo",
                provider="openai",
                max_tokens=4096,
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.CREATIVE_WRITING,
                    ModelCapability.TECHNICAL_WRITING,
                    ModelCapability.TRANSLATION,
                    ModelCapability.SUMMARIZATION,
                    ModelCapability.QUESTION_ANSWERING
                ],
                complexity_threshold=ComplexityLevel.HIGH,
                cost_per_token=0.0005,
                response_time_ms=2000,
                description="Fast and efficient for most tasks"
            ),
            
            "gpt-4": CustomModel(
                name="GPT-4",
                model_id="gpt-4",
                provider="openai",
                max_tokens=8192,
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.CREATIVE_WRITING,
                    ModelCapability.TECHNICAL_WRITING,
                    ModelCapability.TRANSLATION,
                    ModelCapability.SUMMARIZATION,
                    ModelCapability.QUESTION_ANSWERING
                ],
                complexity_threshold=ComplexityLevel.EXPERT,
                cost_per_token=0.03,
                response_time_ms=5000,
                description="Most capable model"
            ),
            
            "gpt-4-turbo": CustomModel(
                name="GPT-4 Turbo",
                model_id="gpt-4-turbo-preview",
                provider="openai",
                max_tokens=128000,
                capabilities=[
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CODE_GENERATION,
                    ModelCapability.ANALYSIS,
                    ModelCapability.CREATIVE_WRITING,
                    ModelCapability.TECHNICAL_WRITING,
                    ModelCapability.TRANSLATION,
                    ModelCapability.SUMMARIZATION,
                    ModelCapability.QUESTION_ANSWERING
                ],
                complexity_threshold=ComplexityLevel.EXPERT,
                cost_per_token=0.01,
                response_time_ms=3000,
                description="High capacity and speed"
            )
        }
    
    def add_custom_models(self, custom_models: Dict[str, ModelInterface]) -> None:
        """Add custom models to the router"""
        for model_name, model in custom_models.items():
            self.models[model_name] = model
    
    def add_model(self, name: str, model: ModelInterface) -> None:
        """Add a single custom model"""
        self.models[name] = model
    
    def remove_model(self, name: str) -> bool:
        """Remove a model from the router"""
        if name in self.models:
            del self.models[name]
            return True
        return False
    
    def _select_model(self, analysis: Dict[str, Any]) -> str:
        """Select the best model based on analysis"""
        required_capabilities = [ModelCapability(cap) for cap in analysis["capabilities"]]
        complexity = ComplexityLevel(analysis["complexity"])
        estimated_tokens = analysis["estimated_tokens"]
        priority = analysis["priority"]
        
        # Filter models that meet requirements
        suitable_models = []
        
        for model_name, model in self.models.items():
            # Check if model has required capabilities
            has_capabilities = all(
                cap in model.get_capabilities() 
                for cap in required_capabilities
            )
            
            # Check if model can handle complexity
            can_handle_complexity = model.can_handle_complexity(complexity)
            
            # Check token limit
            within_token_limit = estimated_tokens <= model.get_max_tokens()
            
            if has_capabilities and can_handle_complexity and within_token_limit:
                suitable_models.append((model_name, model))
        
        if not suitable_models:
            # Fallback to most capable model
            return "gpt-4"
        
        # Select based on priority
        if priority == "speed":
            suitable_models.sort(key=lambda x: x[1].get_response_time_ms())
        elif priority == "cost":
            suitable_models.sort(key=lambda x: x[1].get_cost_per_token())
        else:  # accuracy
            suitable_models.sort(key=lambda x: x[1].complexity_threshold.value, reverse=True)
        
        return suitable_models[0][0]
    
    def get_available_models(self) -> Dict[str, ModelInterface]:
        """Get all available models"""
        return self.models.copy()
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        return {
            "name": model.name,
            "model_id": model.model_id,
            "provider": model.provider,
            "max_tokens": model.get_max_tokens(),
            "capabilities": [cap.value for cap in model.get_capabilities()],
            "complexity_threshold": model.complexity_threshold.value,
            "cost_per_token": model.get_cost_per_token(),
            "response_time_ms": model.get_response_time_ms(),
            "description": model.description
        }
    
    async def route_prompt(self, prompt: str) -> Dict[str, Any]:
        """Route a prompt to the appropriate model"""
        # Analyze the prompt
        analysis = await self.analyzer.analyze_prompt(prompt)
        
        # Select the best model
        selected_model = self._select_model(analysis)
        
        # Create routing result
        routing_result = {
            "prompt": prompt,
            "analysis": analysis,
            "selected_model": selected_model,
            "model_info": self.get_model_info(selected_model),
            "routing_decision": self._get_routing_decision(analysis, selected_model)
        }
        
        # Store in history
        self.routing_history.append(routing_result)
        
        return routing_result
    
    def _get_routing_decision(self, analysis: Dict[str, Any], selected_model: str) -> str:
        """Generate a human-readable routing decision"""
        complexity = analysis["complexity"]
        capabilities = ", ".join(analysis["capabilities"])
        
        if complexity == "high" or complexity == "expert":
            return "high"
        elif complexity == "medium":
            return "medium"
        else:
            return "low"
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions"""
        if not self.routing_history:
            return {"total_routes": 0}
        
        decisions = [route["routing_decision"] for route in self.routing_history]
        model_usage = [route["selected_model"] for route in self.routing_history]
        
        return {
            "total_routes": len(self.routing_history),
            "decision_distribution": {
                decision: decisions.count(decision) 
                for decision in set(decisions)
            },
            "model_usage": {
                model: model_usage.count(model) 
                for model in set(model_usage)
            }
        }


# Example usage and testing
async def main():
   
    # Initialize router
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    router = ModelRouter(api_key)
    
    # Test prompts
    test_prompts = [
        "What is the weather like today?",
        "Write a complex machine learning algorithm in Python",
        "Explain quantum computing principles",
        "Translate 'Hello world' to Spanish",
        "Create a detailed business plan for a tech startup"
    ]
    
    print("AI Model Router - Testing")
    print("=" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: {prompt}")
        print("-" * 30)
        
        try:
            result = await router.route_prompt(prompt)
            
            print(f"Analysis: {result['analysis']['reasoning']}")
            print(f"Selected Model: {result['selected_model']}")
            print(f"Routing Decision: {result['routing_decision']}")
            print(f"Complexity: {result['analysis']['complexity']}")
            print(f"Capabilities: {', '.join(result['analysis']['capabilities'])}")
            
        except Exception as e:
            print(f"Error routing prompt: {str(e)}")
    
    # Show routing statistics
    print("\n" + "=" * 50)
    print("Routing Statistics:")
    stats = router.get_routing_stats()
    print(f"Total routes: {stats['total_routes']}")
    print(f"Decision distribution: {stats['decision_distribution']}")
    print(f"Model usage: {stats['model_usage']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
