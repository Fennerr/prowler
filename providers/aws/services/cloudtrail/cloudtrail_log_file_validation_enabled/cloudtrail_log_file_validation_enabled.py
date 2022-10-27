from lib.check.models import Check, Check_Report
from providers.aws.services.cloudtrail.cloudtrail_client import cloudtrail_client


class cloudtrail_log_file_validation_enabled(Check):
    def execute(self):
        findings = []
        for trail in cloudtrail_client.trails:
            report = Check_Report(self.metadata)
            report.region = trail.region
            report.resource_id = trail.name
            report.resource_arn = trail.trail_arn
            report.status = "FAIL"
            if trail.is_multiregion:
                report.status_extended = (
                    f"Multiregion trail {trail.name} log file validation disabled"
                )
            else:
                report.status_extended = (
                    f"Single region trail {trail.name} log file validation disabled"
                )
            if trail.log_file_validation_enabled:
                report.status = "PASS"
                if trail.is_multiregion:
                    report.status_extended = (
                        f"Multiregion trail {trail.name} log file validation enabled"
                    )
                else:
                    report.status_extended = (
                        f"Single region trail {trail.name} log file validation enabled"
                    )

            findings.append(report)

        return findings
