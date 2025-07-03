#!/usr/bin/env python3
"""
External I/O Boundary Layer
Provides file system interfaces and deployment protocols
"""

import os
import shutil
import json
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

@dataclass
class MountPoint:
    local_path: str
    external_path: str
    sync_enabled: bool = True
    watch_enabled: bool = True

@dataclass
class DeploymentTarget:
    name: str
    type: str  # 'vercel', 'netlify', 'heroku', 'custom'
    config: Dict
    auto_deploy: bool = False

class FileSystemBridge:
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path)
        self.mount_points = []
        self.observers = []
        self.deployment_targets = []
        self.setup_mount_points()
        self.setup_deployment_targets()
    
    def load_config(self, config_path: str) -> Dict:
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "sandbox_mount_paths": ["/home/ubuntu/projects", "/home/ubuntu/assets"],
            "external_storage": {"type": "local", "path": "/external/storage"},
            "deployment": {"auto_deploy": True, "target_platforms": ["vercel"]}
        }
    
    def setup_mount_points(self):
        """Setup mountable sandbox paths"""
        for path in self.config.get("sandbox_mount_paths", []):
            os.makedirs(path, exist_ok=True)
            mount_point = MountPoint(
                local_path=path,
                external_path=f"/external{path}",
                sync_enabled=True,
                watch_enabled=True
            )
            self.mount_points.append(mount_point)
            
            if mount_point.watch_enabled:
                self.setup_file_watcher(mount_point)
    
    def setup_file_watcher(self, mount_point: MountPoint):
        """Setup file system watcher for real-time sync"""
        class SyncHandler(FileSystemEventHandler):
            def __init__(self, bridge, mount_point):
                self.bridge = bridge
                self.mount_point = mount_point
            
            def on_modified(self, event):
                if not event.is_directory:
                    self.bridge.sync_file(event.src_path, self.mount_point)
            
            def on_created(self, event):
                if not event.is_directory:
                    self.bridge.sync_file(event.src_path, self.mount_point)
        
        handler = SyncHandler(self, mount_point)
        observer = Observer()
        observer.schedule(handler, mount_point.local_path, recursive=True)
        observer.start()
        self.observers.append(observer)
    
    def sync_file(self, file_path: str, mount_point: MountPoint):
        """Sync file to external storage"""
        if not mount_point.sync_enabled:
            return
        
        relative_path = os.path.relpath(file_path, mount_point.local_path)
        external_file = os.path.join(mount_point.external_path, relative_path)
        
        os.makedirs(os.path.dirname(external_file), exist_ok=True)
        shutil.copy2(file_path, external_file)
        print(f"Synced: {file_path} -> {external_file}")
    
    def setup_deployment_targets(self):
        """Setup deployment targets"""
        deployment_config = self.config.get("deployment", {})
        
        for platform in deployment_config.get("target_platforms", []):
            if platform == "vercel":
                target = DeploymentTarget(
                    name="vercel",
                    type="vercel",
                    config={
                        "project_name": "ai-generated-app",
                        "build_command": "npm run build",
                        "output_directory": "dist"
                    },
                    auto_deploy=deployment_config.get("auto_deploy", False)
                )
                self.deployment_targets.append(target)
            
            elif platform == "netlify":
                target = DeploymentTarget(
                    name="netlify",
                    type="netlify",
                    config={
                        "site_name": "ai-generated-app",
                        "build_command": "npm run build",
                        "publish_directory": "dist"
                    },
                    auto_deploy=deployment_config.get("auto_deploy", False)
                )
                self.deployment_targets.append(target)
    
    def deploy_project(self, project_path: str, target_name: str = None) -> Dict:
        """Deploy project to specified target"""
        if target_name:
            targets = [t for t in self.deployment_targets if t.name == target_name]
        else:
            targets = [t for t in self.deployment_targets if t.auto_deploy]
        
        results = []
        
        for target in targets:
            try:
                result = self._deploy_to_target(project_path, target)
                results.append(result)
            except Exception as e:
                results.append({
                    "target": target.name,
                    "status": "failed",
                    "error": str(e)
                })
        
        return {"deployments": results}
    
    def _deploy_to_target(self, project_path: str, target: DeploymentTarget) -> Dict:
        """Deploy to specific target"""
        if target.type == "vercel":
            return self._deploy_vercel(project_path, target)
        elif target.type == "netlify":
            return self._deploy_netlify(project_path, target)
        else:
            raise ValueError(f"Unsupported deployment target: {target.type}")
    
    def _deploy_vercel(self, project_path: str, target: DeploymentTarget) -> Dict:
        """Deploy to Vercel"""
        # Create vercel.json config
        vercel_config = {
            "name": target.config["project_name"],
            "builds": [
                {"src": "**/*", "use": "@vercel/static"}
            ]
        }
        
        config_path = os.path.join(project_path, "vercel.json")
        with open(config_path, 'w') as f:
            json.dump(vercel_config, f, indent=2)
        
        # Run deployment command
        cmd = ["vercel", "--prod", "--yes"]
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Extract URL from output
            url = self._extract_vercel_url(result.stdout)
            return {
                "target": "vercel",
                "status": "success",
                "url": url,
                "output": result.stdout
            }
        else:
            return {
                "target": "vercel",
                "status": "failed",
                "error": result.stderr
            }
    
    def _deploy_netlify(self, project_path: str, target: DeploymentTarget) -> Dict:
        """Deploy to Netlify"""
        # Create netlify.toml config
        netlify_config = f"""
[build]
  command = "{target.config['build_command']}"
  publish = "{target.config['publish_directory']}"

[build.environment]
  NODE_VERSION = "18"
"""
        
        config_path = os.path.join(project_path, "netlify.toml")
        with open(config_path, 'w') as f:
            f.write(netlify_config)
        
        # Run deployment command
        cmd = ["netlify", "deploy", "--prod", "--dir", target.config["publish_directory"]]
        result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            url = self._extract_netlify_url(result.stdout)
            return {
                "target": "netlify",
                "status": "success",
                "url": url,
                "output": result.stdout
            }
        else:
            return {
                "target": "netlify",
                "status": "failed",
                "error": result.stderr
            }
    
    def _extract_vercel_url(self, output: str) -> str:
        """Extract deployment URL from Vercel output"""
        lines = output.split('\n')
        for line in lines:
            if 'https://' in line and 'vercel.app' in line:
                return line.strip()
        return "URL not found"
    
    def _extract_netlify_url(self, output: str) -> str:
        """Extract deployment URL from Netlify output"""
        lines = output.split('\n')
        for line in lines:
            if 'https://' in line and 'netlify.app' in line:
                return line.strip()
        return "URL not found"
    
    def inject_external_files(self, external_path: str, target_mount: str) -> Dict:
        """Inject files from external source into sandbox"""
        mount_point = next((mp for mp in self.mount_points if mp.local_path == target_mount), None)
        
        if not mount_point:
            return {"status": "failed", "error": f"Mount point {target_mount} not found"}
        
        try:
            if os.path.exists(external_path):
                if os.path.isfile(external_path):
                    shutil.copy2(external_path, mount_point.local_path)
                else:
                    shutil.copytree(external_path, mount_point.local_path, dirs_exist_ok=True)
                
                return {"status": "success", "message": f"Files injected into {target_mount}"}
            else:
                return {"status": "failed", "error": f"External path {external_path} not found"}
        
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def get_mount_info(self) -> Dict:
        """Get information about all mount points"""
        return {
            "mount_points": [
                {
                    "local_path": mp.local_path,
                    "external_path": mp.external_path,
                    "sync_enabled": mp.sync_enabled,
                    "watch_enabled": mp.watch_enabled,
                    "exists": os.path.exists(mp.local_path)
                }
                for mp in self.mount_points
            ],
            "deployment_targets": [
                {
                    "name": target.name,
                    "type": target.type,
                    "auto_deploy": target.auto_deploy
                }
                for target in self.deployment_targets
            ]
        }
    
    def cleanup(self):
        """Cleanup watchers and resources"""
        for observer in self.observers:
            observer.stop()
            observer.join()

# Example usage
if __name__ == "__main__":
    bridge = FileSystemBridge()
    
    print("File System Bridge initialized")
    print("Mount points:", bridge.get_mount_info())
    
    # Keep running to watch for file changes
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bridge.cleanup()
        print("File System Bridge stopped")

