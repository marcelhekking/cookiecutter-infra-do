variable "do_token" {}
variable "pvt_key" {}
variable "domain_name" {
    type = string
    default = "{{cookiecutter.domain}}"
}
