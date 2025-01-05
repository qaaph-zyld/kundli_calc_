"""
Deployment Framework
PGF Protocol: DEP_001
Gate: GATE_9
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import subprocess
import shutil
import os
from pathlib import Path
import yaml
import json
import logging
import docker
from docker.models.containers import Container
from docker.models.images import Image

class DeploymentEnvironment(str, Enum):
    """Deployment environments"""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class DeploymentMode(str, Enum):
    """Deployment modes"""
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    SERVERLESS = "serverless"
    BARE_METAL = "bare_metal"

class ServiceType(str, Enum):
    """Service types"""
    API = "api"
    WORKER = "worker"
    CACHE = "cache"
    DATABASE = "database"
    FRONTEND = "frontend"

class ResourceRequirements(BaseModel):
    """Resource requirements"""
    
    cpu: str = "100m"
    memory: str = "128Mi"
    storage: Optional[str] = None
    replicas: int = 1
    min_replicas: Optional[int] = None
    max_replicas: Optional[int] = None

class HealthCheck(BaseModel):
    """Health check configuration"""
    
    path: str = "/health"
    port: int = 8000
    initial_delay: int = 30
    period: int = 10
    timeout: int = 5
    success_threshold: int = 1
    failure_threshold: int = 3

class ServiceConfig(BaseModel):
    """Service configuration"""
    
    name: str
    type: ServiceType
    image: str
    tag: str = "latest"
    port: int
    env_vars: Dict[str, str] = Field(default_factory=dict)
    secrets: List[str] = Field(default_factory=list)
    resources: ResourceRequirements
    health_check: HealthCheck
    dependencies: List[str] = Field(default_factory=list)
    volumes: Dict[str, str] = Field(default_factory=dict)

class DeploymentConfig(BaseModel):
    """Deployment configuration"""
    
    environment: DeploymentEnvironment
    mode: DeploymentMode
    services: Dict[str, ServiceConfig]
    global_env_vars: Dict[str, str] = Field(default_factory=dict)
    global_secrets: List[str] = Field(default_factory=list)
    registry: Optional[str] = None
    namespace: str = "default"
    network: str = "vedic-astrology"
    monitoring: bool = True
    logging: bool = True

class DeploymentManager:
    """Deployment manager for service orchestration"""
    
    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.docker_client = docker.from_env()
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("deployment.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def deploy(self) -> Dict[str, Any]:
        """Deploy services based on configuration"""
        self.logger.info(f"Starting deployment in {self.config.environment} environment")
        
        try:
            if self.config.mode == DeploymentMode.DOCKER:
                return await self._deploy_docker()
            elif self.config.mode == DeploymentMode.KUBERNETES:
                return await self._deploy_kubernetes()
            elif self.config.mode == DeploymentMode.SERVERLESS:
                return await self._deploy_serverless()
            else:
                return await self._deploy_bare_metal()
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            raise
    
    async def _deploy_docker(self) -> Dict[str, Any]:
        """Deploy using Docker"""
        results = {}
        
        # Create network if it doesn't exist
        try:
            self.docker_client.networks.get(self.config.network)
        except docker.errors.NotFound:
            self.docker_client.networks.create(
                self.config.network,
                driver="bridge"
            )
        
        # Deploy services in dependency order
        deployed_services = set()
        while len(deployed_services) < len(self.config.services):
            for name, service in self.config.services.items():
                if name in deployed_services:
                    continue
                    
                # Check if dependencies are met
                if all(dep in deployed_services for dep in service.dependencies):
                    # Build and deploy service
                    result = await self._deploy_docker_service(name, service)
                    results[name] = result
                    deployed_services.add(name)
        
        return results
    
    async def _deploy_docker_service(
        self,
        name: str,
        service: ServiceConfig
    ) -> Dict[str, Any]:
        """Deploy Docker service"""
        self.logger.info(f"Deploying service: {name}")
        
        # Prepare environment variables
        env_vars = {
            **self.config.global_env_vars,
            **service.env_vars,
            "SERVICE_NAME": name,
            "ENVIRONMENT": self.config.environment
        }
        
        # Prepare volumes
        volumes = {}
        for src, dst in service.volumes.items():
            if src.startswith("./"):
                src = str(Path(src).resolve())
            volumes[src] = {"bind": dst, "mode": "rw"}
        
        # Pull or build image
        image = f"{service.image}:{service.tag}"
        try:
            self.docker_client.images.pull(image)
        except docker.errors.ImageNotFound:
            self.logger.warning(f"Image not found: {image}, will build locally")
            self._build_docker_image(service)
        
        # Create and start container
        container = self.docker_client.containers.run(
            image=image,
            name=f"{name}-{self.config.environment}",
            detach=True,
            environment=env_vars,
            network=self.config.network,
            ports={f"{service.port}/tcp": service.port},
            volumes=volumes,
            restart_policy={"Name": "unless-stopped"},
            healthcheck={
                "test": [
                    "CMD",
                    "curl",
                    "-f",
                    f"http://localhost:{service.health_check.port}{service.health_check.path}"
                ],
                "interval": service.health_check.period * 1000000000,
                "timeout": service.health_check.timeout * 1000000000,
                "retries": service.health_check.failure_threshold,
                "start_period": service.health_check.initial_delay * 1000000000
            }
        )
        
        return {
            "container_id": container.id,
            "status": container.status,
            "image": image,
            "ports": container.ports,
            "network": self.config.network
        }
    
    def _build_docker_image(self, service: ServiceConfig) -> None:
        """Build Docker image"""
        dockerfile_path = Path(f"docker/{service.type}/Dockerfile")
        if not dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
        
        self.docker_client.images.build(
            path=".",
            dockerfile=str(dockerfile_path),
            tag=f"{service.image}:{service.tag}"
        )
    
    async def _deploy_kubernetes(self) -> Dict[str, Any]:
        """Deploy using Kubernetes"""
        # Generate Kubernetes manifests
        manifests = self._generate_k8s_manifests()
        
        # Apply manifests
        results = {}
        for name, manifest in manifests.items():
            manifest_path = Path(f"k8s/{name}.yaml")
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(manifest_path, "w") as f:
                yaml.dump(manifest, f)
            
            # Apply manifest using kubectl
            result = subprocess.run(
                ["kubectl", "apply", "-f", str(manifest_path)],
                capture_output=True,
                text=True
            )
            
            results[name] = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        
        return results
    
    def _generate_k8s_manifests(self) -> Dict[str, Any]:
        """Generate Kubernetes manifests"""
        manifests = {}
        
        for name, service in self.config.services.items():
            # Deployment
            deployment = {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": {
                    "name": name,
                    "namespace": self.config.namespace
                },
                "spec": {
                    "replicas": service.resources.replicas,
                    "selector": {
                        "matchLabels": {"app": name}
                    },
                    "template": {
                        "metadata": {
                            "labels": {"app": name}
                        },
                        "spec": {
                            "containers": [{
                                "name": name,
                                "image": f"{service.image}:{service.tag}",
                                "ports": [{
                                    "containerPort": service.port
                                }],
                                "env": [
                                    {"name": k, "value": v}
                                    for k, v in {
                                        **self.config.global_env_vars,
                                        **service.env_vars
                                    }.items()
                                ],
                                "resources": {
                                    "requests": {
                                        "cpu": service.resources.cpu,
                                        "memory": service.resources.memory
                                    },
                                    "limits": {
                                        "cpu": service.resources.cpu,
                                        "memory": service.resources.memory
                                    }
                                },
                                "livenessProbe": {
                                    "httpGet": {
                                        "path": service.health_check.path,
                                        "port": service.health_check.port
                                    },
                                    "initialDelaySeconds": service.health_check.initial_delay,
                                    "periodSeconds": service.health_check.period,
                                    "timeoutSeconds": service.health_check.timeout,
                                    "successThreshold": service.health_check.success_threshold,
                                    "failureThreshold": service.health_check.failure_threshold
                                }
                            }]
                        }
                    }
                }
            }
            
            # Service
            service_manifest = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": name,
                    "namespace": self.config.namespace
                },
                "spec": {
                    "selector": {"app": name},
                    "ports": [{
                        "protocol": "TCP",
                        "port": service.port,
                        "targetPort": service.port
                    }]
                }
            }
            
            manifests[f"{name}-deployment"] = deployment
            manifests[f"{name}-service"] = service_manifest
            
            # Horizontal Pod Autoscaler if configured
            if service.resources.min_replicas and service.resources.max_replicas:
                hpa = {
                    "apiVersion": "autoscaling/v2",
                    "kind": "HorizontalPodAutoscaler",
                    "metadata": {
                        "name": name,
                        "namespace": self.config.namespace
                    },
                    "spec": {
                        "scaleTargetRef": {
                            "apiVersion": "apps/v1",
                            "kind": "Deployment",
                            "name": name
                        },
                        "minReplicas": service.resources.min_replicas,
                        "maxReplicas": service.resources.max_replicas,
                        "metrics": [{
                            "type": "Resource",
                            "resource": {
                                "name": "cpu",
                                "target": {
                                    "type": "Utilization",
                                    "averageUtilization": 80
                                }
                            }
                        }]
                    }
                }
                manifests[f"{name}-hpa"] = hpa
        
        return manifests
    
    async def _deploy_serverless(self) -> Dict[str, Any]:
        """Deploy using serverless framework"""
        # Generate serverless.yml
        serverless_config = self._generate_serverless_config()
        
        with open("serverless.yml", "w") as f:
            yaml.dump(serverless_config, f)
        
        # Deploy using serverless framework
        result = subprocess.run(
            ["serverless", "deploy", "--stage", self.config.environment],
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def _generate_serverless_config(self) -> Dict[str, Any]:
        """Generate serverless.yml configuration"""
        return {
            "service": "vedic-astrology",
            "provider": {
                "name": "aws",
                "runtime": "python3.9",
                "stage": self.config.environment,
                "region": "us-west-2",
                "environment": self.config.global_env_vars
            },
            "functions": {
                name: {
                    "handler": f"app.handlers.{name}.handler",
                    "events": [{
                        "http": {
                            "path": f"/{name}",
                            "method": "any"
                        }
                    }],
                    "environment": service.env_vars,
                    "memorySize": int(service.resources.memory.replace("Mi", "")),
                    "timeout": 30
                }
                for name, service in self.config.services.items()
                if service.type == ServiceType.API
            }
        }
    
    async def _deploy_bare_metal(self) -> Dict[str, Any]:
        """Deploy on bare metal"""
        results = {}
        
        for name, service in self.config.services.items():
            # Create service directory
            service_dir = Path(f"/opt/vedic-astrology/{name}")
            service_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy application files
            src_dir = Path(f"services/{name}")
            if src_dir.exists():
                shutil.copytree(
                    src_dir,
                    service_dir,
                    dirs_exist_ok=True
                )
            
            # Create systemd service
            service_file = f"""[Unit]
Description={name} service
After=network.target

[Service]
Type=simple
User=vedic
WorkingDirectory={service_dir}
Environment=PYTHONPATH={service_dir}
{"".join(f'Environment={k}={v}\\n' for k, v in service.env_vars.items())}
ExecStart=/usr/local/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port {service.port}
Restart=always

[Install]
WantedBy=multi-user.target
"""
            
            service_path = Path(f"/etc/systemd/system/{name}.service")
            with open(service_path, "w") as f:
                f.write(service_file)
            
            # Start service
            subprocess.run(["systemctl", "daemon-reload"])
            subprocess.run(["systemctl", "enable", f"{name}.service"])
            result = subprocess.run(
                ["systemctl", "start", f"{name}.service"],
                capture_output=True,
                text=True
            )
            
            results[name] = {
                "success": result.returncode == 0,
                "service_file": str(service_path),
                "error": result.stderr if result.returncode != 0 else None
            }
        
        return results
