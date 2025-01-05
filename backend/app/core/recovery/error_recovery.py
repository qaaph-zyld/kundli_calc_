"""
Error Recovery System for House Analysis Engine
PGF Protocol: ERS_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
import pickle
from functools import wraps

@dataclass
class CalculationState:
    """Represents the state of a calculation at a specific point"""
    calculation_id: str
    timestamp: datetime
    phase: str
    input_data: Dict[str, Any]
    intermediate_results: Dict[str, Any]
    completed_steps: List[str]
    resources: Dict[str, float]
    status: str

class ErrorRecoverySystem:
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.active_calculations: Dict[str, CalculationState] = {}
        self.logger = logging.getLogger(__name__)
        
    async def create_checkpoint(
        self,
        calculation_id: str,
        state: CalculationState
    ) -> bool:
        """Create a checkpoint for the current calculation state"""
        try:
            checkpoint_path = self._get_checkpoint_path(calculation_id)
            
            # Serialize state
            with open(checkpoint_path, 'wb') as f:
                pickle.dump(state, f)
            
            self.logger.info(
                f"Checkpoint created for calculation {calculation_id}"
            )
            return True
            
        except Exception as e:
            self.logger.error(
                f"Failed to create checkpoint for {calculation_id}: {str(e)}"
            )
            return False
    
    async def restore_checkpoint(
        self,
        calculation_id: str
    ) -> Optional[CalculationState]:
        """Restore calculation state from checkpoint"""
        try:
            checkpoint_path = self._get_checkpoint_path(calculation_id)
            
            if not checkpoint_path.exists():
                self.logger.warning(
                    f"No checkpoint found for calculation {calculation_id}"
                )
                return None
            
            # Deserialize state
            with open(checkpoint_path, 'rb') as f:
                state = pickle.load(f)
            
            self.logger.info(
                f"Checkpoint restored for calculation {calculation_id}"
            )
            return state
            
        except Exception as e:
            self.logger.error(
                f"Failed to restore checkpoint for {calculation_id}: {str(e)}"
            )
            return None
    
    def _get_checkpoint_path(self, calculation_id: str) -> Path:
        """Get path for checkpoint file"""
        return self.checkpoint_dir / f"{calculation_id}.checkpoint"
    
    async def cleanup_checkpoints(
        self,
        max_age_hours: int = 24
    ) -> int:
        """Clean up old checkpoints"""
        try:
            current_time = datetime.now()
            cleaned = 0
            
            for checkpoint in self.checkpoint_dir.glob("*.checkpoint"):
                if (current_time - datetime.fromtimestamp(checkpoint.stat().st_mtime)
                    ).total_seconds() > max_age_hours * 3600:
                    checkpoint.unlink()
                    cleaned += 1
            
            self.logger.info(f"Cleaned up {cleaned} old checkpoints")
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Checkpoint cleanup failed: {str(e)}")
            return 0

def with_error_recovery(recovery_system: ErrorRecoverySystem):
    """Decorator for automatic error recovery"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            calculation_id = kwargs.get('calculation_id', str(datetime.now().timestamp()))
            
            try:
                # Create initial state
                state = CalculationState(
                    calculation_id=calculation_id,
                    timestamp=datetime.now(),
                    phase="started",
                    input_data=kwargs,
                    intermediate_results={},
                    completed_steps=[],
                    resources={},
                    status="running"
                )
                
                # Save initial checkpoint
                await recovery_system.create_checkpoint(calculation_id, state)
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Update state with success
                state.status = "completed"
                state.intermediate_results['final_result'] = result
                await recovery_system.create_checkpoint(calculation_id, state)
                
                return result
                
            except Exception as e:
                # Update state with error
                state.status = "failed"
                state.intermediate_results['error'] = str(e)
                await recovery_system.create_checkpoint(calculation_id, state)
                
                # Attempt recovery
                recovered_state = await recovery_system.restore_checkpoint(calculation_id)
                if recovered_state and recovered_state.status != "failed":
                    # Retry calculation from last good state
                    kwargs.update(recovered_state.input_data)
                    return await wrapper(*args, **kwargs)
                
                raise
                
        return wrapper
    return decorator

