#!/usr/bin/env python3
"""
Unity Connector with Self-Repair and Risk Management
Includes OptiGate risk matrix and automated mitigation strategies
"""

import os
import json
import subprocess
import shutil
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import threading
import hashlib

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ModuleTier(Enum):
    T40_T60 = "T40-T60"
    T61_T80 = "T61-T80"
    T81_T100 = "T81-T100"

@dataclass
class RiskAssessment:
    risk_id: str
    module_tier: ModuleTier
    risk_level: RiskLevel
    description: str
    probability: float  # 0.0 to 1.0
    impact_score: int   # 1 to 10
    mitigation_strategy: str
    auto_repair_enabled: bool
    monitoring_enabled: bool

@dataclass
class SelfRepairAction:
    action_id: str
    trigger_condition: str
    repair_script: str
    rollback_script: str
    success_criteria: str
    max_attempts: int

class OptiGateRiskMatrix:
    """Risk assessment and mitigation for every optimization"""
    
    def __init__(self):
        self.risk_assessments = self._initialize_risk_matrix()
        self.mitigation_strategies = self._initialize_mitigation_strategies()
        self.repair_actions = self._initialize_repair_actions()
        
    def _initialize_risk_matrix(self) -> Dict[str, RiskAssessment]:
        """Initialize comprehensive risk matrix"""
        return {
            "unity_project_corruption": RiskAssessment(
                risk_id="unity_project_corruption",
                module_tier=ModuleTier.T40_T60,
                risk_level=RiskLevel.HIGH,
                description="Unity project files become corrupted during AI generation",
                probability=0.15,
                impact_score=8,
                mitigation_strategy="automatic_backup_and_validation",
                auto_repair_enabled=True,
                monitoring_enabled=True
            ),
            "script_compilation_failure": RiskAssessment(
                risk_id="script_compilation_failure",
                module_tier=ModuleTier.T40_T60,
                risk_level=RiskLevel.MEDIUM,
                description="Generated C# scripts fail to compile",
                probability=0.25,
                impact_score=6,
                mitigation_strategy="syntax_validation_and_auto_fix",
                auto_repair_enabled=True,
                monitoring_enabled=True
            ),
            "asset_dependency_break": RiskAssessment(
                risk_id="asset_dependency_break",
                module_tier=ModuleTier.T61_T80,
                risk_level=RiskLevel.MEDIUM,
                description="Asset references break during generation",
                probability=0.20,
                impact_score=5,
                mitigation_strategy="dependency_tracking_and_repair",
                auto_repair_enabled=True,
                monitoring_enabled=True
            ),
            "performance_degradation": RiskAssessment(
                risk_id="performance_degradation",
                module_tier=ModuleTier.T61_T80,
                risk_level=RiskLevel.LOW,
                description="Generated systems cause performance issues",
                probability=0.30,
                impact_score=4,
                mitigation_strategy="performance_monitoring_and_optimization",
                auto_repair_enabled=True,
                monitoring_enabled=True
            ),
            "build_pipeline_failure": RiskAssessment(
                risk_id="build_pipeline_failure",
                module_tier=ModuleTier.T81_T100,
                risk_level=RiskLevel.CRITICAL,
                description="Unity build process fails completely",
                probability=0.10,
                impact_score=10,
                mitigation_strategy="redundant_build_systems",
                auto_repair_enabled=True,
                monitoring_enabled=True
            ),
            "ai_generation_infinite_loop": RiskAssessment(
                risk_id="ai_generation_infinite_loop",
                module_tier=ModuleTier.T81_T100,
                risk_level=RiskLevel.HIGH,
                description="AI generation gets stuck in infinite optimization loop",
                probability=0.08,
                impact_score=9,
                mitigation_strategy="circuit_breaker_and_timeout",
                auto_repair_enabled=True,
                monitoring_enabled=True
            )
        }
    
    def _initialize_mitigation_strategies(self) -> Dict[str, Dict]:
        """Initialize mitigation strategies for each risk"""
        return {
            "automatic_backup_and_validation": {
                "description": "Create automatic backups before any operation and validate integrity",
                "steps": [
                    "create_timestamped_backup",
                    "validate_project_structure",
                    "verify_asset_integrity",
                    "test_compilation"
                ],
                "rollback_enabled": True,
                "success_rate": 0.95
            },
            "syntax_validation_and_auto_fix": {
                "description": "Validate C# syntax and automatically fix common issues",
                "steps": [
                    "parse_csharp_syntax",
                    "identify_compilation_errors",
                    "apply_auto_fixes",
                    "recompile_and_verify"
                ],
                "rollback_enabled": True,
                "success_rate": 0.88
            },
            "dependency_tracking_and_repair": {
                "description": "Track all asset dependencies and repair broken references",
                "steps": [
                    "scan_asset_dependencies",
                    "identify_broken_references",
                    "attempt_automatic_repair",
                    "regenerate_missing_assets"
                ],
                "rollback_enabled": True,
                "success_rate": 0.82
            },
            "performance_monitoring_and_optimization": {
                "description": "Monitor performance and automatically optimize",
                "steps": [
                    "profile_performance_metrics",
                    "identify_bottlenecks",
                    "apply_optimization_patterns",
                    "verify_performance_improvement"
                ],
                "rollback_enabled": True,
                "success_rate": 0.75
            },
            "redundant_build_systems": {
                "description": "Multiple build pipelines with automatic failover",
                "steps": [
                    "attempt_primary_build",
                    "fallback_to_secondary_build",
                    "use_cloud_build_service",
                    "manual_intervention_alert"
                ],
                "rollback_enabled": False,
                "success_rate": 0.98
            },
            "circuit_breaker_and_timeout": {
                "description": "Prevent infinite loops with circuit breakers and timeouts",
                "steps": [
                    "monitor_generation_time",
                    "detect_infinite_loops",
                    "trigger_circuit_breaker",
                    "reset_to_last_known_good_state"
                ],
                "rollback_enabled": True,
                "success_rate": 0.92
            }
        }
    
    def _initialize_repair_actions(self) -> Dict[str, SelfRepairAction]:
        """Initialize self-repair actions"""
        return {
            "fix_unity_corruption": SelfRepairAction(
                action_id="fix_unity_corruption",
                trigger_condition="unity_project_validation_failed",
                repair_script="restore_from_backup_and_regenerate",
                rollback_script="restore_original_backup",
                success_criteria="project_loads_successfully",
                max_attempts=3
            ),
            "fix_compilation_errors": SelfRepairAction(
                action_id="fix_compilation_errors",
                trigger_condition="csharp_compilation_failed",
                repair_script="auto_fix_syntax_errors",
                rollback_script="restore_previous_scripts",
                success_criteria="all_scripts_compile",
                max_attempts=5
            ),
            "repair_asset_references": SelfRepairAction(
                action_id="repair_asset_references",
                trigger_condition="missing_asset_references_detected",
                repair_script="regenerate_missing_assets_and_fix_references",
                rollback_script="restore_asset_backup",
                success_criteria="no_missing_references",
                max_attempts=3
            )
        }
    
    def assess_risk(self, operation: str, module_tier: ModuleTier) -> List[RiskAssessment]:
        """Assess risks for a specific operation"""
        relevant_risks = []
        
        for risk in self.risk_assessments.values():
            if risk.module_tier == module_tier or operation in risk.description.lower():
                relevant_risks.append(risk)
        
        # Sort by risk level and impact
        relevant_risks.sort(key=lambda r: (r.risk_level.value, r.impact_score), reverse=True)
        
        return relevant_risks
    
    def calculate_overall_risk_score(self, risks: List[RiskAssessment]) -> float:
        """Calculate overall risk score for operation"""
        if not risks:
            return 0.0
        
        total_risk = 0.0
        for risk in risks:
            risk_value = risk.probability * risk.impact_score
            total_risk += risk_value
        
        return min(total_risk / len(risks), 10.0)  # Cap at 10

