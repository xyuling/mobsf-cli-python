"""Tests for error handling."""

import pytest
from mobsf_core.error import MobsfError, ErrorCause
from cli.error import AppError


def test_mobsf_error_creation():
    """Test MobsfError creation."""
    error = MobsfError(
        cause=ErrorCause.HTTP_CLIENT_ERROR,
        message="Test error",
    )
    
    assert error.cause == ErrorCause.HTTP_CLIENT_ERROR
    assert error.message == "Test error"
    assert "HttpClientError" in str(error)


def test_mobsf_error_with_status_code():
    """Test MobsfError with status code."""
    error = MobsfError(
        cause=ErrorCause.INVALID_HTTP_RESPONSE,
        message="Not found",
        status_code=404,
    )
    
    assert error.status_code == 404
    assert "404" in str(error)


def test_app_error_from_mobsf_error():
    """Test AppError creation from MobsfError."""
    mobsf_error = MobsfError(
        cause=ErrorCause.IO_ERROR,
        message="File not found",
    )
    
    app_error = AppError.from_mobsf_error(mobsf_error)
    
    assert isinstance(app_error, AppError)
    assert "IoError" in str(app_error)
