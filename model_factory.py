"""
Model Factory - Helper functions for creating custom models easily
"""

from typing import Dict, List, Optional
from model_router import CustomModel, ModelCapability, ComplexityLevel


class ModelFactory:
    """Factory class for creating custom models with common configurations"""
    
    @staticmethod
    def create_fast_model(name: str, model_id: str, provider: str = "custom",
                        max_tokens: int = 2048, cost_per_token: float = 0.0001,
                        response_time_ms: int = 500) -> CustomModel:
        """Create a fast, cheap model for simple tasks"""
        return CustomModel(
            name=name,
            model_id=model_id,
            provider=provider,
            max_tokens=max_tokens,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.SUMMARIZATION,
                ModelCapability.QUESTION_ANSWERING
            ],
            complexity_threshold=ComplexityLevel.LOW,
            cost_per_token=cost_per_token,
            response_time_ms=response_time_ms,
            description="Fast, cheap model for simple tasks"
        )
    
    @staticmethod
    def create_balanced_model(name: str, model_id: str, provider: str = "custom",
                            max_tokens: int = 4096, cost_per_token: float = 0.0005,
                            response_time_ms: int = 1500) -> CustomModel:
        """Create a balanced model for medium complexity tasks"""
        return CustomModel(
            name=name,
            model_id=model_id,
            provider=provider,
            max_tokens=max_tokens,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.ANALYSIS,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.TECHNICAL_WRITING,
                ModelCapability.SUMMARIZATION,
                ModelCapability.QUESTION_ANSWERING
            ],
            complexity_threshold=ComplexityLevel.MEDIUM,
            cost_per_token=cost_per_token,
            response_time_ms=response_time_ms,
            description="Balanced model for medium complexity tasks"
        )
    
    @staticmethod
    def create_expert_model(name: str, model_id: str, provider: str = "custom",
                          max_tokens: int = 8192, cost_per_token: float = 0.002,
                          response_time_ms: int = 3000) -> CustomModel:
        """Create an expert model for complex tasks"""
        return CustomModel(
            name=name,
            model_id=model_id,
            provider=provider,
            max_tokens=max_tokens,
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
            cost_per_token=cost_per_token,
            response_time_ms=response_time_ms,
            description="Expert model for complex tasks"
        )
    
    @staticmethod
    def create_specialized_model(name: str, model_id: str, capabilities: List[ModelCapability],
                               complexity_threshold: ComplexityLevel, provider: str = "custom",
                               max_tokens: int = 4096, cost_per_token: float = 0.001,
                               response_time_ms: int = 2000, description: str = "") -> CustomModel:
        """Create a specialized model with custom capabilities"""
        return CustomModel(
            name=name,
            model_id=model_id,
            provider=provider,
            max_tokens=max_tokens,
            capabilities=capabilities,
            complexity_threshold=complexity_threshold,
            cost_per_token=cost_per_token,
            response_time_ms=response_time_ms,
            description=description or f"Specialized model for {', '.join([cap.value for cap in capabilities])}"
        )
    
    @staticmethod
    def create_model_from_config(config: Dict) -> CustomModel:
        """Create a model from a configuration dictionary"""
        return CustomModel(
            name=config["name"],
            model_id=config["model_id"],
            provider=config.get("provider", "custom"),
            max_tokens=config["max_tokens"],
            capabilities=[ModelCapability(cap) for cap in config["capabilities"]],
            complexity_threshold=ComplexityLevel(config["complexity_threshold"]),
            cost_per_token=config["cost_per_token"],
            response_time_ms=config["response_time_ms"],
            description=config.get("description", "")
        )
    
    @staticmethod
    def create_models_from_configs(configs: List[Dict]) -> Dict[str, CustomModel]:
        """Create multiple models from configuration dictionaries"""
        models = {}
        for config in configs:
            model = ModelFactory.create_model_from_config(config)
            models[config["model_id"]] = model
        return models


# Predefined model configurations
PREDEFINED_CONFIGS = {
    "fast-text": {
        "name": "Fast Text Model",
        "model_id": "fast-text-v1",
        "provider": "custom",
        "max_tokens": 2048,
        "capabilities": ["text_generation", "summarization", "question_answering"],
        "complexity_threshold": "low",
        "cost_per_token": 0.0001,
        "response_time_ms": 500,
        "description": "Fast model for text tasks"
    },
    
    "creative-writer": {
        "name": "Creative Writer Model",
        "model_id": "creative-writer-v1",
        "provider": "custom",
        "max_tokens": 4096,
        "capabilities": ["text_generation", "creative_writing", "translation"],
        "complexity_threshold": "high",
        "cost_per_token": 0.0008,
        "response_time_ms": 1500,
        "description": "Specialized for creative writing"
    },
    
    "code-expert": {
        "name": "Code Expert Model",
        "model_id": "code-expert-v1",
        "provider": "custom",
        "max_tokens": 8192,
        "capabilities": ["code_generation", "analysis", "technical_writing"],
        "complexity_threshold": "expert",
        "cost_per_token": 0.002,
        "response_time_ms": 2500,
        "description": "Expert model for coding tasks"
    },
    
    "multilingual": {
        "name": "Multilingual Model",
        "model_id": "multilingual-v1",
        "provider": "custom",
        "max_tokens": 4096,
        "capabilities": ["text_generation", "translation", "summarization"],
        "complexity_threshold": "medium",
        "cost_per_token": 0.0006,
        "response_time_ms": 1200,
        "description": "Specialized for multilingual tasks"
    }
}


def get_predefined_models() -> Dict[str, CustomModel]:
    """Get predefined model configurations"""
    return ModelFactory.create_models_from_configs(list(PREDEFINED_CONFIGS.values()))


# Example usage
if __name__ == "__main__":
    # Create models using factory methods
    fast_model = ModelFactory.create_fast_model("My Fast Model", "fast-v1")
    expert_model = ModelFactory.create_expert_model("My Expert Model", "expert-v1")
    
    # Create specialized model
    creative_model = ModelFactory.create_specialized_model(
        name="Creative Model",
        model_id="creative-v1",
        capabilities=[ModelCapability.CREATIVE_WRITING, ModelCapability.TEXT_GENERATION],
        complexity_threshold=ComplexityLevel.HIGH,
        description="Specialized for creative tasks"
    )
    
    # Create from predefined configs
    predefined_models = get_predefined_models()
    
    print("Created models:")
    for name, model in predefined_models.items():
        print(f"  {name}: {model.name} - {model.description}")
