# Pulumi code and Ansible files for the "{{cookiecutter.project_name}}" website

## Introduction

This repo contains the necessary files to create a Digital Ocean droplet that will run the "{{cookiecutter.project_name}}" website on https using Letsencrypt to manage the SSL certificates. The droplet will run two services in separate containers (Gunicorn webservice serving Django and a Postgress database service) with Nginx on the host machine as a proxy-server.
[Pulumi](https://www.pulumi.com/) is used to create and spin up a Digital Ocean Droplet. [Ansible](https://ansible.readthedocs.io/) is then used to:

- install SSL certificates by using Letsencrypt,
- create SSH key pairs and fetching the private key

## How to work with Pulumi

With Pulumi a Digital Ocean droplet can be created, just like Terraform. The difference betweeen Terraform  and Pulumi is that infractructure can be completely defined using Python code. The examples below assumes a Pulumi stack with at least the user-defined following configuration:

- digitalocean:token (enables the access of Pulumi to Digial Ocean)
  - To add the token (Digital Ocean Personal Access Token [DO_PATH]) to the Pulumi config as a secret:

  ```bash
      pulumi config set digitalocean:token <DO_PAT> --secret
  ```

- infra-{{cookiecutter.project_slug}}:domain_name
  - To add the domain name to the Pulumi config as a secret:

  ```bash
      pulumi config set infra-{{cookiecutter.project_slug}}:domain_name {{cookiecutter.domain_name}}
  ```

- infra-{{cookiecutter.project_slug}}:pvt_key_path (path to an SSH private key on the host, enabling login to the Droplet from the machine you run Pulumi on.)
  - To add the path to a private SSH key to the Pulumi config:

  ```bash
      pulumi config set infra-{{cookiecutter.project_slug}}:pvt_key_path ~/.ssh/{{cookiecutter.project_slug}}
  ```

### Create a Droplet

First login to your Pulumi account:

```bash
pulumi login
```

then prepare the changes:

```bash
pulumi up
```

### Destroy a Droplet

```bash
pulumi destroy
```

## Setting up and rolling out a website to "{{cookiecutter.domain_name}}"

### Used tutorials/instructions from the internet

#### On CI/CD of Django projects on Digital Ocean

- <https://testdriven.io/blog/deploying-django-to-digitalocean-with-docker-and-gitlab/>

#### On Docker volumes

- <https://mydeveloperplanet.com/2022/10/19/docker-files-and-volumes-permission-denied/>
- <https://medium.com/@nielssj/docker-volumes-and-file-system-permissions-772c1aee23ca>

#### On Letsencrypt and Ansible

- <https://gist.github.com/mattiaslundberg/ba214a35060d3c8603e9b1ec8627d349>

### Prerequisites

- Since Pulumi is a Python package, this package should be installed. If you have [`uv`](https://github.com/astral-sh/uv) installed on your machine you could easily do this with

  ```bash
  uv sync
  ```

  This will install the right Python version and create a virtual environment `.venv` with the required Python packages installed.

- [Ansible](https://ansible.readthedocs.io/) installed and {{cookiecutter.domain_name}} added as an Ansible host locally in `/etc/ansible/hosts` (see tutorial under 'On Letsencrypt and Ansible'),
- [Pulumi](https://www.pulumi.com/) installed and a Pulumi account with a stack called `infra-{{cookiecutter.project_slug}}` , holding the following variables:
  - DATABASE="postgres"
  - DEBUG="0"
  - DOMAIN_NAME="{{cookiecutter.domain_name}}"
  - DROPLET_IP="DROPLET IP ADDRESS"
  - MEDIAFILES_HOST="/home/public/mediafiles"
  - NAMESPACE="GITHUB USER NAME"
  - PERSONAL_ACCESS_TOKEN="GITHUB PERSONAL ACCESS TOKEN"
  - POSTGRES_DB="DB NAME"
  - POSTGRES_PASSWORD="DB PASSWORD"
  - POSTGRES_USER="postgres"
  - SECRET_KEY="DJANGO SECRET"
  - SQL_DATABASE="DB NAME"
  - SQL_HOST="db"
  - SQL_PASSWORD="DB PASSWORD"
  - SQL_PORT="5432"
  - SQL_USER="postgres"
  - STATICFILES_HOST="/home/public/staticfiles"
- An account on [Digital Ocean](<https://www.digitalocean.com/>) (DO),
- A Digital Ocean Personal Access Token (DO_PAT)
- A registered domain name,
- A domain with this name created in Digital Ocean with three nameservers (NS records):
  - ns1.digitalocean.com.
  - ns2.digitalocean.com.
  - ns3.digitalocean.com.,

- Repo with a Django application on Github with the following CI/CD secrets:
  - PRIVATE_KEY_DROPLET (the private SSH key of an SSH pair as created on the droplet with `ansible-playbook ansible/ssh.yml`),
  - PULUMI_ACCESS_TOKEN (a token to access the environment variables of this project on Pulumi)

  If you want email enabled:
  - EMAIL_HOST_USER (user to log in at email provider)
  - EMAIL_HOST_PASSWORD (password to log in at email provider)
  - EMAIL_RECIPIENT_LIST (list if email addresses that should be notified)
  - DEFAULT_FROM_EMAIL (email address of sender)

### Setup new Digital Ocean Droplet

```bash
pulumi up (select yes)
```

Check if droplet is up and ready to go by pinging `{{cookiecutter.domain_name}}`. If ready, log into the droplet once with `ssh root@{{cookiecutter.domain_name}}`. This will add `{{cookiecutter.domain_name}}` to the list of known hosts. This should be performed before running any Ansible file. Then run the Ansible file that configures Nginx and Letsencrypt:

```bash
ansible-playbook ansible/playbook.yml
```

Then create a ssh key pair on {{cookiecutter.domain_name}}, store the public key in the authorized_keys files on {{cookiecutter.domain_name}}, and send the private key to your own machine where it will be saved under the name "private_key_droplet" (which will be the input of one of the secrets in the Github repo):

```bash
ansible-playbook ansible/ssh.yml
```

Save this private SSH key as one of the CI/CD secrets in the {{cookiecutter.project_slug}} Github repo as a key/value pair with "PRIVATE_KEY_DROPLET" as key and start a CI/CD build.

If the build passes, enjoy your newly created secure website on "<https://{{cookiecutter.domain_name}}/>". Letsencrypt certificates will be automatically renewed.
