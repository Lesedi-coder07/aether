"""
Example showing how to use custom models with the AI Model Router
"""

import asyncio
from model_router import ModelRouter, CustomModel, ModelCapability, ComplexityLevel


class MyCustomModel(CustomModel):
    """Example custom model implementation"""
    
    def __init__(self, name: str, model_id: str, provider: str, 
                 max_tokens: int, capabilities: list,
                 complexity_threshold: ComplexityLevel, cost_per_token: float,
                 response_time_ms: int, description: str = ""):
        super().__init__(name, model_id, provider, max_tokens, capabilities,
                        complexity_threshold, cost_per_token, response_time_ms, description)
    
    def can_handle_complexity(self, complexity: ComplexityLevel) -> bool:
        """Custom complexity handling logic"""
        # Example: This model can handle any complexity but prefers high-complexity tasks
        return True


async def demonstrate_custom_models():
    """Demonstrate using custom models with the router"""
    
    # Create custom models
    custom_models = {
        "my-fast-model": MyCustomModel(
            name="My Fast Model",
            model_id="fast-model-v1",
            provider="custom",
            max_tokens=2048,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.SUMMARIZATION,
                ModelCapability.QUESTION_ANSWERING
            ],
            complexity_threshold=ComplexityLevel.MEDIUM,
            cost_per_token=0.0001,
            response_time_ms=500,
            description="Fast, cheap model for simple tasks"
        ),
        
        "my-expert-model": MyCustomModel(
            name="My Expert Model",
            model_id="expert-model-v1",
            provider="custom",
            max_tokens=16384,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.ANALYSIS,
                ModelCapability.TECHNICAL_WRITING,
                ModelCapability.QUESTION_ANSWERING
            ],
            complexity_threshold=ComplexityLevel.EXPERT,
            cost_per_token=0.002,
            response_time_ms=3000,
            description="Expert model for complex tasks"
        ),
        
        "my-creative-model": MyCustomModel(
            name="My Creative Model",
            model_id="creative-model-v1",
            provider="custom",
            max_tokens=4096,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.TRANSLATION
            ],
            complexity_threshold=ComplexityLevel.HIGH,
            cost_per_token=0.0008,
            response_time_ms=1500,
            description="Specialized for creative writing tasks"
        )
    }
    
    # Initialize router with custom models
    router = ModelRouter("your_openai_api_key", custom_models)
    
    print("Custom Models Router Demonstration")
    print("=" * 50)
    
    # Show available models
    print("\nAvailable Models:")
    for model_name, model in router.get_available_models().items():
        info = router.get_model_info(model_name)
        print(f"  {model_name}: {info['name']} - {info['description']}")
        print(f"    Complexity: {info['complexity_threshold']}, Cost: ${info['cost_per_token']}, Time: {info['response_time_ms']}ms")
    
    # Test prompts with different complexity levels
    test_prompts = [
        {
            "prompt": "What is 2+2?",
            "expected": "Should route to fast model"
        },
        {
            "prompt": "Write a creative short story about a robot learning to dream",
            "expected": "Should route to creative model"
        },
        {
            "prompt": "Implement a distributed consensus algorithm with fault tolerance",
            "expected": "Should route to expert model"
        }
    ]
    
    print("\n" + "=" * 50)
    print("Testing Custom Model Routing")
    print("=" * 50)
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\nTest {i}: {test['prompt']}")
        print(f"Expected: {test['expected']}")
        print("-" * 30)
        
        try:
            result = await router.route_prompt(test['prompt'])
            
            print(f"Selected Model: {result['selected_model']}")
            print(f"Routing Decision: {result['routing_decision']}")
            print(f"Complexity: {result['analysis']['complexity']}")
            print(f"Capabilities: {', '.join(result['analysis']['capabilities'])}")
            print(f"Model Info: {result['model_info']['name']} - {result['model_info']['description']}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Show routing statistics
    print("\n" + "=" * 50)
    print("Routing Statistics:")
    stats = router.get_routing_stats()
    print(f"Total routes: {stats['total_routes']}")
    print(f"Decision distribution: {stats['decision_distribution']}")
    print(f"Model usage: {stats['model_usage']}")


async def demonstrate_dynamic_model_management():
    """Demonstrate adding/removing models dynamically"""
    
    print("\n" + "=" * 50)
    print("Dynamic Model Management")
    print("=" * 50)
    
    # Start with basic router
    router = ModelRouter("your_openai_api_key")
    
    print("Initial models:", list(router.get_available_models().keys()))
    
    # Add a new model dynamically
    new_model = CustomModel(
        name="Dynamic Model",
        model_id="dynamic-v1",
        provider="custom",
        max_tokens=8192,
        capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.ANALYSIS],
        complexity_threshold=ComplexityLevel.HIGH,
        cost_per_token=0.001,
        response_time_ms=1000,
        description="Dynamically added model"
    )
    
    router.add_model("dynamic-model", new_model)
    print("After adding dynamic model:", list(router.get_available_models().keys()))
    
    # Test routing with new model
    result = await router.route_prompt("Analyze this data and provide insights")
    print(f"Selected model: {result['selected_model']}")
    
    # Remove a model
    removed = router.remove_model("gpt-3.5-turbo")
    print(f"Removed gpt-3.5-turbo: {removed}")
    print("After removal:", list(router.get_available_models().keys()))


