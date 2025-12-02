"""Response models for MobSF API."""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from dateutil import parser as date_parser
from tabulate import tabulate


@dataclass
class ErrorResponse:
    """Error response from API."""
    
    error: str
    
    def __str__(self) -> str:
        """String representation."""
        return self.error
    
    @classmethod
    def from_dict(cls, data: dict) -> "ErrorResponse":
        """Create from dictionary."""
        return cls(error=data.get("error", "Unknown error"))


@dataclass
class UploadResponse:
    """Upload response from API."""
    
    analyzer: str
    status: str
    hash: str
    scan_type: str
    file_name: str
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Status: {self.status}\n"
            f"File name: {self.file_name}\n"
            f"Hash: {self.hash}\n"
            f"Scan type: {self.scan_type}\n"
            f"Analyzer: {self.analyzer}\n"
        )
    
    @classmethod
    def from_dict(cls, data: dict) -> "UploadResponse":
        """Create from dictionary."""
        return cls(
            analyzer=data["analyzer"],
            status=data["status"],
            hash=data["hash"],
            scan_type=data["scan_type"],
            file_name=data["file_name"],
        )


@dataclass
class Trackers:
    """Trackers detection information."""
    
    detected_trackers: int
    total_trackers: int
    
    @classmethod
    def from_dict(cls, data: dict) -> "Trackers":
        """Create from dictionary."""
        return cls(
            detected_trackers=data["detected_trackers"],
            total_trackers=data["total_trackers"],
        )


@dataclass
class ScanResponse:
    """Scan response from API."""
    
    title: str
    version: str
    file_name: str
    app_name: str
    app_type: str
    package_name: Optional[str]
    size: str
    md5: str
    sha1: str
    sha256: str
    average_cvss: float
    security_score: int
    trackers: Optional[Trackers] = None
    
    def __str__(self) -> str:
        """String representation."""
        lines = [
            f"Title: {self.title}",
            f"File name: {self.file_name}",
            f"Version: {self.version}",
            f"App name: {self.app_name}",
            f"App type: {self.app_type}",
            f"MD5: {self.md5}",
            f"SHA1: {self.sha1}",
            f"SHA256: {self.sha256}",
            f"Size: {self.size}",
        ]
        
        if self.package_name:
            lines.append(f"Package name: {self.package_name}")
        
        lines.append(f"Average CVSS: {self.average_cvss}")
        lines.append(f"Security score: {self.security_score}/100")
        
        if self.trackers:
            lines.append(
                f"Trackers detection: {self.trackers.detected_trackers}/{self.trackers.total_trackers}"
            )
        
        return "\n".join(lines) + "\n"
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScanResponse":
        """Create from dictionary."""
        trackers_data = data.get("trackers")
        trackers = Trackers.from_dict(trackers_data) if trackers_data else None
        
        return cls(
            title=data["title"],
            version=data["version"],
            file_name=data["file_name"],
            app_name=data["app_name"],
            app_type=data["app_type"],
            package_name=data.get("package_name"),
            size=data["size"],
            md5=data["md5"],
            sha1=data["sha1"],
            sha256=data["sha256"],
            average_cvss=data["average_cvss"],
            security_score=data["security_score"],
            trackers=trackers,
        )


@dataclass
class ScanItem:
    """Individual scan item."""
    
    scan_type: str
    analyzer: str
    timestamp: datetime
    md5: str
    version_name: str
    app_name: str
    package_name: str
    file_name: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScanItem":
        """Create from dictionary."""
        # Parse timestamp
        timestamp_str = data.get("TIMESTAMP", data.get("timestamp", ""))
        try:
            timestamp = date_parser.parse(timestamp_str)
        except (ValueError, TypeError):
            timestamp = datetime.now()
        
        return cls(
            scan_type=data.get("SCAN_TYPE", data.get("scan_type", "")),
            analyzer=data.get("ANALYZER", data.get("analyzer", "")),
            timestamp=timestamp,
            md5=data.get("MD5", data.get("md5", "")),
            version_name=data.get("VERSION_NAME", data.get("version_name", "")),
            app_name=data.get("APP_NAME", data.get("app_name", "")),
            package_name=data.get("PACKAGE_NAME", data.get("package_name", "")),
            file_name=data.get("FILE_NAME", data.get("file_name", "")),
        )


@dataclass
class ScansResponse:
    """Scans response from API."""
    
    content: List[ScanItem]
    count: int
    num_pages: int
    
    def __str__(self) -> str:
        """String representation as table."""
        if not self.content:
            return "No scans found.\n"
        
        headers = [
            "Type",
            "Analyzer",
            "Time",
            "Hash",
            "Version",
            "App name",
            "Package name",
            "File name",
        ]
        
        rows = []
        for item in self.content:
            timestamp_str = item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            rows.append([
                item.scan_type,
                item.analyzer,
                timestamp_str,
                item.md5[:12] + "..." if len(item.md5) > 12 else item.md5,
                item.version_name,
                item.app_name[:20] if len(item.app_name) > 20 else item.app_name,
                item.package_name[:20] if len(item.package_name) > 20 else item.package_name,
                item.file_name[:20] if len(item.file_name) > 20 else item.file_name,
            ])
        
        return tabulate(rows, headers=headers, tablefmt="grid") + "\n"
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScansResponse":
        """Create from dictionary."""
        content_data = data.get("content", [])
        content = [ScanItem.from_dict(item) for item in content_data]
        
        return cls(
            content=content,
            count=data.get("count", len(content)),
            num_pages=data.get("num_pages", 1),
        )


@dataclass
class DeleteScanResponse:
    """Delete scan response from API."""
    
    deleted: str
    
    def __str__(self) -> str:
        """String representation."""
        return f"Deleted: {self.deleted}\n"
    
    @classmethod
    def from_dict(cls, data: dict) -> "DeleteScanResponse":
        """Create from dictionary."""
        return cls(deleted=data["deleted"])


@dataclass
class ViewSourceResponse:
    """View source response from API."""
    
    title: str
    file: str
    file_type: str
    data: str
    version: str
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Title: {self.title}\n"
            f"File: {self.file}\n"
            f"Type: {self.file_type}\n"
            f"Version: {self.version}\n"
            f"{self.data}\n"
        )
    
    @classmethod
    def from_dict(cls, data: dict) -> "ViewSourceResponse":
        """Create from dictionary."""
        return cls(
            title=data["title"],
            file=data["file"],
            file_type=data.get("type", data.get("file_type", "")),
            data=data["data"],
            version=data["version"],
        )
