"""Security testing script using OWASP ZAP."""
import time
from zapv2 import ZAPv2
import subprocess
import sys
import json

class SecurityTester:
    """Security testing using OWASP ZAP."""

    def __init__(self, target_url: str, api_key: str = None):
        """Initialize security tester."""
        self.target_url = target_url
        self.zap = ZAPv2(
            apikey=api_key,
            proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
        )

    def setup(self):
        """Set up the security testing environment."""
        print('Setting up ZAP scanner...')
        
        # Configure ZAP scanner
        self.zap.core.new_session()
        self.zap.context.new_context('kundli')
        self.zap.context.include_in_context('kundli', f'^{self.target_url}.*$')
        
        # Configure authentication
        self.zap.authentication.set_authentication_method(
            'kundli',
            'jsonBasedAuthentication',
            f'loginUrl={self.target_url}/auth/login&username=testuser@example.com&password=testpassword'
        )

    def spider_scan(self):
        """Run spider scan to discover endpoints."""
        print('Starting spider scan...')
        scan_id = self.zap.spider.scan(self.target_url)
        
        # Wait for spider scan to complete
        while int(self.zap.spider.status(scan_id)) < 100:
            print(f'Spider progress: {self.zap.spider.status(scan_id)}%')
            time.sleep(5)
        
        print('Spider scan completed')

    def active_scan(self):
        """Run active scan to find vulnerabilities."""
        print('Starting active scan...')
        scan_id = self.zap.ascan.scan(self.target_url)
        
        # Wait for active scan to complete
        while int(self.zap.ascan.status(scan_id)) < 100:
            print(f'Active scan progress: {self.zap.ascan.status(scan_id)}%')
            time.sleep(5)
        
        print('Active scan completed')

    def generate_report(self):
        """Generate security report."""
        print('Generating report...')
        
        # Get all alerts
        alerts = self.zap.core.alerts()
        
        # Organize alerts by risk level
        report = {
            'high_risks': [],
            'medium_risks': [],
            'low_risks': [],
            'informational': []
        }
        
        for alert in alerts:
            risk = alert.get('risk')
            if risk == 'High':
                report['high_risks'].append(alert)
            elif risk == 'Medium':
                report['medium_risks'].append(alert)
            elif risk == 'Low':
                report['low_risks'].append(alert)
            else:
                report['informational'].append(alert)
        
        # Save report to file
        with open('security_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print('\nSecurity Scan Summary:')
        print(f"High Risk Issues: {len(report['high_risks'])}")
        print(f"Medium Risk Issues: {len(report['medium_risks'])}")
        print(f"Low Risk Issues: {len(report['low_risks'])}")
        print(f"Informational: {len(report['informational'])}")
        
        return report

    def run_security_tests(self):
        """Run all security tests."""
        try:
            self.setup()
            self.spider_scan()
            self.active_scan()
            return self.generate_report()
        except Exception as e:
            print(f'Error during security testing: {str(e)}')
            sys.exit(1)

def main():
    """Main function to run security tests."""
    target_url = 'http://localhost:8000'  # Update with your target URL
    tester = SecurityTester(target_url)
    report = tester.run_security_tests()
    
    # Exit with error if high risk issues found
    if len(report['high_risks']) > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
