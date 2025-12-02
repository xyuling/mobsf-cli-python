"""MobSF API Client."""

import os
from typing import Optional
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .error import MobsfError, ErrorCause
from .response import (
    ErrorResponse,
    UploadResponse,
    ScansResponse,
    ScanResponse,
    DeleteScanResponse,
    ViewSourceResponse,
)


class Mobsf:
    """MobSF API Client."""
    
    # API endpoints
    UPLOAD_API = "api/v1/upload"
    SCANS_API = "api/v1/scans"
    SCAN_API = "api/v1/scan"
    DELETE_SCAN_API = "api/v1/delete_scan"
    REPORT_PDF_API = "api/v1/download_pdf"
    REPORT_JSON_API = "api/v1/report_json"
    VIEW_SOURCE_API = "api/v1/view_source"
    
    def __init__(self, api_key: str, server: str, timeout: int = 10):
        """Initialize MobSF client.
        
        Args:
            api_key: API key for authentication
            server: Server URL
            timeout: Connection timeout in seconds
        """
        self.server = server.rstrip("/")
        self.timeout = timeout
        
        # Create session with retry logic
        self.session = self._create_session(api_key)
    
    def _create_session(self, api_key: str) -> requests.Session:
        """Create a requests session with retry logic and headers.
        
        Args:
            api_key: API key for authentication
            
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Configure retry logic
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers
        session.headers.update({
            "Accept": "application/json",
            "Authorization": api_key,
        })
        
        return session
    
    def _url(self, api_path: str) -> str:
        """Construct full API URL.
        
        Args:
            api_path: API endpoint path
            
        Returns:
            Full URL
        """
        return f"{self.server}/{api_path}"
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses from API.
        
        Args:
            response: HTTP response
            
        Raises:
            MobsfError: If response indicates an error
        """
        try:
            error_data = response.json()
            error_msg = ErrorResponse.from_dict(error_data).error
        except (ValueError, KeyError):
            error_msg = response.text or f"HTTP {response.status_code}"
        
        raise MobsfError(
            cause=ErrorCause.INVALID_HTTP_RESPONSE,
            message=error_msg,
            status_code=response.status_code,
        )
    
    def upload(self, file_path: str) -> UploadResponse:
        """Upload a file to MobSF.
        
        Args:
            file_path: Path to file to upload
            
        Returns:
            Upload response
            
        Raises:
            MobsfError: If upload fails
        """
        path = Path(file_path)
        
        if not path.exists():
            raise MobsfError(
                cause=ErrorCause.IO_ERROR,
                message=f"File not found: {file_path}",
            )
        
        if not path.is_file():
            raise MobsfError(
                cause=ErrorCause.IO_ERROR,
                message=f"Not a file: {file_path}",
            )
        
        file_name = path.name
        
        try:
            with open(path, "rb") as f:
                files = {"file": (file_name, f, "application/octet-stream")}
                response = self.session.post(
                    self._url(self.UPLOAD_API),
                    files=files,
                    timeout=self.timeout,
                )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        except IOError as e:
            raise MobsfError(
                cause=ErrorCause.IO_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return UploadResponse.from_dict(response.json())
    
    def scans(self) -> ScansResponse:
        """Get recent scans.
        
        Returns:
            Scans response
            
        Raises:
            MobsfError: If request fails
        """
        try:
            response = self.session.get(
                self._url(self.SCANS_API),
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return ScansResponse.from_dict(response.json())
    
    def scan(
        self,
        scan_type: str,
        file_name: str,
        hash_value: str,
        re_scan: bool = False,
    ) -> ScanResponse:
        """Scan a file.
        
        Args:
            scan_type: Type of scan (apk, xapk, ipa, etc.)
            file_name: File name
            hash_value: File hash
            re_scan: Whether to re-scan
            
        Returns:
            Scan response
            
        Raises:
            MobsfError: If scan fails
        """
        data = {
            "scan_type": scan_type,
            "file_name": file_name,
            "hash": hash_value,
        }
        
        if re_scan:
            data["re_scan"] = "1"
        
        try:
            response = self.session.post(
                self._url(self.SCAN_API),
                data=data,
                timeout=300,  # Scanning can take time
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return ScanResponse.from_dict(response.json())
    
    def delete_scan(self, hash_value: str) -> DeleteScanResponse:
        """Delete a scan.
        
        Args:
            hash_value: File hash
            
        Returns:
            Delete response
            
        Raises:
            MobsfError: If deletion fails
        """
        data = {"hash": hash_value}
        
        try:
            response = self.session.post(
                self._url(self.DELETE_SCAN_API),
                data=data,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return DeleteScanResponse.from_dict(response.json())
    
    def report_pdf(self, hash_value: str, file_path: str) -> None:
        """Download PDF report.
        
        Args:
            hash_value: File hash
            file_path: Path to save PDF
            
        Raises:
            MobsfError: If download fails
        """
        data = {"hash": hash_value}
        
        try:
            response = self.session.post(
                self._url(self.REPORT_PDF_API),
                data=data,
                timeout=60,
                stream=True,
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        try:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except IOError as e:
            raise MobsfError(
                cause=ErrorCause.IO_ERROR,
                message=str(e),
            )
    
    def report_json(self, hash_value: str) -> str:
        """Get JSON report.
        
        Args:
            hash_value: File hash
            
        Returns:
            JSON report as string
            
        Raises:
            MobsfError: If request fails
        """
        data = {"hash": hash_value}
        
        try:
            response = self.session.post(
                self._url(self.REPORT_JSON_API),
                data=data,
                timeout=60,
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return response.text
    
    def write_report_json(self, hash_value: str, file_path: str) -> str:
        """Get JSON report and write to file.
        
        Args:
            hash_value: File hash
            file_path: Path to save JSON
            
        Returns:
            JSON report as string
            
        Raises:
            MobsfError: If request or write fails
        """
        json_text = self.report_json(hash_value)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json_text)
        except IOError as e:
            raise MobsfError(
                cause=ErrorCause.IO_ERROR,
                message=str(e),
            )
        
        return json_text
    
    def view_source(
        self,
        scan_type: str,
        file_path: str,
        hash_value: str,
    ) -> ViewSourceResponse:
        """View source file.
        
        Args:
            scan_type: Type of scan
            file_path: Relative file path
            hash_value: File hash
            
        Returns:
            View source response
            
        Raises:
            MobsfError: If request fails
        """
        data = {
            "hash": hash_value,
            "file": file_path,
            "type": scan_type,
        }
        
        try:
            response = self.session.post(
                self._url(self.VIEW_SOURCE_API),
                data=data,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            raise MobsfError(
                cause=ErrorCause.HTTP_CLIENT_ERROR,
                message=str(e),
            )
        
        if response.status_code != 200:
            self._handle_error_response(response)
        
        return ViewSourceResponse.from_dict(response.json())
