# AI Model Router

An intelligent routing system that analyzes prompts and routes them to the most appropriate AI model based on complexity, capabilities, and cost considerations.

## Features

- **Intelligent Prompt Analysis**: Uses a light router model to analyze prompts and determine requirements
- **Model Selection**: Routes to appropriate models based on capabilities, complexity, and limitations
- **Cost Optimization**: Considers token costs and response times in routing decisions
- **Modular Design**: Easy to add custom models and map them to complexity thresholds
- **Flexible Configuration**: Support for user-defined models with custom capabilities
- **Routing History**: Tracks routing decisions for analytics and optimization

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Quick Start

### Basic Usage

```python
import asyncio
from model_router import ModelRouter

async def main():
    # Initialize router
    router = ModelRouter("your_openai_api_key")
    
    # Route a prompt
    result = await router.route_prompt("Write a Python function to sort a list")
    
    print(f"Selected Model: {result['selected_model']}")
    print(f"Routing Decision: {result['routing_decision']}")

asyncio.run(main())
```

### Using Custom Models

```python
import asyncio
from model_router import ModelRouter, CustomModel, ModelCapability, ComplexityLevel
from model_factory import ModelFactory

async def main():
    # Create custom models
    custom_models = {
        "my-fast-model": ModelFactory.create_fast_model("My Fast Model", "fast-v1"),
        "my-expert-model": ModelFactory.create_expert_model("My Expert Model", "expert-v1")
    }
    
    # Initialize router with custom models
    router = ModelRouter("your_openai_api_key", custom_models)
    
    # Route a prompt
    result = await router.route_prompt("Complex algorithm implementation")
    print(f"Selected Model: {result['selected_model']}")
    print(f"Routing Decision: {result['routing_decision']}")

asyncio.run(main())
```

## How It Works

1. **Prompt Analysis**: The router analyzes the input prompt to determine:
   - Required capabilities (text generation, code generation, analysis, etc.)
   - Complexity level (low, medium, high, expert)
   - Estimated token count
   - Priority requirements (speed, accuracy, cost)

2. **Model Selection**: Based on the analysis, the router selects the most appropriate model considering:
   - Model capabilities and limitations
   - Token limits
   - Cost per token
   - Response time
   - Complexity handling

3. **Routing Decision**: Returns a routing decision string like "high", "medium", or "low" based on the analysis

## Model Configurations

### Default Models

The router comes pre-configured with several models:

- **GPT-3.5 Turbo**: Fast and efficient for most tasks
- **GPT-4**: Most capable model for complex tasks
- **GPT-4 Turbo**: High capacity and speed

### Custom Models

You can easily add your own models with custom capabilities and complexity thresholds:

```python
# Create a custom model
custom_model = CustomModel(
    name="My Custom Model",
    model_id="custom-v1",
    provider="my-provider",
    max_tokens=4096,
    capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.CODE_GENERATION],
    complexity_threshold=ComplexityLevel.HIGH,
    cost_per_token=0.001,
    response_time_ms=1500,
    description="My specialized model"
)

# Add to router
router.add_model("my-custom", custom_model)
```

### Model Factory

Use the ModelFactory for common model configurations:

```python
from model_factory import ModelFactory

# Create fast model
fast_model = ModelFactory.create_fast_model("Fast Model", "fast-v1")

# Create expert model
expert_model = ModelFactory.create_expert_model("Expert Model", "expert-v1")

# Create specialized model
specialized_model = ModelFactory.create_specialized_model(
    name="Creative Model",
    model_id="creative-v1",
    capabilities=[ModelCapability.CREATIVE_WRITING],
    complexity_threshold=ComplexityLevel.HIGH
)
```

## Example Usage

```python
# Run the basic example demonstration
python example_usage.py

# Run the custom models example
python custom_models_example.py
```

## Configuration

Customize the router by modifying `config.py`:

- Add new models
- Adjust cost thresholds
- Modify performance settings
- Set complexity thresholds

## API Reference

### ModelRouter

Main router class for prompt routing.

#### Methods

- `route_prompt(prompt: str) -> Dict[str, Any]`: Route a prompt to the appropriate model
- `get_routing_stats() -> Dict[str, Any]`: Get routing statistics

### PromptAnalyzer

Analyzes prompts to determine routing requirements.

#### Methods

- `analyze_prompt(prompt: str) -> Dict[str, Any]`: Analyze a prompt and return requirements

## Routing Logic

The router uses the following logic:

1. **Capability Matching**: Ensures the selected model has all required capabilities
2. **Complexity Handling**: Ensures the model can handle the complexity level
3. **Token Limits**: Checks that the estimated tokens don't exceed model limits
4. **Priority Optimization**: Selects based on speed, accuracy, or cost priority

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
