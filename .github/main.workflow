workflow "jenkins execute" {
  on = "push"
  resolves = ["new-action"]
}

action "new-action" {
  uses = "owner/repo/path@ref"
}