async def demonstrate_complexity_mapping():
    """Demonstrate how complexity thresholds work with custom models"""
    
    print("\n" + "=" * 50)
    print("Complexity Threshold Mapping")
    print("=" * 50)
    
    # Create models with different complexity thresholds
    complexity_models = {
        "low-specialist": CustomModel(
            name="Low Complexity Specialist",
            model_id="low-spec-v1",
            provider="custom",
            max_tokens=1024,
            capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.QUESTION_ANSWERING],
            complexity_threshold=ComplexityLevel.LOW,
            cost_per_token=0.0001,
            response_time_ms=200,
            description="Specialized for low complexity tasks"
        ),
        
        "medium-specialist": CustomModel(
            name="Medium Complexity Specialist",
            model_id="medium-spec-v1",
            provider="custom",
            max_tokens=4096,
            capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.ANALYSIS, ModelCapability.CREATIVE_WRITING],
            complexity_threshold=ComplexityLevel.MEDIUM,
            cost_per_token=0.0005,
            response_time_ms=800,
            description="Specialized for medium complexity tasks"
        ),
        
        "high-specialist": CustomModel(
            name="High Complexity Specialist",
            model_id="high-spec-v1",
            provider="custom",
            max_tokens=8192,
            capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.CODE_GENERATION, ModelCapability.ANALYSIS],
            complexity_threshold=ComplexityLevel.HIGH,
            cost_per_token=0.001,
            response_time_ms=1500,
            description="Specialized for high complexity tasks"
        )
    }
    
    router = ModelRouter("your_openai_api_key", complexity_models)
    
    # Test different complexity levels
    complexity_tests = [
        ("What is the weather?", "low"),
        ("Write a poem about coding", "medium"),
        ("Implement a machine learning algorithm", "high")
    ]
    
    for prompt, expected_complexity in complexity_tests:
        print(f"\nTesting: {prompt}")
        print(f"Expected complexity: {expected_complexity}")
        
        result = await router.route_prompt(prompt)
        print(f"Selected model: {result['selected_model']}")
        print(f"Analyzed complexity: {result['analysis']['complexity']}")
        print(f"Model complexity threshold: {result['model_info']['complexity_threshold']}")


async def main():
    """Run all demonstrations"""
    await demonstrate_custom_models()
    await demonstrate_dynamic_model_management()
    await demonstrate_complexity_mapping()


if __name__ == "__main__":
    asyncio.run(main())
