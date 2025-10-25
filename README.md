# Aether

A Fast AI Model Router for Modern AI Agents

Aether is an open-source intelligent routing system that analyzes prompts and routes them to the most appropriate AI model based on complexity, capabilities, and cost considerations. Built for modern AI agents that need fast, intelligent model selection.

## Features

- **Lightning Fast Routing**: Ultra-fast prompt analysis and model selection
- **Intelligent Prompt Analysis**: Uses a lightweight router model to analyze prompts and determine requirements
- **Smart Model Selection**: Routes to appropriate models based on capabilities, complexity, and limitations
- **Cost Optimization**: Considers token costs and response times in routing decisions
- **Modular Design**: Easy to add custom models and map them to complexity thresholds
- **Agent-Ready**: Built specifically for modern AI agents and workflows
- **Open Source**: Fully open source with MIT license
- **Routing History**: Tracks routing decisions for analytics and optimization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/aether.git
cd aether
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Quick Start

### Basic Usage

```python
import asyncio
from model_router import ModelRouter

async def main():
    # Initialize Aether router
    router = ModelRouter("your_openai_api_key")
    
    # Route a prompt - Aether will automatically select the best model
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
    # Create custom models for your AI agents
    custom_models = {
        "agent-fast": ModelFactory.create_fast_model("Agent Fast Model", "fast-v1"),
        "agent-expert": ModelFactory.create_expert_model("Agent Expert Model", "expert-v1")
    }
    
    # Initialize Aether with custom models
    router = ModelRouter("your_openai_api_key", custom_models)
    
    # Route a prompt - Aether intelligently selects the best model
    result = await router.route_prompt("Complex algorithm implementation")
    print(f"Selected Model: {result['selected_model']}")
    print(f"Routing Decision: {result['routing_decision']}")

asyncio.run(main())
```

## How Aether Works

1. **Lightning-Fast Analysis**: Aether analyzes the input prompt in milliseconds to determine:
   - Required capabilities (text generation, code generation, analysis, etc.)
   - Complexity level (low, medium, high, expert)
   - Estimated token count
   - Priority requirements (speed, accuracy, cost)

2. **Intelligent Model Selection**: Based on the analysis, Aether selects the most appropriate model considering:
   - Model capabilities and limitations
   - Token limits
   - Cost per token
   - Response time
   - Complexity handling

3. **Smart Routing Decision**: Returns a routing decision string like "high", "medium", or "low" based on the analysis

## Why Aether?

- **Built for AI Agents**: Designed specifically for modern AI agent workflows
- **Open Source**: Fully open source with MIT license
- **Lightning Fast**: Ultra-fast routing decisions for real-time agent responses
- **Cost Effective**: Optimizes costs by selecting the most appropriate model
- **Modular**: Easy to extend with custom models and capabilities

## Model Configurations

### Default Models

Aether comes pre-configured with several models:

- **GPT-3.5 Turbo**: Fast and efficient for most tasks
- **GPT-4**: Most capable model for complex tasks
- **GPT-4 Turbo**: High capacity and speed

### Custom Models

You can easily add your own models with custom capabilities and complexity thresholds:

```python
# Create a custom model for your AI agents
custom_model = CustomModel(
    name="My Agent Model",
    model_id="agent-v1",
    provider="my-provider",
    max_tokens=4096,
    capabilities=[ModelCapability.TEXT_GENERATION, ModelCapability.CODE_GENERATION],
    complexity_threshold=ComplexityLevel.HIGH,
    cost_per_token=0.001,
    response_time_ms=1500,
    description="My specialized agent model"
)

# Add to Aether router
router.add_model("my-agent-model", custom_model)
```

### Model Factory

Use the ModelFactory for common model configurations:

```python
from model_factory import ModelFactory

# Create fast model for simple agent tasks
fast_model = ModelFactory.create_fast_model("Agent Fast Model", "fast-v1")

# Create expert model for complex agent tasks
expert_model = ModelFactory.create_expert_model("Agent Expert Model", "expert-v1")

# Create specialized model for specific agent capabilities
specialized_model = ModelFactory.create_specialized_model(
    name="Agent Creative Model",
    model_id="creative-v1",
    capabilities=[ModelCapability.CREATIVE_WRITING],
    complexity_threshold=ComplexityLevel.HIGH
)
```

## Example Usage

```python
# Run the basic Aether demonstration
python example_usage.py

# Run the custom models example for AI agents
python custom_models_example.py
```

## Configuration

Customize Aether by modifying `config.py`:

- Add new models for your AI agents
- Adjust cost thresholds
- Modify performance settings
- Set complexity thresholds

## API Reference

### ModelRouter

Main Aether router class for prompt routing.

#### Methods

- `route_prompt(prompt: str) -> Dict[str, Any]`: Route a prompt to the appropriate model
- `get_routing_stats() -> Dict[str, Any]`: Get routing statistics
- `add_model(name: str, model: ModelInterface)`: Add a custom model
- `remove_model(name: str)`: Remove a model
- `get_available_models() -> Dict[str, ModelInterface]`: Get all available models

### PromptAnalyzer

Analyzes prompts to determine routing requirements.

#### Methods

- `analyze_prompt(prompt: str) -> Dict[str, Any]`: Analyze a prompt and return requirements

## Routing Logic

Aether uses the following intelligent routing logic:

1. **Capability Matching**: Ensures the selected model has all required capabilities
2. **Complexity Handling**: Ensures the model can handle the complexity level
3. **Token Limits**: Checks that the estimated tokens don't exceed model limits
4. **Priority Optimization**: Selects based on speed, accuracy, or cost priority
5. **Agent Optimization**: Optimized for AI agent workflows and real-time responses

## Contributing

We welcome contributions to Aether! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - Aether is open source and free to use for your AI agents and projects.
