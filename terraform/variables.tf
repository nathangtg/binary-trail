variable "region" {
  description = "AWS region for deployment the Flask"
  default     = "ap-southeast-1"
}

variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}
variable "aws_region" {
  default = "ap-southeast-1"
}

variable "dynamodb_table_name" {}
variable "dynamodb_endpoint" {}
variable "jwt_secret" {}
