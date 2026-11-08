# Git et publication GitHub

## État au 8 novembre 2026

- Dépôt fourni par l'étudiant : <https://github.com/Hugodrc55/ENSO-Monitor>.
- Distant `origin` : `https://github.com/Hugodrc55/ENSO-Monitor.git`.
- Branche locale : `main`. Le dépôt distant était vide lors de la consultation.
- Le Jour 1, développé le 4 novembre, est organisé en commits locaux le 8 novembre.
- **Aucun push effectué.** Le contrôle automatique a refusé la publication faute
  d'autorisation explicite d'envoyer ces fichiers à cette destination. L'accord
  de l'étudiant est demandé avant toute nouvelle tentative.

## Commits du Jour 1

| Ensemble cohérent | Message |
| --- | --- |
| Conventions Git et structure | `chore: initialiser le dépôt et ses conventions` |
| API et test de santé | `feat: ajouter la route de santé FastAPI et son test` |
| Accueil React et communication API | `feat: relier l'accueil React à l'API` |
| Documentation et préparation de la publication | `docs: documenter le jour 1 et préparer sa publication` |

Ces commits correspondent au travail réel du Jour 1 et à son suivi. Ils ne
représentent pas quatre journées différentes et ne sont pas antidatés.
L'identité Git préexistante a été conservée.

## Consulter le travail avant publication

Depuis la racine du projet :

```powershell
git status --short --branch
git remote -v
git log --oneline --reverse
git show --stat HEAD
git diff HEAD~3 HEAD
git ls-tree -r --name-only HEAD
git check-ignore -v docs/sujet/HETIC_WEB3_Projet_ENSO_Monitor.pdf backend/.venv frontend/node_modules
```

La comparaison `HEAD~3 HEAD` montre les trois commits suivant le premier ;
`git show --root d2fc989` permet de lire aussi le commit initial.
Les 28 fichiers de code, configuration et documentation sont destinés au dépôt.
Le PDF officiel, `.env`, les dépendances installées et les fichiers temporaires
sont exclus. Le contrôle de motifs usuels de secrets n'a rien détecté ; il ne
remplace pas une revue complète du contenu.

## Premier push, après autorisation explicite

`origin` est déjà configuré : ne pas refaire `git remote add origin`.

```powershell
git push -u origin main
```

Cette commande envoie les commits et les fichiers suivis vers GitHub, où leur
accès dépend de la visibilité et des permissions du dépôt. Git peut demander une
authentification. Ne jamais placer un jeton dans l'URL ou dans un fichier du projet.

Si le distant a reçu d'autres commits entre-temps, examiner l'historique avant de
poursuivre. Aucun force-push, aucune réécriture d'historique.

## Vérifier le résultat du push

```powershell
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Le SHA local doit être identique à celui de `refs/heads/main` sur GitHub. Ne
déclarer la publication réussie qu'après cette vérification et consigner le
résultat réel dans le journal.

## Pour une prochaine modification autorisée

```powershell
git status --short
git diff
```

Ajouter uniquement les fichiers concernés, puis examiner l'index :

```powershell
git diff --cached --check
git diff --cached
```

Après revue et vérification, créer un commit précis avec `git commit -m`, puis
pousser seulement dans le périmètre autorisé. Ne pas recréer les commits initiaux.
