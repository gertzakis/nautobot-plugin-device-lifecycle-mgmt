"""Jobs for the CVE Tracking portion of the Device Lifecycle plugin."""
from datetime import datetime

from nautobot.extras.jobs import Job, StringVar, BooleanVar
from nautobot.extras.models import Relationship

from nautobot_device_lifecycle_mgmt.models import (
    CVELCM,
    VulnerabilityLCM,
)


name = "CVE Tracking"  # pylint: disable=invalid-name


class GenerateVulnerabilities(Job):
    """Generates VulnerabilityLCM objects based on CVEs that are related to Devices."""

    name = "Generate Vulnerabilities"
    description = "Generates any missing Vulnerability objects."
    read_only = False
    published_after = StringVar(
        regex=r"^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$",
        label="CVEs Published After",
        description="Enter a date in ISO Format (YYYY-MM-DD) to only process CVEs published after that date.",
        default="1970-01-01",
        required=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for the job."""

        commit_default = True
        field_order = ["published_after", "_task_queue", "debug", "_commit"]

    debug = BooleanVar(description="Enable for more verbose logging.")

    def run(self, data, commit):  # pylint: disable=too-many-locals
        """Check if software assigned to each device is valid. If no software is assigned return warning message."""
        # Although the default is set on the class attribute for the UI, it doesn't default for the API
        published_after = data.get("published_after", "1970-01-01")
        cves = CVELCM.objects.filter(published_date__gte=datetime.fromisoformat(published_after)).prefetch_related(
            "destination_for_associations", "destination_for_associations__relationship"
        )
        count_before = VulnerabilityLCM.objects.count()
        device_soft_rel = Relationship.objects.get(slug="device_soft")
        inv_item_soft_rel = Relationship.objects.get(slug="inventory_item_soft")

        for cve in cves:
            if data["debug"]:
                self.log_info(obj=cve, message="Generating vulnerabilities for CVE {cve}")
            # Get Software Relationships from the `_prefetched_objects_cache`
            software_rels = cve.destination_for_associations.filter(relationship__slug="soft_cve")
            for soft_rel in software_rels:
                # Loop through any device relationships~
                device_rels = soft_rel.source.get_relationships()["source"][device_soft_rel]
                for dev_rel in device_rels:
                    VulnerabilityLCM.objects.get_or_create(cve=cve, software=dev_rel.source, device=dev_rel.destination)

                # Loop through any inventory tem relationships
                item_rels = soft_rel.source.get_relationships()["source"][inv_item_soft_rel]
                for item_rel in item_rels:
                    VulnerabilityLCM.objects.get_or_create(
                        cve=cve,
                        software=item_rel.source,
                        inventory_item=item_rel.destination,
                    )

        diff = VulnerabilityLCM.objects.count() - count_before
        self.log_success(message=f"Processed {cves.count()} CVEs and generated {diff} Vulnerabilities.")
