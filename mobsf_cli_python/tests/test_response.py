"""Tests for response models."""

import pytest
from mobsf_core.response import (
    ErrorResponse,
    UploadResponse,
    Trackers,
    ScanResponse,
)


def test_error_response_from_dict():
    """Test ErrorResponse creation from dict."""
    data = {"error": "Invalid API key"}
    response = ErrorResponse.from_dict(data)
    
    assert response.error == "Invalid API key"
    assert str(response) == "Invalid API key"


def test_upload_response_from_dict():
    """Test UploadResponse creation from dict."""
    data = {
        "analyzer": "static_analyzer",
        "status": "success",
        "hash": "abc123",
        "scan_type": "apk",
        "file_name": "test.apk",
    }
    response = UploadResponse.from_dict(data)
    
    assert response.analyzer == "static_analyzer"
    assert response.status == "success"
    assert response.hash == "abc123"
    assert response.scan_type == "apk"
    assert response.file_name == "test.apk"


def test_trackers_from_dict():
    """Test Trackers creation from dict."""
    data = {
        "detected_trackers": 5,
        "total_trackers": 407,
    }
    trackers = Trackers.from_dict(data)
    
    assert trackers.detected_trackers == 5
    assert trackers.total_trackers == 407


def test_scan_response_from_dict():
    """Test ScanResponse creation from dict."""
    data = {
        "title": "Test App",
        "version": "1.0",
        "file_name": "test.apk",
        "app_name": "TestApp",
        "app_type": "apk",
        "package_name": "com.test.app",
        "size": "10MB",
        "md5": "abc123",
        "sha1": "def456",
        "sha256": "ghi789",
        "average_cvss": 3.5,
        "security_score": 75,
        "trackers": {
            "detected_trackers": 2,
            "total_trackers": 407,
        },
    }
    response = ScanResponse.from_dict(data)
    
    assert response.title == "Test App"
    assert response.average_cvss == 3.5
    assert response.security_score == 75
    assert response.trackers is not None
    assert response.trackers.detected_trackers == 2
