# TP DevSecOps — Partie 6 : analyse statique (SAST) avec Semgrep

Dépôt de démonstration du TP **DevSecOps — Partie 6** : mise en place d'une
Quality Gate SAST dans GitHub Actions, avec publication des résultats au format
SARIF dans l'onglet **Security > Code scanning**.

> ⚠️ **Avertissement pédagogique**
> La branche `feature/user-api` introduit volontairement un fichier `server.py`
> vulnérable (injection SQL et injection de commande). Ce code ne doit jamais
> être déployé. Aucun secret réel n'est présent dans ce dépôt.

## Architecture CI/CD

Un fichier de workflow par scanner, pour isoler les temps d'exécution, les
échecs et les permissions :

```text
.github/
└── workflows/
    ├── gitleaks.yml     # Scan de secrets statique (Partie 2)
    ├── trufflehog.yml   # Scan & vérification dynamique de secrets (Partie 4)
    └── semgrep.yml      # Analyse statique SAST du code source (Partie 6)
```

## Le workflow Semgrep

- exécution dans le conteneur officiel `semgrep/semgrep:latest` ;
- règles `p/default` et `p/owasp-top-ten` ;
- `--error` : la Quality Gate échoue si une règle bloquante est déclenchée ;
- export SARIF puis `upload-sarif` pour alimenter **Security > Code scanning**.

## Scénario du TP

1. `main` contient les trois workflows et passe au vert.
2. Une branche `feature/user-api` ajoute `server.py` avec deux failles
   intentionnelles : la PR passe au rouge.
3. Le correctif (requête paramétrée + validation IPv4 + exception `nosemgrep`
   documentée) fait repasser la PR au vert.
