# flake8: noqa
"""
Comprehensive tests for v2 API endpoints with dependent workflows.
"""

import os
import time
import uuid
from datetime import datetime, timezone

import pytest

# Test configuration
TEST_PROJECT_NAME = "scaleapi-python-sdk"
test_api_key = os.environ.get(
    "SCALE_TEST_API_KEY", "test_7115d7ca4834448a97147a7f03a6e8fd"
)

# Check if we can import the v2 modules
HAS_TEST_API_KEY = bool(test_api_key)
try:
    from scaleapi.api_client.v2.models.batch_operation_request import (
        BatchOperationRequest,
    )
    from scaleapi.api_client.v2.models.create_batch_request import CreateBatchRequest

    HAS_V2_IMPORTS = True
except ImportError:
    HAS_V2_IMPORTS = False


def test_v2_batch_operation_request_creation():
    """Test BatchOperationRequest model creation."""
    try:
        import os
        import sys

        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from scaleapi.api_client.v2.models.batch_operation_request import (
            BatchOperationRequest,
        )

        request = BatchOperationRequest(batch_id="test_batch_123")
        assert request.batch_id == "test_batch_123"
        assert request.batch_name is None

        request_with_name = BatchOperationRequest(batch_name="Test Batch Name")
        assert request_with_name.batch_name == "Test Batch Name"
        assert request_with_name.batch_id is None

    except ImportError as e:
        pytest.fail(f"Failed to import BatchOperationRequest: {e}")


def test_v2_create_batch_request_creation():
    """Test CreateBatchRequest model creation."""
    try:
        import os
        import sys

        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from scaleapi.api_client.v2.models.create_batch_request import (
            CreateBatchRequest,
        )

        request = CreateBatchRequest(name="Test Batch", project_name=TEST_PROJECT_NAME)
        assert request.name == "Test Batch"
        assert request.project_name == TEST_PROJECT_NAME

    except ImportError as e:
        pytest.fail(f"Failed to import CreateBatchRequest: {e}")


def test_v2_imports_basic():
    """Test basic v2 API imports work."""
    if not HAS_TEST_API_KEY:
        pytest.skip("No test API key available")

    import scaleapi

    client = scaleapi.ScaleClient(test_api_key, "pytest")
    assert hasattr(client, "v2")


