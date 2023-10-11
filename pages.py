import pulumi
import pulumi_cloudflare as cloudflare

config = pulumi.Config()

account_id = config.get("account-id")

for page_name, page_domains in config.get_object("pages").items():
    page_project = cloudflare.PagesProject(
        page_name,
        account_id=account_id,
        name=page_name,
        production_branch="main",
    )

    for domain, names in page_domains.items():
        zone = cloudflare.get_zone(account_id=account_id, name=domain)

        for name in names:
            record = cloudflare.Record(
                "{}-{}".format(domain, name),
                name=name,
                type="CNAME",
                value=page_project.domains[0],
                zone_id=zone.id,
            )
            cloudflare.PagesDomain(
                "{}-{}".format(domain, name),
                account_id=account_id,
                domain=record.hostname,
                project_name=page_project.name,
            )
