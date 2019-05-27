workflow "Build and deploy on push" {
  on = "push"
  resolves = ["HTTP client"]
}

action "HTTP client" {
  uses = "swinton/httpie.action@8ab0a0e926d091e0444fcacd5eb679d2e2d4ab3d"
  secrets = ["GITHUB_TOKEN", "my_valor_Secreto"]
}
