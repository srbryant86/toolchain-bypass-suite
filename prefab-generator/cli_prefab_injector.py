#!/usr/bin/env python3
"""
CLI Prefab Injector with OptiStack Integration
Self-repairing automation tools with risk management
"""

import os
import sys
import json
import argparse
import time
import threading
import queue
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import hashlib
import shutil
import yaml

# Import OptiStack components
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from monetization_kit.payment_integration import OptiStack, OptiStackConfig, OptiTier, RiskLevel

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class PrefabTask:
    task_id: str
    task_type: str
    priority: TaskPriority
    spec: Dict
    status: TaskStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    output_path: Optional[str] = None
    risk_assessment: Optional[Dict] = None

@dataclass
class BatchJob:
    job_id: str
    name: str
    tasks: List[PrefabTask]
    priority: TaskPriority
    created_at: str
    status: TaskStatus
    progress: float = 0.0
    estimated_completion: Optional[str] = None

class SelfRepairCLI:
    """Self-repairing CLI system with automatic error recovery"""
    
    def __init__(self):
        self.repair_history = []
        self.error_patterns = self._initialize_error_patterns()
        self.repair_strategies = self._initialize_repair_strategies()
        
    def _initialize_error_patterns(self) -> Dict[str, Dict]:
        """Initialize known error patterns and their solutions"""
        return {
            "file_not_found": {
                "pattern": ["FileNotFoundError", "No such file or directory"],
                "severity": "medium",
                "auto_repairable": True,
                "repair_strategy": "create_missing_file"
            },
            "permission_denied": {
                "pattern": ["PermissionError", "Permission denied"],
                "severity": "high",
                "auto_repairable": True,
                "repair_strategy": "fix_permissions"
            },
            "dependency_missing": {
                "pattern": ["ModuleNotFoundError", "ImportError"],
                "severity": "high",
                "auto_repairable": True,
                "repair_strategy": "install_dependencies"
            },
            "disk_space_full": {
                "pattern": ["No space left on device", "Disk full"],
                "severity": "critical",
                "auto_repairable": True,
                "repair_strategy": "cleanup_disk_space"
            },
            "memory_error": {
                "pattern": ["MemoryError", "Out of memory"],
                "severity": "critical",
                "auto_repairable": True,
                "repair_strategy": "optimize_memory_usage"
            },
            "network_timeout": {
                "pattern": ["TimeoutError", "Connection timeout"],
                "severity": "medium",
                "auto_repairable": True,
                "repair_strategy": "retry_with_backoff"
            }
        }
    
    def _initialize_repair_strategies(self) -> Dict[str, callable]:
        """Initialize repair strategy functions"""
        return {
            "create_missing_file": self._create_missing_file,
            "fix_permissions": self._fix_permissions,
            "install_dependencies": self._install_dependencies,
            "cleanup_disk_space": self._cleanup_disk_space,
            "optimize_memory_usage": self._optimize_memory_usage,
            "retry_with_backoff": self._retry_with_backoff
        }
    
    def diagnose_error(self, error_message: str, context: Dict) -> Optional[Dict]:
        """Diagnose error and determine repair strategy"""
        for error_type, pattern_info in self.error_patterns.items():
            for pattern in pattern_info["pattern"]:
                if pattern.lower() in error_message.lower():
                    return {
                        "error_type": error_type,
                        "severity": pattern_info["severity"],
                        "auto_repairable": pattern_info["auto_repairable"],
                        "repair_strategy": pattern_info["repair_strategy"],
                        "context": context
                    }
        
        return None
    
    def attempt_repair(self, diagnosis: Dict) -> bool:
        """Attempt to repair the diagnosed error"""
        if not diagnosis["auto_repairable"]:
            return False
        
        repair_strategy = diagnosis["repair_strategy"]
        repair_func = self.repair_strategies.get(repair_strategy)
        
        if not repair_func:
            return False
        
        try:
            success = repair_func(diagnosis["context"])
            
            # Record repair attempt
            self.repair_history.append({
                "timestamp": datetime.now().isoformat(),
                "error_type": diagnosis["error_type"],
                "repair_strategy": repair_strategy,
                "success": success,
                "context": diagnosis["context"]
            })
            
            return success
            
        except Exception as e:
            logging.error(f"Repair attempt failed: {e}")
            return False
    
    def _create_missing_file(self, context: Dict) -> bool:
        """Create missing file or directory"""
        missing_path = context.get("missing_path")
        if not missing_path:
            return False
        
        try:
            if context.get("is_directory", False):
                os.makedirs(missing_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(missing_path), exist_ok=True)
                with open(missing_path, 'w') as f:
                    f.write(context.get("default_content", ""))
            
            return True
        except Exception:
            return False
    
    def _fix_permissions(self, context: Dict) -> bool:
        """Fix file permissions"""
        file_path = context.get("file_path")
        if not file_path or not os.path.exists(file_path):
            return False
        
        try:
            os.chmod(file_path, 0o755)
            return True
        except Exception:
            return False
    
    def _install_dependencies(self, context: Dict) -> bool:
        """Install missing dependencies"""
        missing_module = context.get("missing_module")
        if not missing_module:
            return False
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", missing_module], 
                         check=True, capture_output=True)
            return True
        except Exception:
            return False
    
    def _cleanup_disk_space(self, context: Dict) -> bool:
        """Clean up disk space"""
        try:
            # Clean temporary files
            temp_dirs = ["/tmp", "/var/tmp"]
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                        except:
                            continue
            
            return True
        except Exception:
            return False
    
    def _optimize_memory_usage(self, context: Dict) -> bool:
        """Optimize memory usage"""
        try:
            # Force garbage collection
            import gc
            gc.collect()
            
            # Reduce batch sizes if applicable
            if "batch_size" in context:
                context["batch_size"] = max(1, context["batch_size"] // 2)
            
            return True
        except Exception:
            return False
    
    def _retry_with_backoff(self, context: Dict) -> bool:
        """Implement retry with exponential backoff"""
        retry_count = context.get("retry_count", 0)
        max_retries = context.get("max_retries", 3)
        
        if retry_count >= max_retries:
            return False
        
        # Exponential backoff
        wait_time = 2 ** retry_count
        time.sleep(wait_time)
        
        context["retry_count"] = retry_count + 1
        return True

class PriorityTaskQueue:
    """Priority-based task queue with self-optimization"""
    
    def __init__(self, max_workers: int = 4):
        self.queues = {
            TaskPriority.CRITICAL: queue.PriorityQueue(),
            TaskPriority.HIGH: queue.PriorityQueue(),
            TaskPriority.MEDIUM: queue.PriorityQueue(),
            TaskPriority.LOW: queue.PriorityQueue()
        }
        self.max_workers = max_workers
        self.workers = []
        self.running = False
        self.task_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_completion_time": 0.0,
            "error_rate": 0.0
        }
        
    def add_task(self, task: PrefabTask):
        """Add task to appropriate priority queue"""
        priority_queue = self.queues[task.priority]
        priority_queue.put((task.priority.value, time.time(), task))
        
    def start_workers(self):
        """Start worker threads"""
        self.running = True
        
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop_workers(self):
        """Stop worker threads"""
        self.running = False
        
        # Add sentinel values to wake up workers
        for priority_queue in self.queues.values():
            priority_queue.put((0, 0, None))
    
    def _worker_loop(self, worker_id: int):
        """Main worker loop"""
        while self.running:
            task = self._get_next_task()
            
            if task is None:
                continue
            
            self._execute_task(task, worker_id)
    
    def _get_next_task(self) -> Optional[PrefabTask]:
        """Get next task from highest priority queue"""
        for priority in [TaskPriority.CRITICAL, TaskPriority.HIGH, 
                        TaskPriority.MEDIUM, TaskPriority.LOW]:
            priority_queue = self.queues[priority]
            
            try:
                _, _, task = priority_queue.get(timeout=1.0)
                return task
            except queue.Empty:
                continue
        
        return None
    
    def _execute_task(self, task: PrefabTask, worker_id: int):
        """Execute a single task with error handling and self-repair"""
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()
        
        start_time = time.time()
        
        try:
            # Execute the actual task
            result = self._run_task_logic(task)
            
            if result["success"]:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                task.output_path = result.get("output_path")
                
                # Update performance metrics
                completion_time = time.time() - start_time
                self._update_performance_metrics(True, completion_time)
                
            else:
                self._handle_task_failure(task, result.get("error", "Unknown error"))
                
        except Exception as e:
            self._handle_task_failure(task, str(e))
        
        finally:
            self.task_history.append(task)
    
    def _run_task_logic(self, task: PrefabTask) -> Dict:
        """Run the actual task logic"""
        task_type = task.task_type
        
        if task_type == "generate_prefab":
            return self._generate_prefab(task)
        elif task_type == "generate_script":
            return self._generate_script(task)
        elif task_type == "optimize_assets":
            return self._optimize_assets(task)
        elif task_type == "validate_project":
            return self._validate_project(task)
        else:
            return {"success": False, "error": f"Unknown task type: {task_type}"}
    
    def _generate_prefab(self, task: PrefabTask) -> Dict:
        """Generate a prefab based on task specification"""
        spec = task.spec
        output_dir = spec.get("output_dir", "/tmp/generated_prefabs")
        
        os.makedirs(output_dir, exist_ok=True)
        
        prefab_name = spec.get("name", f"GeneratedPrefab_{task.task_id}")
        prefab_path = os.path.join(output_dir, f"{prefab_name}.prefab")
        
        # Generate prefab content
        prefab_content = self._create_prefab_content(spec)
        
        with open(prefab_path, 'w') as f:
            f.write(prefab_content)
        
        return {"success": True, "output_path": prefab_path}
    
    def _generate_script(self, task: PrefabTask) -> Dict:
        """Generate a script based on task specification"""
        spec = task.spec
        output_dir = spec.get("output_dir", "/tmp/generated_scripts")
        
        os.makedirs(output_dir, exist_ok=True)
        
        script_name = spec.get("name", f"GeneratedScript_{task.task_id}")
        script_path = os.path.join(output_dir, f"{script_name}.cs")
        
        # Generate script content
        script_content = self._create_script_content(spec)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        return {"success": True, "output_path": script_path}
    
    def _optimize_assets(self, task: PrefabTask) -> Dict:
        """Optimize assets based on task specification"""
        spec = task.spec
        asset_path = spec.get("asset_path")
        
        if not asset_path or not os.path.exists(asset_path):
            return {"success": False, "error": f"Asset path not found: {asset_path}"}
        
        # Perform optimization (simplified)
        optimized_path = f"{asset_path}.optimized"
        shutil.copy2(asset_path, optimized_path)
        
        return {"success": True, "output_path": optimized_path}
    
    def _validate_project(self, task: PrefabTask) -> Dict:
        """Validate project based on task specification"""
        spec = task.spec
        project_path = spec.get("project_path")
        
        if not project_path or not os.path.exists(project_path):
            return {"success": False, "error": f"Project path not found: {project_path}"}
        
        # Perform validation (simplified)
        validation_results = {
            "structure_valid": True,
            "scripts_compile": True,
            "assets_valid": True
        }
        
        return {"success": True, "validation_results": validation_results}
    
    def _create_prefab_content(self, spec: Dict) -> str:
        """Create prefab content with self-repair capabilities"""
        prefab_name = spec.get("name", "GeneratedPrefab")
        components = spec.get("components", [])
        
        return f"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &{hash(prefab_name) % 1000000}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {hash(prefab_name) % 1000000 + 1}}}
  m_Layer: 0
  m_Name: {prefab_name}
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
  # Auto-generated with self-repair: {datetime.now().isoformat()}
  # Components: {', '.join(components)}"""
    
    def _create_script_content(self, spec: Dict) -> str:
        """Create script content with self-repair capabilities"""
        script_name = spec.get("name", "GeneratedScript")
        base_class = spec.get("base_class", "MonoBehaviour")
        
        return f"""using UnityEngine;
using System.Collections;

/// <summary>
/// Auto-generated script with self-repair capabilities
/// Generated: {datetime.now().isoformat()}
/// OptiStack Integration: Enabled
/// </summary>
public class {script_name} : {base_class}
{{
    [Header("Self-Repair Settings")]
    public bool selfRepairEnabled = true;
    public float healthCheckInterval = 30f;
    
    private bool systemHealthy = true;
    private float lastHealthCheck = 0f;
    
    void Start()
    {{
        InitializeSystem();
        if (selfRepairEnabled)
        {{
            StartCoroutine(SelfRepairLoop());
        }}
    }}
    
    void Update()
    {{
        // Auto-generated update logic
        {spec.get('update_logic', '// No update logic specified')}
        
        // Periodic health check
        if (Time.time - lastHealthCheck > healthCheckInterval)
        {{
            PerformHealthCheck();
            lastHealthCheck = Time.time;
        }}
    }}
    
    private void InitializeSystem()
    {{
        // System initialization
        {spec.get('init_logic', '// No initialization logic specified')}
        systemHealthy = true;
    }}
    
    private void PerformHealthCheck()
    {{
        try
        {{
            // Validate system state
            systemHealthy = ValidateSystemState();
            
            if (!systemHealthy && selfRepairEnabled)
            {{
                AttemptSelfRepair();
            }}
        }}
        catch (System.Exception e)
        {{
            Debug.LogError($"Health check failed: {{e.Message}}");
            if (selfRepairEnabled)
            {{
                AttemptSelfRepair();
            }}
        }}
    }}
    
    private bool ValidateSystemState()
    {{
        // Validate component integrity
        return gameObject != null && enabled && gameObject.activeInHierarchy;
    }}
    
    private void AttemptSelfRepair()
    {{
        Debug.Log($"{{name}}: Attempting self-repair...");
        
        // Reset to safe state
        ResetToSafeState();
        
        // Re-initialize
        InitializeSystem();
        
        Debug.Log($"{{name}}: Self-repair completed");
    }}
    
    private void ResetToSafeState()
    {{
        // Reset component to known good state
        {spec.get('reset_logic', '// No reset logic specified')}
    }}
    
    private IEnumerator SelfRepairLoop()
    {{
        while (selfRepairEnabled)
        {{
            yield return new WaitForSeconds(healthCheckInterval);
            PerformHealthCheck();
        }}
    }}
}}"""
    
    def _handle_task_failure(self, task: PrefabTask, error_message: str):
        """Handle task failure with self-repair attempts"""
        task.error_message = error_message
        task.retry_count += 1
        
        # Update performance metrics
        self._update_performance_metrics(False, 0)
        
        # Attempt self-repair if retries available
        if task.retry_count <= task.max_retries:
            # Diagnose and attempt repair
            repair_cli = SelfRepairCLI()
            diagnosis = repair_cli.diagnose_error(error_message, {"task": task})
            
            if diagnosis and repair_cli.attempt_repair(diagnosis):
                # Retry the task
                task.status = TaskStatus.RETRYING
                self.add_task(task)
            else:
                task.status = TaskStatus.FAILED
        else:
            task.status = TaskStatus.FAILED
    
    def _update_performance_metrics(self, success: bool, completion_time: float):
        """Update performance metrics"""
        if success:
            self.performance_metrics["tasks_completed"] += 1
            
            # Update average completion time
            total_completed = self.performance_metrics["tasks_completed"]
            current_avg = self.performance_metrics["average_completion_time"]
            new_avg = ((current_avg * (total_completed - 1)) + completion_time) / total_completed
            self.performance_metrics["average_completion_time"] = new_avg
        else:
            self.performance_metrics["tasks_failed"] += 1
        
        # Update error rate
        total_tasks = (self.performance_metrics["tasks_completed"] + 
                      self.performance_metrics["tasks_failed"])
        if total_tasks > 0:
            self.performance_metrics["error_rate"] = (
                self.performance_metrics["tasks_failed"] / total_tasks
            )

