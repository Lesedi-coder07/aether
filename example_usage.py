"""
Example usage of the AI Model Router
"""

import asyncio
import os
from model_router import ModelRouter
from config import Config


async def demonstrate_router():
    """Demonstrate the model router with various prompt types"""
    
    # Check configuration
    if not Config.validate_config():
        print("Please set your OPENAI_API_KEY in the environment")
        return
    
    # Initialize router
    router = ModelRouter(Config.OPENAI_API_KEY)
    
    # Test cases with different complexity levels
    test_cases = [
        {
            "name": "Simple Question",
            "prompt": "What is the capital of France?",
            "expected_complexity": "low"
        },
        {
            "name": "Code Generation",
            "prompt": "Write a Python function to implement quicksort algorithm with detailed comments",
            "expected_complexity": "high"
        },
        {
            "name": "Creative Writing",
            "prompt": "Write a short story about a robot learning to feel emotions",
            "expected_complexity": "medium"
        },
        {
            "name": "Technical Analysis",
            "prompt": "Analyze the time complexity of this algorithm and suggest optimizations: [complex algorithm code]",
            "expected_complexity": "expert"
        },
        {
            "name": "Translation Task",
            "prompt": "Translate this technical document from English to Spanish: [long technical text]",
            "expected_complexity": "medium"
        }
    ]
    
    print("AI Model Router Demonstration")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Prompt: {test_case['prompt'][:100]}{'...' if len(test_case['prompt']) > 100 else ''}")
        print(f"Expected Complexity: {test_case['expected_complexity']}")
        
        try:
            # Route the prompt
            result = await router.route_prompt(test_case['prompt'])
            
            # Display results
            print(f"\nRouting Results:")
            print(f"  Selected Model: {result['selected_model']}")
            print(f"  Routing Decision: {result['routing_decision']}")
            print(f"  Analyzed Complexity: {result['analysis']['complexity']}")
            print(f"  Required Capabilities: {', '.join(result['analysis']['capabilities'])}")
            print(f"  Estimated Tokens: {result['analysis']['estimated_tokens']}")
            print(f"  Priority: {result['analysis']['priority']}")
            print(f"  Reasoning: {result['analysis']['reasoning']}")
            
            # Show model details
            model_config = result['model_config']
            print(f"\nModel Details:")
            print(f"  Name: {model_config.name}")
            print(f"  Max Tokens: {model_config.limitations.max_tokens}")
            print(f"  Cost per Token: ${model_config.limitations.cost_per_token}")
            print(f"  Response Time: {model_config.limitations.response_time_ms}ms")
            print(f"  Description: {model_config.description}")
            
        except Exception as e:
            print(f"Error processing prompt: {str(e)}")
        
        print("\n" + "=" * 60)
    
    # Show overall statistics
    print("\nOverall Routing Statistics:")
    stats = router.get_routing_stats()
    print(f"Total Routes: {stats['total_routes']}")
    print(f"Decision Distribution: {stats['decision_distribution']}")
    print(f"Model Usage: {stats['model_usage']}")


async def test_custom_models():
    """Test the router with custom model configurations"""
    
    print("\n" + "=" * 60)
    print("Testing Custom Model Configurations")
    print("=" * 60)
    
    router = ModelRouter(Config.OPENAI_API_KEY)
    
    # Add a custom model configuration
    from model_router import ModelConfig, ModelLimitation, ModelCapability, ComplexityLevel
    
    custom_model = ModelConfig(
        name="Custom Fast Model",
        model_id="custom-fast",
        provider="custom",
        limitations=ModelLimitation(
            max_tokens=2048,
            capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.SUMMARIZATION],
            complexity_threshold=ComplexityLevel.MEDIUM,
            cost_per_token=0.0001,
            response_time_ms=500
        ),
        description="Fast, cheap model for simple tasks"
    )
    
    # Add to router's model list
    router.models["custom-fast"] = custom_model
    
    # Test with a simple prompt
    simple_prompt = "Summarize this text: [sample text]"
    result = await router.route_prompt(simple_prompt)
    
    print(f"Custom Model Test:")
    print(f"Selected Model: {result['selected_model']}")
    print(f"Routing Decision: {result['routing_decision']}")


async def main():
    """Main function to run all demonstrations"""
    await demonstrate_router()
    await test_custom_models()


if __name__ == "__main__":
    asyncio.run(main())