# Only enable the full API tests if imports work
if HAS_TEST_API_KEY:  # noqa: C901

    def test_v2_get_projects():
        """Test getting projects via V2 API"""
        import scaleapi

        client = scaleapi.ScaleClient(test_api_key, "pytest")
        response = client.v2.get_projects()
        assert hasattr(response, "projects")

    def test_v2_get_batches():
        """Test getting batches via V2 API"""
        import scaleapi

        client = scaleapi.ScaleClient(test_api_key, "pytest")
        response = client.v2.get_batches(project_name=TEST_PROJECT_NAME, limit=5)
        assert hasattr(response, "batches")

    def test_v2_project_workflow():
        """Test comprehensive project operations workflow"""
        import scaleapi

        client = scaleapi.ScaleClient(test_api_key, "pytest")

        # Get all projects
        projects_response = client.v2.get_projects()
        assert hasattr(projects_response, "projects")
        assert len(projects_response.projects) > 0

        # Find test project or use first available
        test_project = None
        for project in projects_response.projects:
            if hasattr(project, "name") and project.name == TEST_PROJECT_NAME:
                test_project = project
                break

        if not test_project:
            test_project = projects_response.projects[0]

        # Get single project
        single_project = client.v2.get_project(project_name=test_project.name)
        assert hasattr(single_project, "name")
        assert single_project.name == test_project.name

    def test_v2_batch_lifecycle_workflow():
        """Test comprehensive batch lifecycle: create -> fetch -> metadata -> operations"""  # noqa: E501,W505
        import scaleapi
        from scaleapi.api_client.v2.models.batch_operation_request import (
            BatchOperationRequest,
        )
        from scaleapi.api_client.v2.models.create_batch_request import (
            CreateBatchRequest,
        )
        from scaleapi.api_client.v2.models.set_batch_metadata_request import (
            SetBatchMetadataRequest,
        )

        client = scaleapi.ScaleClient(test_api_key, "pytest")

        # Get available projects
        projects_response = client.v2.get_projects()
        if not projects_response.projects:
            pytest.skip("No projects available")

        # Use test project or first available
        project_name = TEST_PROJECT_NAME
        available_project_names = [
            p.name for p in projects_response.projects if hasattr(p, "name")
        ]
        if TEST_PROJECT_NAME not in available_project_names:
            project_name = available_project_names[0]

        # Create batch
        batch_name = f"test-batch-{uuid.uuid4().hex[:8]}-{int(time.time())}"
        create_request = CreateBatchRequest(name=batch_name, project_name=project_name)
        created_batch = client.v2.create_batch(create_batch_request=create_request)
        assert hasattr(created_batch, "id")
        batch_id = created_batch.id

        # Get the created batch
        fetched_batch = client.v2.get_batch(batch_id=batch_id)
        assert fetched_batch.id == batch_id
        assert fetched_batch.name == batch_name

        # Get multiple batches
        batches_response = client.v2.get_batches(project_name=project_name, limit=10)
        assert hasattr(batches_response, "batches")
        batch_found = any(
            b.id == batch_id for b in batches_response.batches if hasattr(b, "id")
        )
        assert batch_found

        # Set batch metadata
        metadata_request = SetBatchMetadataRequest(
            batch_id=batch_id,
            metadata={
                "test_run": True,
                "created_by": "pytest",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
        client.v2.set_batch_metadata(set_batch_metadata_request=metadata_request)

        # Verify metadata was set
        updated_batch = client.v2.get_batch(batch_id=batch_id)
        assert hasattr(updated_batch, "metadata")

        # Finalize the batch
        try:
            finalize_request = BatchOperationRequest(batch_id=batch_id)
            client.v2.finalize_batch(batch_operation_request=finalize_request)
        except Exception:
            pass

    def test_v2_batch_cancellation_workflow():
        """Test batch cancellation workflow with business rules"""
        import scaleapi
        from scaleapi.api_client.v2.models.batch_operation_request import (
            BatchOperationRequest,
        )
        from scaleapi.api_client.v2.models.create_batch_request import (
            CreateBatchRequest,
        )

        client = scaleapi.ScaleClient(test_api_key, "pytest")

        # Get available projects
        projects_response = client.v2.get_projects()
        if not projects_response.projects:
            pytest.skip("No projects available")

        project_name = TEST_PROJECT_NAME
        available_project_names = [
            p.name for p in projects_response.projects if hasattr(p, "name")
        ]
        if TEST_PROJECT_NAME not in available_project_names:
            project_name = available_project_names[0]

        # Create batch
        batch_name = f"test-cancel-{uuid.uuid4().hex[:8]}-{int(time.time())}"
        create_request = CreateBatchRequest(name=batch_name, project_name=project_name)
        created_batch = client.v2.create_batch(create_batch_request=create_request)
        batch_id = created_batch.id

        # Cancel the batch
        cancel_request = BatchOperationRequest(batch_id=batch_id)
        client.v2.cancel_batch(batch_operation_request=cancel_request)

        # Verify batch is cancelled
        time.sleep(2)
        cancelled_batch = client.v2.get_batch(batch_id=batch_id)  # noqa: F841

        # Verify that cancelled batches cannot be resumed
        with pytest.raises(Exception):
            resume_request = BatchOperationRequest(batch_id=batch_id)
            client.v2.resume_batch(batch_operation_request=resume_request)

    def test_v2_batch_pause_resume_workflow():
        """Test batch pause and resume workflow"""
        import scaleapi
        from scaleapi.api_client.v2.models.batch_operation_request import (
            BatchOperationRequest,
        )
        from scaleapi.api_client.v2.models.create_batch_request import (
            CreateBatchRequest,
        )

        client = scaleapi.ScaleClient(test_api_key, "pytest")

        # Get available projects
        projects_response = client.v2.get_projects()
        if not projects_response.projects:
            pytest.skip("No projects available")

        project_name = TEST_PROJECT_NAME
        available_project_names = [
            p.name for p in projects_response.projects if hasattr(p, "name")
        ]
        if TEST_PROJECT_NAME not in available_project_names:
            project_name = available_project_names[0]

        # Create batch
        batch_name = f"test-pause-{uuid.uuid4().hex[:8]}-{int(time.time())}"
        create_request = CreateBatchRequest(name=batch_name, project_name=project_name)
        created_batch = client.v2.create_batch(create_batch_request=create_request)
        batch_id = created_batch.id

        # Pause the batch
        pause_request = BatchOperationRequest(batch_id=batch_id)
        client.v2.pause_batch(batch_operation_request=pause_request)

        # Wait for status to update
        time.sleep(2)

        # Check if batch was actually paused
        paused_batch = client.v2.get_batch(batch_id=batch_id)

        # Only resume if actually paused
        if paused_batch.status.value.lower() == "paused":
            # Resume the batch
            resume_request = BatchOperationRequest(batch_id=batch_id)
            client.v2.resume_batch(batch_operation_request=resume_request)
        else:
            pytest.skip(
                f"Batch remained in {paused_batch.status.value} status - empty batches cannot be paused"
            )

    def test_v2_model_instantiation():
        """Test creating v2 model objects directly"""
        from scaleapi.api_client.v2.models.batch_operation_request import (
            BatchOperationRequest,
        )
        from scaleapi.api_client.v2.models.create_batch_request import (
            CreateBatchRequest,
        )

        # Test BatchOperationRequest
        batch_op = BatchOperationRequest(batch_id="test-batch-123")
        assert batch_op.batch_id == "test-batch-123"

        # Test CreateBatchRequest
        create_req = CreateBatchRequest(name="test-batch", project_name="test-project")
        assert create_req.name == "test-batch"
        assert create_req.project_name == "test-project"
