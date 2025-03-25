# Cookiecutter template to install Droplets on Digital Ocean using Pulumi and Ansible.

## Introduction

This repo is a cookiecutter template with which one can create a Digital Ocean droplet that will run a website on https using Letsencrypt to manage the SSL certificates. [Pulumi](https://www.pulumi.com/) is used to create and spin up a Digital Ocean Droplet. [Ansible](https://ansible.readthedocs.io/) is then used to:

- install SSL certificates by using Letsencrypt,
- create SSH key pairs and fetching the private key

## How to install this template

First install [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and then run:

```bash
cookiecutter https://github.com/marcelhekking/cookiecutter-infra-do
```

You'll be asked some questions about the project. After installation read the README.md file of the just created project on how to further set things up with Pulumi and Ansible.