# Terraform and Ansible files for the "{{cookiecutter.project_name}}" website on Digital Ocean

## Introduction

This repo contains the necessary files to create a Digital Ocean droplet that will run the "{{cookiecutter.project_name}}" website on https using Letsencrypt to manage the SSL certificates. The droplet will run two services in separate containers (Gunicorn webservice serving Django and a Postgress database service) with Nginx on the host machine as a proxy-server.
Terraform is used to create and spin up a Digital Ocean Droplet. Ansible is then used to:

- install SSL certificates by using Letsencrypt,
- create SSH key pairs and fetching the private key

## How to work with Terraform

### Plan the creation/change of a Droplet

```bash
terraform plan -var "do_token=$DO_PAT" -var "pvt_key=$HOME/.ssh/id_rsa"
```

### Create/change a Droplet

```bash
terraform apply -var "do_token=$DO_PAT" -var "pvt_key=$HOME/.ssh/id_rsa"
```

### Destroy a Droplet

```bash
terraform destroy -var "do_token=$DO_PAT" -var "pvt_key=$HOME/.ssh/id_rsa"
```

## Setting up and rolling out a website with site {{cookiecutter.domain}}

### Used tutorials/instructions from the internet

#### On CI/CD of Django projects on Digital Ocean

- <https://testdriven.io/blog/deploying-django-to-digitalocean-with-docker-and-gitlab/>

#### On Docker volumes

- <https://mydeveloperplanet.com/2022/10/19/docker-files-and-volumes-permission-denied/>
- <https://medium.com/@nielssj/docker-volumes-and-file-system-permissions-772c1aee23ca>

#### On Letsencrypt and Ansible

- <https://gist.github.com/mattiaslundberg/ba214a35060d3c8603e9b1ec8627d349>

### Prerequisites

- Ansible (<https://www.terraform.io/>) installed and {{cookiecutter.domain}} added as an Ansible host locally in `/etc/ansible/hosts` (see tutorial under 'On Letsencrypt and Ansible'),
- Terraform installed,
- An account on Digital Ocean (DO) (<https://www.digitalocean.com/>),
  - A DO team name saved as an environment variable with the name  `DIGITALOCEAN_CONTEXT`
  - an API token for this DO team, saved  as an environment variable with the name `DO_PAT`,
- A registered domain name,
- A domain with this name created in Digital Ocean with three nameservers (NS records):
  - ns1.digitalocean.com.
  - ns2.digitalocean.com.
  - ns3.digitalocean.com.,

- Repo with a Django application on Gitlab with the following CI/CD variables:
  - DIGITAL_OCEAN_IP_ADDRESS (can also be `URI` like example.com),
  - MEDIAFILES_HOST (location on DO Droplet that is mounted in the Web service container to store Django mediafiles),
``  - SQL_DATABASE (database name),
  - POSTGRES_DB (database name when Postgress image is first started, should be the same as `SQL_DATABASE`),
  - POSTGRES_PASSWORD (password of the Postgress user),
  - POSTGRES_USER (the Postgress user),
  - PRIVATE_KEY (private key of the created DO Droplet),
  - SECRET_KEY (Django secret key),
  - SQL_DATABASE (database name),
  - SQL_HOST (db),
  - SQL_PASSWORD (password of the database owner),
  - SQL_PORT (port database is reachable on),
  - SQL_USER (database owner),
  - STATICFILES_HOST (location on DO Droplet that is mounted in Web service container to store the Django static files that are created with the management command `collectstatic`)

  If you want email enabled:
  - EMAIL_HOST_USER (user to log in at email provider)
  - EMAIL_HOST_PASSWORD (password to log in at email provider)
  - EMAIL_RECIPIENT_LIST (list if email addresses that should be notified)
  - DEFAULT_FROM_EMAIL (email address of sender)

### Setup new Digital Ocean Droplet

```bash
terraform apply -var "do_token=$DO_PAT" -var "pvt_key=$HOME/.ssh/id_rsa"
```

Check if droplet is up and ready to go by pinging `{{cookiecutter.domain}}`. If ready, log into the droplet once with `ssh root@{{cookiecutter.domain}}`. This will add `{{cookiecutter.domain}}` to the list of known hosts. This should be performed before running any Ansible file. Then run the Ansible file that configures Nginx and Letsencrypt:

```bash
ansible-playbook ansible/playbook.yml
```

Then create a ssh key pair on {{cookiecutter.domain}}, store the public key in the authorized_keys files on {{cookiecutter.domain}}, and send the private key to your own machine where it will be saved under the name "private_key_droplet":

```bash
ansible-playbook ansible/ssh.yml
```

Save this private ssh key as one of the CI/CD variables in the {{cookiecutter.project_slug}} Gitlab repo as a key/value pair with "PRIVATE_KEY" as key and start a CI/CD build.

If the build passes, enjoy your newly created secure website on "<https://{{cookiecutter.domain}}/>". Letsencrypt certificates will be automatically renewed.
