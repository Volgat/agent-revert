# Security Policy

## Reporting a vulnerability

Please **do not** open a public issue. Report privately via GitHub:
go to the repository's **Security** tab → **Report a vulnerability**
(GitHub Private Vulnerability Reporting), or contact the maintainer
`@kaia-cod` through GitHub.

Include: affected version/commit, steps to reproduce, and impact.

## Scope & expectations

- We acknowledge reports within 7 days and aim to ship a fix or a mitigation
  plan within 30 days.
- `agent-revert` is a local CLI: it never sends your files anywhere, requires
  no network access, and stores snapshots only in directories you choose.
- Please do not run automated scanners against the maintainer's accounts;
  test against a local clone.
