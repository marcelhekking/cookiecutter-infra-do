"""A DigitalOcean Python Pulumi program"""

from pathlib import Path

import pulumi
import pulumi_command as command
import pulumi_digitalocean as do

# Load the configuration variables
config = pulumi.Config()
pvt_key_path = config.require("pvt_key_path")
domain_name = config.get("domain_name")

# Read the private key from the file
pvt_key = Path(pvt_key_path).read_text()

# Define the SSH key
ssh_key_name = pvt_key_path.split("/")[-1]
ssh_key = do.get_ssh_key(name=ssh_key_name)

# Create a DigitalOcean Droplet
droplet = do.Droplet(
    "{{cookiecutter.project_slug}}",
    image="docker-20-04",
    name="{{cookiecutter.project_slug}}",
    region="ams3",
    size="s-1vcpu-1gb",
    ssh_keys=[ssh_key.id],
)

# Define the connection details
connection = command.remote.ConnectionArgs(
    host=droplet.ipv4_address,
    user="root",
    private_key=pvt_key,
)


# Define provisioning commands
provisioning_commands = [
    "export PATH=$PATH:/usr/bin",
    "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 35696F43FC7DB4C2",
    "sudo apt update",
    "sudo apt install -y python3-simplejson",
    "sudo apt install -y nginx",
    "sudo ufw allow 'Nginx HTTP'",
    "mkdir /app",
    "mkdir /home/public",
    "cd /home/public",
    "mkdir staticfiles",
    "mkdir mediafiles",
    "sudo chown :1024 staticfiles",
    "chmod 775 staticfiles",
    "chmod g+s staticfiles",
    "sudo chown :1024 mediafiles",
    "chmod 775 mediafiles",
    "chmod g+s mediafiles",
]

cmds = " && ".join(provisioning_commands)

# Execute provisioning commands
command.remote.Command(
    "provision",
    connection=connection,
    create=cmds,
    opts=pulumi.ResourceOptions(depends_on=[droplet]),
)

# Create DNS records
www_record = do.DnsRecord(
    "www", domain=domain_name, type="A", name="@", value=droplet.ipv4_address
)

www_2_record = do.DnsRecord(
    "www-2", domain=domain_name, type="A", name="www", value=droplet.ipv4_address
)

{% if cookiecutter.use_email == "y" %}

mx_record = do.DnsRecord(
    "mx",
    domain=domain_name,
    type="MX",
    name="@",
    priority=10,
    value="mailfilter.hostnet.nl.",
)

spf_record = do.DnsRecord(
    "spf",
    domain=domain_name,
    type="TXT",
    name="@",
    value="v=spf1 a mx include:_spf.hostnet.nl -all",
)

dkim_record = do.DnsRecord(
    "dkim",
    domain=domain_name,
    type="TXT",
    name="default._domainkey",
    value="v=DKIM1; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAouILmrc1JPOXs4fWdPKi365yVeve4Y15RwYpTgbIwKCwo0S0Z+ucrzNbaFfM26J38hLfH4KbWhCALHRVsVg3+iv4pxsfLwAJP7fdm+6xKo64gih5X8UVYrQhs863owBMQWl9CA5B2IhSCqWtzNX2OGe8EViCZqQS0Fdlw3tfnDZzerj5aO7ZNYMfNmg+zE6V0ycz226z9Pq3OPLG7kVVjmv7GRjHOVsTofui2678HtQ4jFAtGp5V6itwkNX5tPuJIH6TNDRQCzwPPY7wRpm9X30JCcRuf14YTVBJ1uWLgt+wnde6ELKD7EXBgR8eoozpVn9mYWVQWfcJN8UH7rQHjwIDAQAB",  # noqa
)

# Export the Droplet IP address and domain name
pulumi.export("droplet_ip", droplet.ipv4_address)
pulumi.export("domain_name", domain_name)

{% endif %}