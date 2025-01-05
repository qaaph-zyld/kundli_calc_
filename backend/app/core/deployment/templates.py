"""
Service Deployment Templates
PGF Protocol: DEPL_003
Gate: GATE_28
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List
from .strategies import (
    DeploymentMode,
    DeploymentStrategy
)

# Base service template
BASE_SERVICE_TEMPLATE = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "kundli-service",
        "namespace": "default",
        "labels": {
            "app": "kundli-service",
            "tier": "backend"
        }
    },
    "spec": {
        "selector": {
            "app": "kundli-service"
        },
        "ports": [
            {
                "protocol": "TCP",
                "port": 8000,
                "targetPort": 8000
            }
        ],
        "type": "ClusterIP"
    }
}

# Base deployment template
BASE_DEPLOYMENT_TEMPLATE = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "kundli-service",
        "namespace": "default",
        "labels": {
            "app": "kundli-service",
            "tier": "backend"
        }
    },
    "spec": {
        "replicas": 3,
        "selector": {
            "matchLabels": {
                "app": "kundli-service"
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "kundli-service"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "kundli-service",
                        "image": "kundli-service:latest",
                        "ports": [
                            {
                                "containerPort": 8000
                            }
                        ],
                        "resources": {
                            "requests": {
                                "cpu": "100m",
                                "memory": "128Mi"
                            },
                            "limits": {
                                "cpu": "500m",
                                "memory": "512Mi"
                            }
                        },
                        "livenessProbe": {
                            "httpGet": {
                                "path": "/health",
                                "port": 8000
                            },
                            "initialDelaySeconds": 30,
                            "periodSeconds": 10
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/ready",
                                "port": 8000
                            },
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5
                        }
                    }
                ]
            }
        }
    }
}

# Mode-specific templates
MODE_TEMPLATES = {
    DeploymentMode.LOCAL: {
        "service": {
            **BASE_SERVICE_TEMPLATE,
            "spec": {
                **BASE_SERVICE_TEMPLATE["spec"],
                "type": "NodePort"
            }
        },
        "deployment": {
            **BASE_DEPLOYMENT_TEMPLATE,
            "spec": {
                **BASE_DEPLOYMENT_TEMPLATE["spec"],
                "replicas": 1
            }
        }
    },
    DeploymentMode.DEVELOPMENT: {
        "service": BASE_SERVICE_TEMPLATE,
        "deployment": BASE_DEPLOYMENT_TEMPLATE
    },
    DeploymentMode.STAGING: {
        "service": {
            **BASE_SERVICE_TEMPLATE,
            "metadata": {
                **BASE_SERVICE_TEMPLATE["metadata"],
                "namespace": "staging"
            }
        },
        "deployment": {
            **BASE_DEPLOYMENT_TEMPLATE,
            "metadata": {
                **BASE_DEPLOYMENT_TEMPLATE["metadata"],
                "namespace": "staging"
            },
            "spec": {
                **BASE_DEPLOYMENT_TEMPLATE["spec"],
                "replicas": 2
            }
        }
    },
    DeploymentMode.PRODUCTION: {
        "service": {
            **BASE_SERVICE_TEMPLATE,
            "metadata": {
                **BASE_SERVICE_TEMPLATE["metadata"],
                "namespace": "production"
            },
            "spec": {
                **BASE_SERVICE_TEMPLATE["spec"],
                "type": "LoadBalancer"
            }
        },
        "deployment": {
            **BASE_DEPLOYMENT_TEMPLATE,
            "metadata": {
                **BASE_DEPLOYMENT_TEMPLATE["metadata"],
                "namespace": "production"
            },
            "spec": {
                **BASE_DEPLOYMENT_TEMPLATE["spec"],
                "replicas": 5,
                "template": {
                    **BASE_DEPLOYMENT_TEMPLATE["spec"]["template"],
                    "spec": {
                        **BASE_DEPLOYMENT_TEMPLATE["spec"]["template"]["spec"],
                        "containers": [
                            {
                                **BASE_DEPLOYMENT_TEMPLATE["spec"]["template"]["spec"]["containers"][0],
                                "resources": {
                                    "requests": {
                                        "cpu": "500m",
                                        "memory": "512Mi"
                                    },
                                    "limits": {
                                        "cpu": "2",
                                        "memory": "2Gi"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
}

# Strategy-specific templates
STRATEGY_TEMPLATES = {
    DeploymentStrategy.ROLLING: {
        "deployment": {
            "spec": {
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {
                        "maxSurge": 1,
                        "maxUnavailable": 0
                    }
                }
            }
        }
    },
    DeploymentStrategy.BLUE_GREEN: {
        "service": {
            "metadata": {
                "labels": {
                    "version": "blue"
                }
            }
        },
        "deployment": {
            "metadata": {
                "labels": {
                    "version": "blue"
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "version": "blue"
                        }
                    }
                }
            }
        }
    },
    DeploymentStrategy.CANARY: {
        "service": {
            "metadata": {
                "labels": {
                    "version": "stable"
                }
            }
        },
        "deployment": {
            "metadata": {
                "labels": {
                    "version": "stable"
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "version": "stable"
                        }
                    }
                }
            }
        }
    }
}

def get_deployment_template(
    mode: DeploymentMode,
    strategy: DeploymentStrategy
) -> Dict[str, Any]:
    """Get deployment template for mode and strategy"""
    
    # Get base template for mode
    template = MODE_TEMPLATES[mode].copy()
    
    # Apply strategy-specific configuration
    strategy_config = STRATEGY_TEMPLATES[strategy]
    
    # Merge service configuration
    if "service" in strategy_config:
        template["service"] = {
            **template["service"],
            **strategy_config["service"]
        }
    
    # Merge deployment configuration
    if "deployment" in strategy_config:
        template["deployment"] = {
            **template["deployment"],
            **strategy_config["deployment"]
        }
    
    return template

def get_service_template(
    mode: DeploymentMode
) -> Dict[str, Any]:
    """Get service template for mode"""
    return MODE_TEMPLATES[mode]["service"]

def get_deployment_spec(
    mode: DeploymentMode,
    strategy: DeploymentStrategy
) -> Dict[str, Any]:
    """Get deployment spec for mode and strategy"""
    return MODE_TEMPLATES[mode]["deployment"]["spec"]

def get_container_spec(
    mode: DeploymentMode
) -> Dict[str, Any]:
    """Get container spec for mode"""
    return MODE_TEMPLATES[mode]["deployment"]["spec"]["template"]["spec"]["containers"][0]

def get_resource_requirements(
    mode: DeploymentMode
) -> Dict[str, Any]:
    """Get resource requirements for mode"""
    return MODE_TEMPLATES[mode]["deployment"]["spec"]["template"]["spec"]["containers"][0]["resources"]
