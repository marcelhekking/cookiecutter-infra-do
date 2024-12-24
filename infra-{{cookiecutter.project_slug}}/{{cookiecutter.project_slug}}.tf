resource "digitalocean_droplet" "{{cookiecutter.project_slug}}" {{ '{' }}
    image = "docker-20-04"
    name = "{{cookiecutter.project_slug}}"
    region = "AMS3"
    size = "s-1vcpu-1gb"
    ssh_keys = [
      data.digitalocean_ssh_key.terraform.id
    ]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = file(var.pvt_key)
    timeout = "2m"
  }

  provisioner "remote-exec" {
    inline = [
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
      # make these last 2 folders have the same group as in the containers
      # to avoid permission errors
      "sudo chown :1024 staticfiles",
      "chmod 775 staticfiles",
      "chmod g+s staticfiles",
      "sudo chown :1024 mediafiles",
      "chmod 775 mediafiles",
      "chmod g+s mediafiles",
    ]
  }
{{ '}' }}