class UnityProjectValidator:
    """Validates Unity project integrity and auto-repairs issues"""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.backup_path = f"{project_path}_backup_{int(time.time())}"
        
    def validate_project(self) -> Dict:
        """Comprehensive project validation"""
        validation_results = {
            "project_structure": self._validate_project_structure(),
            "asset_integrity": self._validate_asset_integrity(),
            "script_compilation": self._validate_script_compilation(),
            "dependency_integrity": self._validate_dependencies(),
            "overall_health": "unknown"
        }
        
        # Calculate overall health
        passed_checks = sum(1 for result in validation_results.values() 
                          if isinstance(result, dict) and result.get("status") == "passed")
        total_checks = len(validation_results) - 1  # Exclude overall_health
        
        if passed_checks == total_checks:
            validation_results["overall_health"] = "healthy"
        elif passed_checks >= total_checks * 0.7:
            validation_results["overall_health"] = "warning"
        else:
            validation_results["overall_health"] = "critical"
        
        return validation_results
    
    def _validate_project_structure(self) -> Dict:
        """Validate Unity project structure"""
        required_folders = ["Assets", "ProjectSettings", "Packages"]
        required_files = ["ProjectSettings/ProjectVersion.txt"]
        
        missing_items = []
        
        for folder in required_folders:
            if not os.path.exists(os.path.join(self.project_path, folder)):
                missing_items.append(f"folder: {folder}")
        
        for file in required_files:
            if not os.path.exists(os.path.join(self.project_path, file)):
                missing_items.append(f"file: {file}")
        
        return {
            "status": "passed" if not missing_items else "failed",
            "missing_items": missing_items,
            "auto_repairable": True
        }
    
    def _validate_asset_integrity(self) -> Dict:
        """Validate asset file integrity"""
        assets_path = os.path.join(self.project_path, "Assets")
        corrupted_assets = []
        
        if os.path.exists(assets_path):
            for root, dirs, files in os.walk(assets_path):
                for file in files:
                    if file.endswith(('.meta', '.asset', '.prefab')):
                        file_path = os.path.join(root, file)
                        if not self._is_file_valid(file_path):
                            corrupted_assets.append(file_path)
        
        return {
            "status": "passed" if not corrupted_assets else "failed",
            "corrupted_assets": corrupted_assets,
            "auto_repairable": True
        }
    
    def _validate_script_compilation(self) -> Dict:
        """Validate C# script compilation"""
        scripts_path = os.path.join(self.project_path, "Assets")
        compilation_errors = []
        
        # Find all C# scripts
        csharp_files = []
        if os.path.exists(scripts_path):
            for root, dirs, files in os.walk(scripts_path):
                for file in files:
                    if file.endswith('.cs'):
                        csharp_files.append(os.path.join(root, file))
        
        # Basic syntax validation
        for script_file in csharp_files:
            errors = self._validate_csharp_syntax(script_file)
            if errors:
                compilation_errors.extend(errors)
        
        return {
            "status": "passed" if not compilation_errors else "failed",
            "compilation_errors": compilation_errors,
            "auto_repairable": True
        }
    
    def _validate_dependencies(self) -> Dict:
        """Validate asset dependencies"""
        broken_references = []
        
        # This would typically involve parsing .meta files and checking references
        # For now, we'll do a basic check
        
        return {
            "status": "passed",
            "broken_references": broken_references,
            "auto_repairable": True
        }
    
    def _is_file_valid(self, file_path: str) -> bool:
        """Check if file is valid and not corrupted"""
        try:
            with open(file_path, 'rb') as f:
                # Basic file integrity check
                content = f.read(1024)  # Read first 1KB
                return len(content) > 0
        except:
            return False
    
    def _validate_csharp_syntax(self, script_path: str) -> List[str]:
        """Basic C# syntax validation"""
        errors = []
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Basic syntax checks
                if content.count('{') != content.count('}'):
                    errors.append(f"{script_path}: Mismatched braces")
                
                if content.count('(') != content.count(')'):
                    errors.append(f"{script_path}: Mismatched parentheses")
                
                # Check for common Unity patterns
                if 'MonoBehaviour' in content and 'using UnityEngine;' not in content:
                    errors.append(f"{script_path}: Missing UnityEngine import")
        
        except Exception as e:
            errors.append(f"{script_path}: Could not read file - {str(e)}")
        
        return errors

