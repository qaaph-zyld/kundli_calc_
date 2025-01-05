"""
Service Deployment Manifests
PGF Protocol: DEPL_004
Gate: GATE_28
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union
import os
import yaml
from pathlib import Path
from .strategies import (
    DeploymentMode,
    DeploymentStrategy
)
from .templates import (
    get_deployment_template,
    get_service_template,
    get_deployment_spec,
    get_container_spec,
    get_resource_requirements
)

class ManifestGenerator:
    """Manifest generator"""
    
    def __init__(
        self,
        mode: DeploymentMode = DeploymentMode.DEVELOPMENT,
        strategy: DeploymentStrategy = DeploymentStrategy.ROLLING
    ):
        """Initialize generator"""
        self.mode = mode
        self.strategy = strategy
    
    def generate_manifests(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate deployment manifests"""
        # Get base templates
        templates = get_deployment_template(
            self.mode,
            self.strategy
        )
        
        # Generate service manifest
        service_manifest = self._generate_service_manifest(
            templates["service"],
            config
        )
        
        # Generate deployment manifest
        deployment_manifest = self._generate_deployment_manifest(
            templates["deployment"],
            config
        )
        
        # Generate additional manifests
        additional_manifests = self._generate_additional_manifests(
            config
        )
        
        return {
            "service": service_manifest,
            "deployment": deployment_manifest,
            **additional_manifests
        }
    
    def _generate_service_manifest(
        self,
        template: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate service manifest"""
        manifest = template.copy()
        
        # Update metadata
        if "name" in config:
            manifest["metadata"]["name"] = config["name"]
        
        if "namespace" in config:
            manifest["metadata"]["namespace"] = config["namespace"]
        
        if "labels" in config:
            manifest["metadata"]["labels"].update(config["labels"])
        
        # Update spec
        if "ports" in config:
            manifest["spec"]["ports"] = config["ports"]
        
        if "type" in config:
            manifest["spec"]["type"] = config["type"]
        
        return manifest
    
    def _generate_deployment_manifest(
        self,
        template: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate deployment manifest"""
        manifest = template.copy()
        
        # Update metadata
        if "name" in config:
            manifest["metadata"]["name"] = config["name"]
        
        if "namespace" in config:
            manifest["metadata"]["namespace"] = config["namespace"]
        
        if "labels" in config:
            manifest["metadata"]["labels"].update(config["labels"])
        
        # Update spec
        if "replicas" in config:
            manifest["spec"]["replicas"] = config["replicas"]
        
        if "strategy" in config:
            manifest["spec"]["strategy"] = config["strategy"]
        
        # Update container spec
        container = manifest["spec"]["template"]["spec"]["containers"][0]
        
        if "image" in config:
            container["image"] = config["image"]
        
        if "env" in config:
            container["env"] = config["env"]
        
        if "resources" in config:
            container["resources"] = config["resources"]
        
        if "probes" in config:
            if "liveness" in config["probes"]:
                container["livenessProbe"] = config["probes"]["liveness"]
            if "readiness" in config["probes"]:
                container["readinessProbe"] = config["probes"]["readiness"]
        
        return manifest
    
    def _generate_additional_manifests(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate additional manifests"""
        manifests = {}
        
        # Generate config maps
        if "configMaps" in config:
            manifests["configMaps"] = self._generate_config_maps(
                config["configMaps"]
            )
        
        # Generate secrets
        if "secrets" in config:
            manifests["secrets"] = self._generate_secrets(
                config["secrets"]
            )
        
        # Generate ingress
        if "ingress" in config:
            manifests["ingress"] = self._generate_ingress(
                config["ingress"]
            )
        
        # Generate horizontal pod autoscaler
        if "autoscaling" in config:
            manifests["hpa"] = self._generate_hpa(
                config["autoscaling"]
            )
        
        return manifests
    
    def _generate_config_maps(
        self,
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate config maps"""
        config_maps = []
        
        for name, data in config.items():
            config_map = {
                "apiVersion": "v1",
                "kind": "ConfigMap",
                "metadata": {
                    "name": name,
                    "namespace": data.get("namespace", "default")
                },
                "data": data.get("data", {})
            }
            config_maps.append(config_map)
        
        return config_maps
    
    def _generate_secrets(
        self,
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate secrets"""
        secrets = []
        
        for name, data in config.items():
            secret = {
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {
                    "name": name,
                    "namespace": data.get("namespace", "default")
                },
                "type": data.get("type", "Opaque"),
                "data": data.get("data", {})
            }
            secrets.append(secret)
        
        return secrets
    
    def _generate_ingress(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate ingress"""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": config.get("name", "kundli-ingress"),
                "namespace": config.get("namespace", "default"),
                "annotations": config.get("annotations", {})
            },
            "spec": {
                "rules": config.get("rules", []),
                "tls": config.get("tls", [])
            }
        }
    
    def _generate_hpa(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate horizontal pod autoscaler"""
        return {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": config.get("name", "kundli-hpa"),
                "namespace": config.get("namespace", "default")
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": config.get("targetName", "kundli-service")
                },
                "minReplicas": config.get("minReplicas", 1),
                "maxReplicas": config.get("maxReplicas", 10),
                "metrics": config.get("metrics", [])
            }
        }

class ManifestWriter:
    """Manifest writer"""
    
    def __init__(
        self,
        output_dir: Union[str, Path]
    ):
        """Initialize writer"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def write_manifests(
        self,
        manifests: Dict[str, Any]
    ):
        """Write manifests to files"""
        # Write service manifest
        if "service" in manifests:
            self._write_manifest(
                "service.yaml",
                manifests["service"]
            )
        
        # Write deployment manifest
        if "deployment" in manifests:
            self._write_manifest(
                "deployment.yaml",
                manifests["deployment"]
            )
        
        # Write config maps
        if "configMaps" in manifests:
            for i, config_map in enumerate(manifests["configMaps"]):
                self._write_manifest(
                    f"configmap-{i+1}.yaml",
                    config_map
                )
        
        # Write secrets
        if "secrets" in manifests:
            for i, secret in enumerate(manifests["secrets"]):
                self._write_manifest(
                    f"secret-{i+1}.yaml",
                    secret
                )
        
        # Write ingress
        if "ingress" in manifests:
            self._write_manifest(
                "ingress.yaml",
                manifests["ingress"]
            )
        
        # Write HPA
        if "hpa" in manifests:
            self._write_manifest(
                "hpa.yaml",
                manifests["hpa"]
            )
    
    def _write_manifest(
        self,
        filename: str,
        manifest: Dict[str, Any]
    ):
        """Write manifest to file"""
        filepath = self.output_dir / filename
        
        with open(filepath, "w") as f:
            yaml.safe_dump(
                manifest,
                f,
                default_flow_style=False
            )
