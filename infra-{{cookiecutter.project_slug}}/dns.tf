resource "digitalocean_record" "www" {
  domain = var.domain_name
  type   = "A"
  name   = "@"
  value  = digitalocean_droplet.{{cookiecutter.project_slug}}.ipv4_address
}


resource "digitalocean_record" "www-2" {
  domain = var.domain_name
  type   = "A"
  name   = "www"
  value  = digitalocean_droplet.{{cookiecutter.project_slug}}.ipv4_address
}
{% if cookiecutter.use_email == "y" %}

resource "digitalocean_record" "mx" {
  domain = var.domain_name
  type     = "MX"
  name     = "@"
  priority = 10
  value  = "mailfilter.hostnet.nl."
}

resource "digitalocean_record" "spf" {
  domain = var.domain_name
  type     = "TXT"
  name     = "@"
  value  = "v=spf1 a mx include:_spf.hostnet.nl -all"
}


resource "digitalocean_record" "dkim" {
  domain = var.domain_name
  type     = "TXT"
  name     = "default._domainkey"
  value  = "v=DKIM1; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAouILmrc1JPOXs4fWdPKi365yVeve4Y15RwYpTgbIwKCwo0S0Z+ucrzNbaFfM26J38hLfH4KbWhCALHRVsVg3+iv4pxsfLwAJP7fdm+6xKo64gih5X8UVYrQhs863owBMQWl9CA5B2IhSCqWtzNX2OGe8EViCZqQS0Fdlw3tfnDZzerj5aO7ZNYMfNmg+zE6V0ycz226z9Pq3OPLG7kVVjmv7GRjHOVsTofui2678HtQ4jFAtGp5V6itwkNX5tPuJIH6TNDRQCzwPPY7wRpm9X30JCcRuf14YTVBJ1uWLgt+wnde6ELKD7EXBgR8eoozpVn9mYWVQWfcJN8UH7rQHjwIDAQAB"
}


resource "digitalocean_record" "autoconfig" {
  domain = var.domain_name
  type     = "CNAME"
  name     = "autoconfig"
  value  = "autodiscover.hostnet.nl."
}


resource "digitalocean_record" "webmail" {
  domain = var.domain_name
  type     = "CNAME"
  name     = "webmail"
  value  = "ox.hostnet.nl."
}
{% endif %}