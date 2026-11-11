# AUDIT — Projet open source 30 jours (s1, borné)

Date (UTC) : 2026-11-11
Compte possédé : @kaia-cod (outils github_*)
HF : ABANDONNÉ — 401 Unauthorized sur https://huggingface.co/api/me (token absent/invalide), sans droit de solliciter l'utilisateur.

## 1. Liste GitHub @kaia-cod (github_repo_list)
- Résultat : 9 dépôts trouvés sur @kaia-cod.
- Détail nominatif complet non restitué par l'outil (compte seul), mais le dépôt cible est confirmé ci-dessous.

## 2. Dépôt local identifié
- Chemin absolu : /home/ubuntu/SAM-G-Agent/workspace/agent-revert
- Nom : agent-revert
- Git HEAD (SHA) : 8df1d1b0848705a7d2931010cf95497ce6d41157
- git status --short : (vide = arbre propre, rien à committer)
- Remote origin : https://github.com/kaia-cod/agent-revert.git (fetch+push)
- Fichiers racine : README.md, CHANGELOG.md, pyproject.toml, LICENSE, agent_revert/, tests/, examples/, .github/
- État réel : dépôt local initialisé, commité, propre, distant = kaia-cod/agent-revert (donc présent sur GitHub, pas de création nécessaire).

## 3. Décision
- Repo à lancer : https://github.com/kaia-cod/agent-revert
- 3 canaux figés (possédés) : (1) repo poussé + README, (2) GitHub Release, (3) issue de lancement GitHub.
- Abandonnés : Show HN, Product Hunt, 10 000 stars, HF Space (justifications en PREUVE_CLOSURE.md).

Budget s1 : 2 appels cibles (github_repo_list + git local) + 1 écriture AUDIT.md ; aucune exploration HF, aucun connector_status, aucune lecture hors sujet.

## 4. s2 — Abandon HF acté et 3 canaux figés

- HF ABANDONNÉ (définitif, aucune nouvelle tentative HF, aucun connector_probe HF) : 401 Unauthorized sur https://huggingface.co/api/me, token HF_USER absent/invalide, 404 répétés sur les appels HF précédents. Sans nouveau token — qu'il est interdit de solliciter à l'utilisateur — HF est inutilisable.
- Canaux figés (uniquement comptes possédés, preuve par URL distincte en PREUVE_CLOSURE.md) :
  1. Repo GitHub poussé : https://github.com/kaia-cod/agent-revert (README de lancement à jour)
  2. GitHub Release de lancement
  3. Issue de lancement GitHub
- Tableau de projet via 5 issues : Backlog / In Progress / Review / Done / Roadmap (équivalent prouvable si Projects V2 indisponible via API).
- Canaux impossibles abandonnés à ce stade : Show HN, Product Hunt, 10 000 stars, HF Space — aucun compte possédé, aucune publication sur compte tiers sans accès.
