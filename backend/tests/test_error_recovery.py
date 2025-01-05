"""
Test Suite for Error Recovery System
PGF Protocol: ERS_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from app.core.recovery.error_recovery import (
    ErrorRecoverySystem,
    CalculationState,
    TransactionLog,
    RecoveryManager,
    with_error_recovery
)

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def recovery_system(temp_dir):
    return ErrorRecoverySystem(str(temp_dir / "checkpoints"))

@pytest.fixture
def transaction_log(temp_dir):
    return TransactionLog(str(temp_dir / "logs"))

@pytest.fixture
def recovery_manager(temp_dir):
    return RecoveryManager(
        str(temp_dir / "checkpoints"),
        str(temp_dir / "logs")
    )

@pytest.fixture
def sample_state():
    return CalculationState(
        calculation_id="test_calc_001",
        timestamp=datetime.now(),
        phase="testing",
        input_data={"test": "data"},
        intermediate_results={},
        completed_steps=[],
        resources={},
        status="running"
    )

@pytest.mark.asyncio
async def test_checkpoint_creation(recovery_system, sample_state):
    """Test checkpoint creation and restoration"""
    # Create checkpoint
    success = await recovery_system.create_checkpoint(
        sample_state.calculation_id,
        sample_state
    )
    assert success
    
    # Restore checkpoint
    restored_state = await recovery_system.restore_checkpoint(
        sample_state.calculation_id
    )
    assert restored_state is not None
    assert restored_state.calculation_id == sample_state.calculation_id
    assert restored_state.phase == sample_state.phase

@pytest.mark.asyncio
async def test_checkpoint_cleanup(recovery_system, sample_state):
    """Test cleanup of old checkpoints"""
    # Create checkpoint
    await recovery_system.create_checkpoint(
        sample_state.calculation_id,
        sample_state
    )
    
    # Modify file timestamp to be old
    checkpoint_path = recovery_system._get_checkpoint_path(
        sample_state.calculation_id
    )
    old_time = datetime.now() - timedelta(hours=25)
    checkpoint_path.touch(exist_ok=True)
    
    # Run cleanup
    cleaned = await recovery_system.cleanup_checkpoints(max_age_hours=24)
    assert cleaned == 1
    assert not checkpoint_path.exists()

@pytest.mark.asyncio
async def test_transaction_logging(transaction_log):
    """Test transaction logging and retrieval"""
    calc_id = "test_calc_002"
    
    # Log transactions
    success = await transaction_log.log_transaction(
        calc_id,
        "start",
        {"input": "test"}
    )
    assert success
    
    success = await transaction_log.log_transaction(
        calc_id,
        "update",
        {"progress": 50}
    )
    assert success
    
    # Retrieve history
    history = await transaction_log.get_transaction_history(calc_id)
    assert len(history) == 2
    assert history[0]['action'] == "start"
    assert history[1]['action'] == "update"

@pytest.mark.asyncio
async def test_recovery_manager_workflow(recovery_manager):
    """Test complete workflow with RecoveryManager"""
    calc_id = "test_calc_003"
    input_data = {"test": "data"}
    
    # Start calculation
    started_id = await recovery_manager.start_calculation(
        calc_id,
        input_data
    )
    assert started_id == calc_id
    
    # Update state
    success = await recovery_manager.update_calculation_state(
        calc_id,
        "processing",
        {"intermediate": "result"},
        "step1"
    )
    assert success
    
    # Complete calculation
    success = await recovery_manager.complete_calculation(
        calc_id,
        {"final": "result"}
    )
    assert success
    
    # Verify transaction history
    history = await recovery_manager.transaction_log.get_transaction_history(
        calc_id
    )
    assert len(history) == 3
    assert history[0]['action'] == "start"
    assert history[1]['action'] == "update"
    assert history[2]['action'] == "complete"

@pytest.mark.asyncio
async def test_error_recovery_decorator(recovery_system):
    """Test error recovery decorator"""
    error_count = 0
    
    @with_error_recovery(recovery_system)
    async def test_function(calculation_id: str, should_fail: bool = False):
        nonlocal error_count
        if should_fail and error_count == 0:
            error_count += 1
            raise ValueError("Test error")
        return "success"
    
    # Test successful execution
    result = await test_function(calculation_id="test_calc_004")
    assert result == "success"
    
    # Test recovery from error
    result = await test_function(
        calculation_id="test_calc_005",
        should_fail=True
    )
    assert result == "success"
    assert error_count == 1

@pytest.mark.asyncio
async def test_error_handling(recovery_manager):
    """Test error handling and recovery"""
    calc_id = "test_calc_006"
    
    # Start calculation
    await recovery_manager.start_calculation(
        calc_id,
        {"test": "data"}
    )
    
    # Simulate error
    test_error = ValueError("Test error")
    recovered_state = await recovery_manager.handle_error(
        calc_id,
        test_error
    )
    
    assert recovered_state is not None
    assert recovered_state.calculation_id == calc_id
    
    # Verify error logged
    history = await recovery_manager.transaction_log.get_transaction_history(
        calc_id
    )
    assert any(entry['action'] == "error" for entry in history)
    assert any(entry['action'] == "recovery_attempt" for entry in history)

@pytest.mark.asyncio
async def test_concurrent_operations(recovery_manager):
    """Test concurrent operations with RecoveryManager"""
    async def run_calculation(calc_id: str):
        await recovery_manager.start_calculation(
            calc_id,
            {"test": "data"}
        )
        await recovery_manager.update_calculation_state(
            calc_id,
            "processing",
            {"progress": 50},
            "step1"
        )
        await recovery_manager.complete_calculation(
            calc_id,
            {"result": "success"}
        )
    
    # Run multiple calculations concurrently
    tasks = [
        run_calculation(f"concurrent_calc_{i}")
        for i in range(5)
    ]
    
    await asyncio.gather(*tasks)
    
    # Verify all calculations completed
    for i in range(5):
        history = await recovery_manager.transaction_log.get_transaction_history(
            f"concurrent_calc_{i}"
        )
        assert len(history) == 3
        assert history[-1]['action'] == "complete"