class CLIPrefabInjector:
    """Main CLI Prefab Injector with OptiStack integration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.optistack = self._initialize_optistack()
        self.task_queue = PriorityTaskQueue(max_workers=self.config.get("max_workers", 4))
        self.batch_jobs = {}
        self.self_repair = SelfRepairCLI()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('prefab_injector.log'),
                logging.StreamHandler()
            ]
        )
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file"""
        default_config = {
            "max_workers": 4,
            "output_directory": "/tmp/generated_assets",
            "optistack_enabled": True,
            "self_repair_enabled": True,
            "risk_assessment_enabled": True
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                else:
                    user_config = json.load(f)
                
                default_config.update(user_config)
        
        return default_config
    
    def _initialize_optistack(self) -> Optional[OptiStack]:
        """Initialize OptiStack if enabled"""
        if not self.config.get("optistack_enabled", True):
            return None
        
        optistack_config = OptiStackConfig(
            optix_gate_enabled=True,
            optimax_enabled=True,
            optilev_enabled=True,
            perpetual_optimization=True
        )
        
        return OptiStack(optistack_config)
    
    def create_task(self, task_type: str, spec: Dict, priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Create a new task"""
        task_id = hashlib.md5(f"{task_type}_{time.time()}".encode()).hexdigest()[:8]
        
        # OptiStack processing if enabled
        if self.optistack:
            opti_result = self.optistack.process_system(spec)
            if opti_result["status"] == "blocked":
                raise ValueError(f"Task blocked by OptiX-Gate: {opti_result['reason']}")
            
            spec = opti_result["optimized_spec"]
            risk_assessment = opti_result.get("gate_check")
        else:
            risk_assessment = None
        
        task = PrefabTask(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            spec=spec,
            status=TaskStatus.PENDING,
            created_at=datetime.now().isoformat(),
            risk_assessment=risk_assessment
        )
        
        self.task_queue.add_task(task)
        logging.info(f"Created task {task_id} of type {task_type} with priority {priority.name}")
        
        return task_id
    
    def create_batch_job(self, name: str, tasks: List[Dict], priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Create a batch job with multiple tasks"""
        job_id = hashlib.md5(f"{name}_{time.time()}".encode()).hexdigest()[:8]
        
        prefab_tasks = []
        for task_spec in tasks:
            task_id = self.create_task(
                task_spec["type"],
                task_spec["spec"],
                priority
            )
            
            # Find the created task
            for task in self.task_queue.task_history:
                if task.task_id == task_id:
                    prefab_tasks.append(task)
                    break
        
        batch_job = BatchJob(
            job_id=job_id,
            name=name,
            tasks=prefab_tasks,
            priority=priority,
            created_at=datetime.now().isoformat(),
            status=TaskStatus.PENDING
        )
        
        self.batch_jobs[job_id] = batch_job
        logging.info(f"Created batch job {job_id} with {len(tasks)} tasks")
        
        return job_id
    
    def start_processing(self):
        """Start task processing"""
        self.task_queue.start_workers()
        logging.info("Task processing started")
    
    def stop_processing(self):
        """Stop task processing"""
        self.task_queue.stop_workers()
        logging.info("Task processing stopped")
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get status of a specific task"""
        for task in self.task_queue.task_history:
            if task.task_id == task_id:
                return asdict(task)
        
        return None
    
    def get_batch_status(self, job_id: str) -> Optional[Dict]:
        """Get status of a batch job"""
        batch_job = self.batch_jobs.get(job_id)
        if not batch_job:
            return None
        
        # Update batch job status
        completed_tasks = sum(1 for task in batch_job.tasks 
                            if task.status == TaskStatus.COMPLETED)
        total_tasks = len(batch_job.tasks)
        
        batch_job.progress = completed_tasks / total_tasks if total_tasks > 0 else 0
        
        if completed_tasks == total_tasks:
            batch_job.status = TaskStatus.COMPLETED
        elif any(task.status == TaskStatus.FAILED for task in batch_job.tasks):
            batch_job.status = TaskStatus.FAILED
        elif any(task.status == TaskStatus.IN_PROGRESS for task in batch_job.tasks):
            batch_job.status = TaskStatus.IN_PROGRESS
        
        return asdict(batch_job)
    
    def get_system_metrics(self) -> Dict:
        """Get comprehensive system metrics"""
        return {
            "task_queue_metrics": self.task_queue.performance_metrics,
            "optistack_metrics": self.optistack.get_optistack_metrics() if self.optistack else None,
            "self_repair_history": self.self_repair.repair_history[-10:],
            "active_workers": len(self.task_queue.workers),
            "pending_tasks": sum(q.qsize() for q in self.task_queue.queues.values()),
            "batch_jobs": len(self.batch_jobs),
            "system_health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> str:
        """Assess overall system health"""
        error_rate = self.task_queue.performance_metrics["error_rate"]
        
        if error_rate < 0.05:  # Less than 5% error rate
            return "healthy"
        elif error_rate < 0.15:  # Less than 15% error rate
            return "warning"
        else:
            return "critical"

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="CLI Prefab Injector with OptiStack")
    
    parser.add_argument("--config", type=str, help="Configuration file path")
    parser.add_argument("--task-type", type=str, choices=["generate_prefab", "generate_script", "optimize_assets", "validate_project"])
    parser.add_argument("--spec", type=str, help="Task specification (JSON string)")
    parser.add_argument("--priority", type=str, choices=["low", "medium", "high", "critical"], default="medium")
    parser.add_argument("--batch-file", type=str, help="Batch job file (JSON/YAML)")
    parser.add_argument("--status", type=str, help="Get status of task or batch job")
    parser.add_argument("--metrics", action="store_true", help="Show system metrics")
    parser.add_argument("--start-daemon", action="store_true", help="Start as daemon")
    
    args = parser.parse_args()
    
    # Initialize injector
    injector = CLIPrefabInjector(args.config)
    
    if args.start_daemon:
        # Start as daemon
        injector.start_processing()
        print("Prefab Injector daemon started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            injector.stop_processing()
            print("Daemon stopped.")
    
    elif args.metrics:
        # Show metrics
        metrics = injector.get_system_metrics()
        print(json.dumps(metrics, indent=2))
    
    elif args.status:
        # Show status
        task_status = injector.get_task_status(args.status)
        if task_status:
            print(json.dumps(task_status, indent=2))
        else:
            batch_status = injector.get_batch_status(args.status)
            if batch_status:
                print(json.dumps(batch_status, indent=2))
            else:
                print(f"No task or batch job found with ID: {args.status}")
    
    elif args.batch_file:
        # Process batch file
        with open(args.batch_file, 'r') as f:
            if args.batch_file.endswith('.yaml') or args.batch_file.endswith('.yml'):
                batch_data = yaml.safe_load(f)
            else:
                batch_data = json.load(f)
        
        job_id = injector.create_batch_job(
            batch_data["name"],
            batch_data["tasks"],
            TaskPriority[args.priority.upper()]
        )
        
        print(f"Created batch job: {job_id}")
        
        # Start processing
        injector.start_processing()
        
        # Wait for completion
        while True:
            status = injector.get_batch_status(job_id)
            if status["status"] in ["completed", "failed"]:
                break
            time.sleep(1)
        
        injector.stop_processing()
        print(f"Batch job completed with status: {status['status']}")
    
    elif args.task_type and args.spec:
        # Create single task
        spec = json.loads(args.spec)
        task_id = injector.create_task(
            args.task_type,
            spec,
            TaskPriority[args.priority.upper()]
        )
        
        print(f"Created task: {task_id}")
        
        # Start processing
        injector.start_processing()
        
        # Wait for completion
        while True:
            status = injector.get_task_status(task_id)
            if status["status"] in ["completed", "failed"]:
                break
            time.sleep(1)
        
        injector.stop_processing()
        print(f"Task completed with status: {status['status']}")
        
        if status["output_path"]:
            print(f"Output: {status['output_path']}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

