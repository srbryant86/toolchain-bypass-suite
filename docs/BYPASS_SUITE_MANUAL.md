# Toolchain Bypass Suite - Complete Manual

## Overview

The Toolchain Bypass Suite is a comprehensive collection of tools designed to extend AI capabilities beyond sandbox limitations, featuring OptiStack integration, self-repair mechanisms, and risk management systems.

## Table of Contents

1. [Installation](#installation)
2. [Components Overview](#components-overview)
3. [OptiStack Integration](#optistack-integration)
4. [Self-Repair Systems](#self-repair-systems)
5. [Risk Management](#risk-management)
6. [Usage Examples](#usage-examples)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [API Reference](#api-reference)

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Unity 2021.3+ (for Unity integration)
- Godot 4.0+ (for Godot integration)

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd toolchain-bypass-suite

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (if needed)
npm install

# Setup configuration
cp configs/config_template.json configs/config.json
# Edit configs/config.json with your API keys and settings
```

### Component Installation

Each component can be installed independently:

```bash
# GPT API Bridge
cd gpt-api-bridge
pip install -r requirements.txt

# External I/O Layer
cd external-io-layer
pip install -r requirements.txt

# Monetization Kit
cd monetization-kit
pip install -r requirements.txt

# 3D Engine Linkers
cd 3d-engine-linkers
pip install -r requirements.txt

# Prefab Generator
cd prefab-generator
pip install -r requirements.txt
```

## Components Overview

### 1. GPT API Bridge (`gpt-api-bridge/`)

**Purpose**: Provides webhook module and rate-limited GPT-4 access with fallback logic.

**Key Features**:
- Real OpenAI API integration
- Rate limiting and throttling
- Automatic fallback to GPT-3.5-turbo
- Webhook server for external integration
- Error handling and retry logic

**Main Files**:
- `openai_connector.py` - Core GPT integration
- `webhook_server.py` - HTTP webhook interface

### 2. External I/O Boundary Layer (`external-io-layer/`)

**Purpose**: Provides file system interfaces and deployment protocols for external integration.

**Key Features**:
- Mountable sandbox paths
- Real-time file synchronization
- Automated deployment to Vercel/Netlify
- File system watchers
- External file injection

**Main Files**:
- `file_system_bridge.py` - Core I/O operations
- `deployment_manager.py` - Deployment automation

### 3. Monetization Integration Kit (`monetization-kit/`)

**Purpose**: Complete OptiStack integration with payment processing and value optimization.

**Key Features**:
- **OptiX-Gate**: Value threshold system (T40-T100 tiers)
- **OptiMAX**: Perpetual optimization enforcement
- **OptiLev**: Leverage optimization for every asset
- **OptiStack**: Genesis system for all optimizations
- Stripe/PayPal integration
- Automated pricing optimization

**Main Files**:
- `payment_integration.py` - Complete OptiStack + payments
- `pricing_optimizer.py` - Dynamic pricing algorithms

### 4. 3D Engine Linkers (`3d-engine-linkers/`)

**Purpose**: Unity and Godot integration with self-repair and risk management.

**Key Features**:
- **Risk Assessment Matrix**: Comprehensive risk evaluation
- **Self-Repair Systems**: Automatic error detection and fixing
- **Unity Integration**: Direct Unity project manipulation
- **Godot Integration**: Godot project automation
- **Asset Injection**: Automated asset generation and placement

**Main Files**:
- `unity_connector.py` - Unity integration with self-repair
- `godot_connector.py` - Godot integration
- `risk_matrix.py` - Risk assessment and mitigation

### 5. Prefab Generator (`prefab-generator/`)

**Purpose**: CLI automation tools with priority queues and batch processing.

**Key Features**:
- **Priority Task Queue**: Multi-priority task processing
- **Batch Job Processing**: Handle multiple tasks simultaneously
- **Self-Repair CLI**: Automatic error diagnosis and repair
- **OptiStack Integration**: Value-driven generation
- **Performance Monitoring**: Real-time metrics and optimization

**Main Files**:
- `cli_prefab_injector.py` - Main CLI interface
- `task_queue.py` - Priority-based task management
- `batch_processor.py` - Batch job handling

## OptiStack Integration

### OptiX-Gate (Value Threshold System)

OptiX-Gate prevents low-value generation by enforcing value thresholds:

- **T40-T60**: $1.25M minimum value threshold
- **T61-T80**: $1.7M minimum value threshold  
- **T81-T100**: $2.6M minimum value threshold

```python
from monetization_kit.payment_integration import OptiXGate

gate = OptiXGate()
result = gate.gate_check({
    "ai_integration": True,
    "automation_level": 0.9,
    "scalability": True,
    "uniqueness": 0.8,
    "monetization_potential": 0.85
})

if result["passed"]:
    print(f"System approved for tier: {result['tier']}")
    print(f"Estimated value: ${result['estimated_value']:,.2f}")
else:
    print(f"System blocked: {result['reason']}")
```

### OptiMAX (Perpetual Optimization)

OptiMAX automatically applies logic-grade optimizations:

```python
from monetization_kit.payment_integration import OptiMAX

optimax = OptiMAX()
optimized_system = optimax.apply_optimization({
    "performance_config": {},
    "code_standards": {},
    "architecture": {},
    "monetization": {}
})

print(f"Optimization score improved to: {optimax._calculate_quality_score(optimized_system)}")
```

### OptiLev (Leverage Optimization)

OptiLev optimizes leverage for maximum asymmetric returns:

```python
from monetization_kit.payment_integration import OptiLev

optilev = OptiLev()
leveraged_asset = optilev.optimize_leverage({
    "automation": 0.8,
    "scalability": 0.9,
    "network_effects": 0.7,
    "ai_leverage": 0.95
})

print(f"Total leverage score: {leveraged_asset['total_leverage_score']}")
```

### Complete OptiStack Processing

```python
from monetization_kit.payment_integration import OptiStack, OptiStackConfig

config = OptiStackConfig(
    optix_gate_enabled=True,
    optimax_enabled=True,
    optilev_enabled=True,
    perpetual_optimization=True
)

optistack = OptiStack(config)

result = optistack.process_system({
    "ai_integration": True,
    "automation_level": 0.95,
    "scalability": True,
    "uniqueness": 0.9,
    "monetization_potential": 0.85
})

if result["status"] == "optimized":
    print(f"System optimized successfully!")
    print(f"Estimated value: ${result['estimated_value']:,.2f}")
    print(f"Optimizations applied: {result['optimizations_applied']}")
else:
    print(f"System blocked: {result['reason']}")
```

## Self-Repair Systems

### Risk Assessment Matrix

Every operation is assessed for risk and assigned mitigation strategies:

```python
from 3d_engine_linkers.unity_connector import OptiGateRiskMatrix, ModuleTier

risk_matrix = OptiGateRiskMatrix()
risks = risk_matrix.assess_risk("unity_generation", ModuleTier.T61_T80)

for risk in risks:
    print(f"Risk: {risk.risk_id}")
    print(f"Level: {risk.risk_level.value}")
    print(f"Probability: {risk.probability}")
    print(f"Impact: {risk.impact_score}")
    print(f"Mitigation: {risk.mitigation_strategy}")
```

### Automatic Self-Repair

Systems automatically detect and repair issues:

```python
from 3d_engine_linkers.unity_connector import SelfRepairSystem, OptiGateRiskMatrix

project_path = "/path/to/unity/project"
risk_matrix = OptiGateRiskMatrix()
self_repair = SelfRepairSystem(project_path, risk_matrix)

# Start continuous monitoring
self_repair.start_monitoring()

# Manual health check
validation_results = self_repair.validator.validate_project()
if validation_results["overall_health"] != "healthy":
    self_repair._trigger_auto_repair(validation_results)
```

### CLI Self-Repair

The CLI system includes automatic error diagnosis and repair:

```python
from prefab_generator.cli_prefab_injector import SelfRepairCLI

repair_cli = SelfRepairCLI()

# Diagnose error
diagnosis = repair_cli.diagnose_error(
    "FileNotFoundError: No such file or directory",
    {"missing_path": "/path/to/file", "is_directory": False}
)

# Attempt repair
if diagnosis:
    success = repair_cli.attempt_repair(diagnosis)
    print(f"Repair {'successful' if success else 'failed'}")
```

## Risk Management

### Risk Levels and Mitigation

The system categorizes risks into four levels:

1. **LOW**: Minor issues with minimal impact
2. **MEDIUM**: Moderate issues requiring attention
3. **HIGH**: Serious issues requiring immediate action
4. **CRITICAL**: System-threatening issues requiring emergency response

### Mitigation Strategies

Each risk type has specific mitigation strategies:

- **automatic_backup_and_validation**: Create backups before operations
- **syntax_validation_and_auto_fix**: Validate and fix code syntax
- **dependency_tracking_and_repair**: Track and repair broken dependencies
- **performance_monitoring_and_optimization**: Monitor and optimize performance
- **redundant_build_systems**: Multiple build pipelines with failover
- **circuit_breaker_and_timeout**: Prevent infinite loops and timeouts

### Risk Assessment Example

```python
from 3d_engine_linkers.unity_connector import OptiGateRiskMatrix, ModuleTier

risk_matrix = OptiGateRiskMatrix()

# Assess risks for Unity project generation
risks = risk_matrix.assess_risk("unity_generation", ModuleTier.T81_T100)
overall_risk = risk_matrix.calculate_overall_risk_score(risks)

print(f"Overall risk score: {overall_risk}/10")

for risk in risks:
    print(f"\nRisk: {risk.description}")
    print(f"Probability: {risk.probability * 100}%")
    print(f"Impact: {risk.impact_score}/10")
    print(f"Mitigation: {risk.mitigation_strategy}")
```

## Usage Examples

### 1. GPT API Integration

```python
from gpt_api_bridge.openai_connector import GPTAPIBridge, APIConfig

config = APIConfig(
    openai_api_key="your-api-key",
    model="gpt-4",
    rate_limit_rpm=60
)

bridge = GPTAPIBridge(config)

result = bridge.send_message(
    "Generate a Unity script for player movement",
    "You are a Unity game development expert"
)

if result["status"] == "success":
    print(result["response"])
else:
    print(f"Error: {result['error']}")
```

### 2. File System Operations

```python
from external_io_layer.file_system_bridge import FileSystemBridge

bridge = FileSystemBridge()

# Deploy project
result = bridge.deploy_project("/path/to/project", "vercel")
print(f"Deployment result: {result}")

# Inject external files
result = bridge.inject_external_files(
    "/external/assets", 
    "/home/ubuntu/projects"
)
print(f"Injection result: {result}")
```

### 3. Unity Project Generation

```python
from 3d_engine_linkers.unity_connector import UnityConnector

connector = UnityConnector("/path/to/unity/project", {})

# Start monitoring
connector.start_continuous_monitoring()

# Generate system
system_spec = {
    "module_tier": "T61-T80",
    "scripts": [{
        "name": "PlayerController",
        "base_class": "MonoBehaviour",
        "init_logic": "// Initialize player",
        "update_logic": "// Handle input"
    }]
}

result = connector.generate_unity_system(system_spec)
print(f"Generation status: {result['generation_status']}")
```

### 4. CLI Batch Processing

```bash
# Create batch job from file
python cli_prefab_injector.py --batch-file batch_job.json --priority high

# Check status
python cli_prefab_injector.py --status job_12345678

# Show system metrics
python cli_prefab_injector.py --metrics

# Start as daemon
python cli_prefab_injector.py --start-daemon
```

### 5. Complete Workflow Example

```python
from monetization_kit.payment_integration import OptiStack, OptiStackConfig
from 3d_engine_linkers.unity_connector import UnityConnector
from prefab_generator.cli_prefab_injector import CLIPrefabInjector

# Initialize OptiStack
config = OptiStackConfig(optix_gate_enabled=True, optimax_enabled=True)
optistack = OptiStack(config)

# Process system through OptiStack
system_spec = {
    "ai_integration": True,
    "automation_level": 0.9,
    "scalability": True,
    "monetization_potential": 0.8
}

opti_result = optistack.process_system(system_spec)

if opti_result["status"] == "optimized":
    # Generate Unity system
    connector = UnityConnector("/path/to/project", {})
    unity_result = connector.generate_unity_system(opti_result["optimized_spec"])
    
    # Create CLI tasks
    injector = CLIPrefabInjector()
    task_id = injector.create_task("generate_prefab", {
        "name": "OptimizedPrefab",
        "components": ["PlayerController"]
    })
    
    print(f"Complete workflow executed successfully!")
    print(f"OptiStack value: ${opti_result['estimated_value']:,.2f}")
    print(f"Unity generation: {unity_result['generation_status']}")
    print(f"CLI task: {task_id}")
```

## Configuration

### Main Configuration File (`configs/config.json`)

```json
{
  "gpt_api_bridge": {
    "openai_api_key": "your-openai-api-key",
    "model": "gpt-4",
    "rate_limit_rpm": 60,
    "webhook_port": 5000
  },
  "external_io": {
    "sandbox_mount_paths": [
      "/home/ubuntu/projects",
      "/home/ubuntu/assets"
    ],
    "deployment": {
      "auto_deploy": true,
      "target_platforms": ["vercel", "netlify"]
    }
  },
  "monetization": {
    "stripe": {
      "publishable_key": "pk_test_...",
      "secret_key": "sk_test_..."
    },
    "pricing_tiers": {
      "basic": {"price": 99, "features": ["basic_ai"]},
      "pro": {"price": 299, "features": ["advanced_ai"]},
      "enterprise": {"price": 999, "features": ["unlimited_ai"]}
    }
  },
  "3d_engines": {
    "unity": {
      "project_template_path": "/templates/unity",
      "build_targets": ["Windows", "Mac", "Linux"]
    }
  },
  "automation": {
    "prefab_generator": {
      "max_workers": 4,
      "batch_size": 10
    }
  }
}
```

### Environment Variables

```bash
# API Keys
export OPENAI_API_KEY="your-openai-api-key"
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_PUBLISHABLE_KEY="pk_test_..."

# Paths
export TOOLCHAIN_CONFIG_PATH="/path/to/config.json"
export TOOLCHAIN_OUTPUT_DIR="/path/to/output"

# OptiStack Settings
export OPTIX_GATE_ENABLED="true"
export OPTIMAX_ENABLED="true"
export OPTILEV_ENABLED="true"
```

## Troubleshooting

### Common Issues

#### 1. API Rate Limiting

**Problem**: Getting rate limit errors from OpenAI API

**Solution**:
```python
# Adjust rate limiting in config
config = APIConfig(
    openai_api_key="your-key",
    rate_limit_rpm=30  # Reduce from default 60
)
```

#### 2. File Permission Errors

**Problem**: Permission denied when accessing files

**Solution**:
```bash
# Fix permissions
chmod -R 755 /path/to/toolchain-bypass-suite
chown -R $USER:$USER /path/to/toolchain-bypass-suite
```

#### 3. Unity Project Corruption

**Problem**: Unity project becomes corrupted during generation

**Solution**: The system automatically detects and repairs this:
```python
# Manual repair trigger
from 3d_engine_linkers.unity_connector import SelfRepairSystem

repair_system = SelfRepairSystem("/path/to/project", risk_matrix)
repair_system._execute_repair_action("fix_unity_corruption")
```

#### 4. OptiX-Gate Blocking Generation

**Problem**: System value below threshold

**Solution**:
```python
# Check why system was blocked
gate_result = optix_gate.gate_check(system_spec)
print(f"Estimated value: ${gate_result['estimated_value']:,.2f}")
print(f"Minimum required: $1,250,000")

# Improve system specification
system_spec.update({
    "ai_integration": True,
    "automation_level": 0.95,
    "scalability": True,
    "uniqueness": 0.9,
    "monetization_potential": 0.9
})
```

### Debugging

#### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Check System Health

```python
from prefab_generator.cli_prefab_injector import CLIPrefabInjector

injector = CLIPrefabInjector()
metrics = injector.get_system_metrics()
print(f"System health: {metrics['system_health']}")
print(f"Error rate: {metrics['task_queue_metrics']['error_rate']}")
```

#### Validate Configuration

```python
from external_io_layer.file_system_bridge import FileSystemBridge

bridge = FileSystemBridge()
mount_info = bridge.get_mount_info()
print("Mount points:", mount_info)
```

## API Reference

### GPT API Bridge

#### `GPTAPIBridge`

```python
class GPTAPIBridge:
    def __init__(self, config: APIConfig)
    def send_message(self, message: str, system_prompt: str = None) -> Dict
```

#### `WebhookServer`

```python
class WebhookServer:
    def __init__(self, gpt_bridge: GPTAPIBridge, port: int = 5000)
    def run(self, debug=False)
```

### External I/O Layer

#### `FileSystemBridge`

```python
class FileSystemBridge:
    def __init__(self, config_path: str = None)
    def deploy_project(self, project_path: str, target_name: str = None) -> Dict
    def inject_external_files(self, external_path: str, target_mount: str) -> Dict
    def get_mount_info(self) -> Dict
```

### Monetization Kit

#### `OptiStack`

```python
class OptiStack:
    def __init__(self, config: OptiStackConfig)
    def process_system(self, system_spec: Dict) -> Dict
    def get_optistack_metrics(self) -> Dict
```

#### `OptiXGate`

```python
class OptiXGate:
    def __init__(self)
    def gate_check(self, system_spec: Dict) -> Dict
    def evaluate_value_threshold(self, estimated_value: float) -> Optional[ValueThreshold]
```

### 3D Engine Linkers

#### `UnityConnector`

```python
class UnityConnector:
    def __init__(self, project_path: str, config: Dict)
    def generate_unity_system(self, system_spec: Dict) -> Dict
    def start_continuous_monitoring(self)
    def get_system_health_report(self) -> Dict
```

### Prefab Generator

#### `CLIPrefabInjector`

```python
class CLIPrefabInjector:
    def __init__(self, config_path: Optional[str] = None)
    def create_task(self, task_type: str, spec: Dict, priority: TaskPriority) -> str
    def create_batch_job(self, name: str, tasks: List[Dict], priority: TaskPriority) -> str
    def get_system_metrics(self) -> Dict
```

## License

This software is proprietary and includes OptiStack integration. See LICENSE file for details.

## Support

For technical support and documentation updates, contact the development team.

---

**Toolchain Bypass Suite v1.0**  
*Extending AI capabilities beyond sandbox limitations*

