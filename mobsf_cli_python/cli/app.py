"""Application logic for mobsf-cli."""

from pathlib import Path
from mobsf_core import Mobsf, MobsfError
from .error import AppError


class App:
    """Application class."""
    
    NAME = "mobsf-cli"
    
    def __init__(self, api_key: str, server: str):
        """Initialize application.
        
        Args:
            api_key: API key for MobSF
            server: Server URL
        """
        try:
            self.mobsf = Mobsf(api_key, server)
        except Exception as e:
            raise AppError(f"Failed to initialize MobSF client: {e}")
    
    def ci(
        self,
        file_path: str,
        re_scan: bool,
        path_to_save: str,
        cvss: float,
        trackers: int,
        security: int,
    ) -> None:
        """CI/CD workflow.
        
        Args:
            file_path: Path to file to upload
            re_scan: Whether to re-scan
            path_to_save: Path to save reports
            cvss: Maximum CVSS score allowed
            trackers: Maximum trackers allowed
            security: Minimum security score required
            
        Raises:
            AppError: If any step fails or validation fails
        """
        try:
            # Upload
            print("Uploading...")
            upload_response = self.mobsf.upload(file_path)
            print(upload_response)
            
            # Scan
            print("Scanning. It takes some time...")
            scan_response = self.mobsf.scan(
                upload_response.scan_type,
                upload_response.file_name,
                upload_response.hash,
                re_scan,
            )
            print(scan_response)
            
            # Save reports
            path_to_save = path_to_save.rstrip("/")
            base_path = f"{path_to_save}/report_{scan_response.file_name}"
            
            print("Downloading reports...")
            
            # PDF report
            pdf_path = f"{base_path}.pdf"
            self.mobsf.report_pdf(upload_response.hash, pdf_path)
            print(f"Pdf report saved: {pdf_path}")
            
            # JSON report
            json_path = f"{base_path}.json"
            self.mobsf.write_report_json(upload_response.hash, json_path)
            print(f"Json report saved: {json_path}")
            
            # Validate scores
            print("Validating scan scores...")
            
            # CVSS check
            if scan_response.average_cvss > cvss:
                raise AppError(
                    f"CVSS score [{scan_response.average_cvss}] is to high. Max: {cvss}!"
                )
            print(f"CVSS score: {scan_response.average_cvss}/{cvss}. OK")
            
            # Security score check
            if scan_response.security_score < security:
                raise AppError(
                    f"Security score [{scan_response.security_score}] is to low. Min: {security}!"
                )
            print(f"Security score: {scan_response.security_score}/{security}. OK")
            
            # Trackers check
            if scan_response.trackers:
                detected = scan_response.trackers.detected_trackers
                if detected > trackers:
                    raise AppError(
                        f"Trackers score [{detected}] is to high. Max: {trackers}!"
                    )
                print(f"Trackers score: {detected}/{trackers}. OK")
            
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def upload_file(self, file_path: str) -> None:
        """Upload a file.
        
        Args:
            file_path: Path to file to upload
            
        Raises:
            AppError: If upload fails
        """
        try:
            response = self.mobsf.upload(file_path)
            print(response)
            print(
                f"Start scan command : {self.NAME} scan "
                f"{response.scan_type} {response.file_name} {response.hash}"
            )
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def scans(self) -> None:
        """Display recent scans.
        
        Raises:
            AppError: If request fails
        """
        try:
            response = self.mobsf.scans()
            print(response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def scan(
        self,
        scan_type: str,
        file_name: str,
        hash_value: str,
        re_scan: bool,
    ) -> None:
        """Scan a file.
        
        Args:
            scan_type: Type of scan
            file_name: File name
            hash_value: File hash
            re_scan: Whether to re-scan
            
        Raises:
            AppError: If scan fails
        """
        try:
            response = self.mobsf.scan(scan_type, file_name, hash_value, re_scan)
            print(response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def delete_scan(self, hash_value: str) -> None:
        """Delete a scan.
        
        Args:
            hash_value: File hash
            
        Raises:
            AppError: If deletion fails
        """
        try:
            response = self.mobsf.delete_scan(hash_value)
            print(response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def play(self, file_path: str, re_scan: bool) -> None:
        """Upload and scan a file.
        
        Args:
            file_path: Path to file to upload
            re_scan: Whether to re-scan
            
        Raises:
            AppError: If upload or scan fails
        """
        try:
            # Upload
            print("Uploading...")
            upload_response = self.mobsf.upload(file_path)
            print(upload_response)
            
            # Scan
            print("Scanning. It takes some time...")
            scan_response = self.mobsf.scan(
                upload_response.scan_type,
                upload_response.file_name,
                upload_response.hash,
                re_scan,
            )
            print(scan_response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def report_pdf(self, hash_value: str, file_path: str) -> None:
        """Download PDF report.
        
        Args:
            hash_value: File hash
            file_path: Path to save PDF
            
        Raises:
            AppError: If download fails
        """
        try:
            self.mobsf.report_pdf(hash_value, file_path)
            print(f"Pdf report saved: {file_path}")
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def write_report_json(self, hash_value: str, file_path: str) -> None:
        """Download and save JSON report.
        
        Args:
            hash_value: File hash
            file_path: Path to save JSON
            
        Raises:
            AppError: If download fails
        """
        try:
            self.mobsf.write_report_json(hash_value, file_path)
            print(f"Json report saved: {file_path}")
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def print_report_json(self, hash_value: str) -> None:
        """Print JSON report to stdout.
        
        Args:
            hash_value: File hash
            
        Raises:
            AppError: If request fails
        """
        try:
            response = self.mobsf.report_json(hash_value)
            print(response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
    
    def view_source(
        self,
        scan_type: str,
        file_path: str,
        hash_value: str,
    ) -> None:
        """View source file.
        
        Args:
            scan_type: Type of scan
            file_path: Relative file path
            hash_value: File hash
            
        Raises:
            AppError: If request fails
        """
        try:
            response = self.mobsf.view_source(scan_type, file_path, hash_value)
            print(response)
        except MobsfError as e:
            raise AppError.from_mobsf_error(e)