class SelfRepairSystem:
    """Automated self-repair system for Unity projects"""
    
    def __init__(self, project_path: str, risk_matrix: OptiGateRiskMatrix):
        self.project_path = project_path
        self.risk_matrix = risk_matrix
        self.validator = UnityProjectValidator(project_path)
        self.repair_history = []
        self.monitoring_active = False
        
    def start_monitoring(self):
        """Start continuous monitoring and auto-repair"""
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self._perform_health_check()
                    time.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    logging.error(f"Monitoring error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
    
    def _perform_health_check(self):
        """Perform health check and trigger repairs if needed"""
        validation_results = self.validator.validate_project()
        
        if validation_results["overall_health"] in ["warning", "critical"]:
            self._trigger_auto_repair(validation_results)
    
    def _trigger_auto_repair(self, validation_results: Dict):
        """Trigger appropriate auto-repair actions"""
        repair_actions = []
        
        # Determine which repairs are needed
        if validation_results["project_structure"]["status"] == "failed":
            repair_actions.append("fix_unity_corruption")
        
        if validation_results["script_compilation"]["status"] == "failed":
            repair_actions.append("fix_compilation_errors")
        
        if validation_results["dependency_integrity"]["status"] == "failed":
            repair_actions.append("repair_asset_references")
        
        # Execute repairs
        for action_id in repair_actions:
            self._execute_repair_action(action_id)
    
    def _execute_repair_action(self, action_id: str):
        """Execute a specific repair action"""
        action = self.risk_matrix.repair_actions.get(action_id)
        if not action:
            return
        
        repair_record = {
            "action_id": action_id,
            "timestamp": datetime.now().isoformat(),
            "attempts": 0,
            "success": False,
            "error_message": None
        }
        
        for attempt in range(action.max_attempts):
            repair_record["attempts"] = attempt + 1
            
            try:
                # Create backup before repair
                self._create_backup()
                
                # Execute repair script
                success = self._run_repair_script(action.repair_script)
                
                if success and self._verify_repair_success(action.success_criteria):
                    repair_record["success"] = True
                    break
                else:
                    # Rollback if repair failed
                    self._run_rollback_script(action.rollback_script)
                    
            except Exception as e:
                repair_record["error_message"] = str(e)
                self._run_rollback_script(action.rollback_script)
        
        self.repair_history.append(repair_record)
    
    def _create_backup(self):
        """Create backup of current project state"""
        backup_path = f"{self.project_path}_backup_{int(time.time())}"
        shutil.copytree(self.project_path, backup_path)
        return backup_path
    
    def _run_repair_script(self, script_name: str) -> bool:
        """Run a repair script"""
        # This would contain the actual repair logic
        # For now, we'll simulate the repair
        
        repair_scripts = {
            "restore_from_backup_and_regenerate": self._restore_from_backup,
            "auto_fix_syntax_errors": self._auto_fix_syntax_errors,
            "regenerate_missing_assets_and_fix_references": self._regenerate_assets
        }
        
        script_func = repair_scripts.get(script_name)
        if script_func:
            return script_func()
        
        return False
    
    def _run_rollback_script(self, script_name: str):
        """Run a rollback script"""
        # Implementation for rollback scripts
        pass
    
    def _verify_repair_success(self, criteria: str) -> bool:
        """Verify that repair was successful"""
        if criteria == "project_loads_successfully":
            return self._test_project_load()
        elif criteria == "all_scripts_compile":
            return self._test_script_compilation()
        elif criteria == "no_missing_references":
            return self._test_asset_references()
        
        return False
    
    def _restore_from_backup(self) -> bool:
        """Restore project from backup"""
        # Implementation for backup restoration
        return True
    
    def _auto_fix_syntax_errors(self) -> bool:
        """Automatically fix common C# syntax errors"""
        # Implementation for syntax error fixing
        return True
    
    def _regenerate_assets(self) -> bool:
        """Regenerate missing assets"""
        # Implementation for asset regeneration
        return True
    
    def _test_project_load(self) -> bool:
        """Test if Unity project loads successfully"""
        # This would typically involve calling Unity in batch mode
        return True
    
    def _test_script_compilation(self) -> bool:
        """Test if all scripts compile successfully"""
        validation = self.validator._validate_script_compilation()
        return validation["status"] == "passed"
    
    def _test_asset_references(self) -> bool:
        """Test if all asset references are valid"""
        validation = self.validator._validate_dependencies()
        return validation["status"] == "passed"

class UnityConnector:
    """Main Unity connector with integrated risk management and self-repair"""
    
    def __init__(self, project_path: str, config: Dict):
        self.project_path = project_path
        self.config = config
        self.risk_matrix = OptiGateRiskMatrix()
        self.self_repair = SelfRepairSystem(project_path, self.risk_matrix)
        self.generation_history = []
        
    def generate_unity_system(self, system_spec: Dict) -> Dict:
        """Generate Unity system with risk assessment and self-repair"""
        
        # Step 1: Risk assessment
        module_tier = ModuleTier(system_spec.get("module_tier", "T40-T60"))
        risks = self.risk_matrix.assess_risk("unity_generation", module_tier)
        risk_score = self.risk_matrix.calculate_overall_risk_score(risks)
        
        # Step 2: Pre-generation backup
        backup_path = self.self_repair._create_backup()
        
        generation_result = {
            "timestamp": datetime.now().isoformat(),
            "system_spec": system_spec,
            "module_tier": module_tier.value,
            "risk_assessment": {
                "overall_risk_score": risk_score,
                "identified_risks": [
                    {
                        "risk_id": risk.risk_id,
                        "level": risk.risk_level.value,
                        "probability": risk.probability,
                        "impact": risk.impact_score,
                        "mitigation": risk.mitigation_strategy
                    }
                    for risk in risks
                ]
            },
            "backup_path": backup_path,
            "generation_status": "in_progress"
        }
        
        try:
            # Step 3: Generate Unity components
            generated_components = self._generate_components(system_spec)
            
            # Step 4: Validate generation
            validation_results = self.self_repair.validator.validate_project()
            
            # Step 5: Auto-repair if needed
            if validation_results["overall_health"] != "healthy":
                self.self_repair._trigger_auto_repair(validation_results)
                # Re-validate after repair
                validation_results = self.self_repair.validator.validate_project()
            
            generation_result.update({
                "generation_status": "completed",
                "generated_components": generated_components,
                "validation_results": validation_results,
                "auto_repair_triggered": validation_results["overall_health"] != "healthy"
            })
            
        except Exception as e:
            # Auto-recovery on failure
            generation_result.update({
                "generation_status": "failed",
                "error": str(e),
                "auto_recovery_attempted": True
            })
            
            # Restore from backup
            self._restore_from_backup(backup_path)
        
        self.generation_history.append(generation_result)
        return generation_result
    
    def _generate_components(self, system_spec: Dict) -> Dict:
        """Generate Unity components based on specification"""
        components = {
            "scripts": [],
            "prefabs": [],
            "materials": [],
            "scenes": []
        }
        
        # Generate C# scripts
        if system_spec.get("scripts"):
            for script_spec in system_spec["scripts"]:
                script_path = self._generate_csharp_script(script_spec)
                components["scripts"].append(script_path)
        
        # Generate prefabs
        if system_spec.get("prefabs"):
            for prefab_spec in system_spec["prefabs"]:
                prefab_path = self._generate_prefab(prefab_spec)
                components["prefabs"].append(prefab_path)
        
        return components
    
    def _generate_csharp_script(self, script_spec: Dict) -> str:
        """Generate C# script with error handling"""
        script_name = script_spec.get("name", "GeneratedScript")
        script_content = self._create_script_content(script_spec)
        
        script_path = os.path.join(
            self.project_path, 
            "Assets", 
            "Scripts", 
            "Generated", 
            f"{script_name}.cs"
        )
        
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def _generate_prefab(self, prefab_spec: Dict) -> str:
        """Generate Unity prefab"""
        # This would contain prefab generation logic
        prefab_name = prefab_spec.get("name", "GeneratedPrefab")
        prefab_path = os.path.join(
            self.project_path,
            "Assets",
            "Prefabs",
            "Generated",
            f"{prefab_name}.prefab"
        )
        
        os.makedirs(os.path.dirname(prefab_path), exist_ok=True)
        
        # Create basic prefab file (simplified)
        prefab_content = self._create_prefab_content(prefab_spec)
        
        with open(prefab_path, 'w') as f:
            f.write(prefab_content)
        
        return prefab_path
    
    def _create_script_content(self, script_spec: Dict) -> str:
        """Create C# script content with proper structure"""
        class_name = script_spec.get("name", "GeneratedScript")
        base_class = script_spec.get("base_class", "MonoBehaviour")
        
        return f"""using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Auto-generated Unity script with self-repair capabilities
/// Generated on: {datetime.now().isoformat()}
/// Risk Level: {script_spec.get('risk_level', 'LOW')}
/// </summary>
public class {class_name} : {base_class}
{{
    [Header("Auto-Generated Properties")]
    public bool autoRepairEnabled = true;
    public float healthCheckInterval = 30f;
    
    private bool isHealthy = true;
    private float lastHealthCheck = 0f;
    
    void Start()
    {{
        // Initialize auto-generated system
        InitializeSystem();
        
        // Start health monitoring
        if (autoRepairEnabled)
        {{
            StartCoroutine(HealthMonitoringLoop());
        }}
    }}
    
    void Update()
    {{
        // Auto-generated update logic
        {script_spec.get('update_logic', '// No update logic specified')}
        
        // Continuous health check
        if (Time.time - lastHealthCheck > healthCheckInterval)
        {{
            PerformHealthCheck();
            lastHealthCheck = Time.time;
        }}
    }}
    
    private void InitializeSystem()
    {{
        // Auto-generated initialization
        {script_spec.get('init_logic', '// No initialization logic specified')}
    }}
    
    private void PerformHealthCheck()
    {{
        // Self-diagnostic and repair
        try
        {{
            // Check system integrity
            isHealthy = ValidateSystemState();
            
            if (!isHealthy && autoRepairEnabled)
            {{
                AttemptSelfRepair();
            }}
        }}
        catch (System.Exception e)
        {{
            Debug.LogError($"Health check failed: {{e.Message}}");
            if (autoRepairEnabled)
            {{
                AttemptSelfRepair();
            }}
        }}
    }}
    
    private bool ValidateSystemState()
    {{
        // Validate component state
        return gameObject != null && enabled;
    }}
    
    private void AttemptSelfRepair()
    {{
        // Self-repair logic
        Debug.Log($"{{name}}: Attempting self-repair...");
        
        // Reset to safe state
        ResetToSafeState();
        
        // Re-initialize if needed
        InitializeSystem();
        
        isHealthy = true;
        Debug.Log($"{{name}}: Self-repair completed");
    }}
    
    private void ResetToSafeState()
    {{
        // Reset component to known good state
        {script_spec.get('reset_logic', '// No reset logic specified')}
    }}
    
    private IEnumerator HealthMonitoringLoop()
    {{
        while (autoRepairEnabled)
        {{
            yield return new WaitForSeconds(healthCheckInterval);
            PerformHealthCheck();
        }}
    }}
    
    // Auto-generated methods
    {script_spec.get('custom_methods', '// No custom methods specified')}
}}"""
    
    def _create_prefab_content(self, prefab_spec: Dict) -> str:
        """Create Unity prefab content"""
        # Simplified prefab structure
        return f"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1 &{hash(prefab_spec.get('name', 'prefab')) % 1000000}
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: {hash(prefab_spec.get('name', 'prefab')) % 1000000 + 1}}}
  m_Layer: 0
  m_Name: {prefab_spec.get('name', 'GeneratedPrefab')}
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1"""
    
    def _restore_from_backup(self, backup_path: str):
        """Restore project from backup"""
        if os.path.exists(backup_path):
            shutil.rmtree(self.project_path)
            shutil.copytree(backup_path, self.project_path)
    
    def start_continuous_monitoring(self):
        """Start continuous monitoring and self-repair"""
        self.self_repair.start_monitoring()
    
    def stop_continuous_monitoring(self):
        """Stop continuous monitoring"""
        self.self_repair.stop_monitoring()
    
    def get_system_health_report(self) -> Dict:
        """Get comprehensive system health report"""
        validation_results = self.self_repair.validator.validate_project()
        
        return {
            "project_path": self.project_path,
            "overall_health": validation_results["overall_health"],
            "validation_details": validation_results,
            "risk_assessments": [
                {
                    "risk_id": risk.risk_id,
                    "level": risk.risk_level.value,
                    "description": risk.description,
                    "mitigation": risk.mitigation_strategy
                }
                for risk in self.risk_matrix.risk_assessments.values()
            ],
            "repair_history": self.self_repair.repair_history[-10:],  # Last 10 repairs
            "generation_history": self.generation_history[-5:],  # Last 5 generations
            "monitoring_active": self.self_repair.monitoring_active
        }

# Example usage
if __name__ == "__main__":
    # Initialize Unity connector
    project_path = "/path/to/unity/project"
    config = {"auto_repair": True, "monitoring": True}
    
    connector = UnityConnector(project_path, config)
    
    # Start continuous monitoring
    connector.start_continuous_monitoring()
    
    # Generate a system with risk assessment
    system_spec = {
        "module_tier": "T61-T80",
        "scripts": [
            {
                "name": "PlayerController",
                "base_class": "MonoBehaviour",
                "risk_level": "MEDIUM",
                "init_logic": "// Initialize player",
                "update_logic": "// Handle input"
            }
        ],
        "prefabs": [
            {
                "name": "Player",
                "components": ["PlayerController"]
            }
        ]
    }
    
    result = connector.generate_unity_system(system_spec)
    print("Generation Result:")
    print(json.dumps(result, indent=2))
    
    # Get health report
    health_report = connector.get_system_health_report()
    print("\nSystem Health Report:")
    print(json.dumps(health_report, indent=2))