class TransactionLog:
    """Maintains a log of calculation transactions"""
    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    async def log_transaction(
        self,
        calculation_id: str,
        action: str,
        details: Dict[str, Any]
    ) -> bool:
        """Log a calculation transaction"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'calculation_id': calculation_id,
                'action': action,
                'details': details
            }
            
            log_path = self.log_dir / f"{calculation_id}.log"
            
            with open(log_path, 'a') as f:
                json.dump(log_entry, f)
                f.write('\n')
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to log transaction: {str(e)}")
            return False
    
    async def get_transaction_history(
        self,
        calculation_id: str
    ) -> List[Dict[str, Any]]:
        """Retrieve transaction history for a calculation"""
        try:
            log_path = self.log_dir / f"{calculation_id}.log"
            
            if not log_path.exists():
                return []
            
            history = []
            with open(log_path, 'r') as f:
                for line in f:
                    if line.strip():
                        history.append(json.loads(line))
            
            return history
            
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve transaction history: {str(e)}"
            )
            return []

class RecoveryManager:
    """Manages error recovery and transaction logging"""
    def __init__(
        self,
        checkpoint_dir: str = "./checkpoints",
        log_dir: str = "./logs"
    ):
        self.recovery_system = ErrorRecoverySystem(checkpoint_dir)
        self.transaction_log = TransactionLog(log_dir)
    
    async def start_calculation(
        self,
        calculation_id: str,
        input_data: Dict[str, Any]
    ) -> str:
        """Start a new calculation with recovery support"""
        try:
            # Create initial state
            state = CalculationState(
                calculation_id=calculation_id,
                timestamp=datetime.now(),
                phase="started",
                input_data=input_data,
                intermediate_results={},
                completed_steps=[],
                resources={},
                status="running"
            )
            
            # Create checkpoint
            await self.recovery_system.create_checkpoint(calculation_id, state)
            
            # Log transaction
            await self.transaction_log.log_transaction(
                calculation_id,
                "start",
                {"input_data": input_data}
            )
            
            return calculation_id
            
        except Exception as e:
            self.logger.error(f"Failed to start calculation: {str(e)}")
            raise
    
    async def update_calculation_state(
        self,
        calculation_id: str,
        phase: str,
        results: Dict[str, Any],
        completed_step: str
    ) -> bool:
        """Update calculation state with new results"""
        try:
            # Restore current state
            state = await self.recovery_system.restore_checkpoint(calculation_id)
            if not state:
                raise ValueError(f"No state found for calculation {calculation_id}")
            
            # Update state
            state.phase = phase
            state.intermediate_results.update(results)
            state.completed_steps.append(completed_step)
            state.timestamp = datetime.now()
            
            # Create new checkpoint
            await self.recovery_system.create_checkpoint(calculation_id, state)
            
            # Log transaction
            await self.transaction_log.log_transaction(
                calculation_id,
                "update",
                {
                    "phase": phase,
                    "completed_step": completed_step,
                    "results": results
                }
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update calculation state: {str(e)}")
            return False
    
    async def complete_calculation(
        self,
        calculation_id: str,
        final_results: Dict[str, Any]
    ) -> bool:
        """Mark calculation as completed"""
        try:
            # Restore current state
            state = await self.recovery_system.restore_checkpoint(calculation_id)
            if not state:
                raise ValueError(f"No state found for calculation {calculation_id}")
            
            # Update state
            state.status = "completed"
            state.intermediate_results['final_results'] = final_results
            state.timestamp = datetime.now()
            
            # Create final checkpoint
            await self.recovery_system.create_checkpoint(calculation_id, state)
            
            # Log transaction
            await self.transaction_log.log_transaction(
                calculation_id,
                "complete",
                {"final_results": final_results}
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete calculation: {str(e)}")
            return False
    
    async def handle_error(
        self,
        calculation_id: str,
        error: Exception
    ) -> Optional[CalculationState]:
        """Handle calculation error and attempt recovery"""
        try:
            # Log error
            await self.transaction_log.log_transaction(
                calculation_id,
                "error",
                {"error": str(error)}
            )
            
            # Attempt recovery
            state = await self.recovery_system.restore_checkpoint(calculation_id)
            if not state:
                return None
            
            # Log recovery attempt
            await self.transaction_log.log_transaction(
                calculation_id,
                "recovery_attempt",
                {"recovered_state": state.__dict__}
            )
            
            return state
            
        except Exception as e:
            self.logger.error(f"Failed to handle error: {str(e)}")
            return None
