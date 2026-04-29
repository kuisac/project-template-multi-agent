# Glossaire métier — `<nom du projet>`

> Maintenu par **Specia** (forme) et alimenté par **Métier** (contenu).
> Toute US ou ADR qui introduit un terme métier doit ajouter ou enrichir une
> entrée ici. Une définition = une phrase + un exemple.

**Convention de tri** : alphabétique. Synonymes regroupés sous le terme canonique.
**Domaine du projet** : industrie / IoT — termes typiques pré-remplis ci-dessous.

---

## A

### Agrégat continu (continuous aggregate)
**Définition** : Vue matérialisée pré-calculée et rafraîchie automatiquement,
qui agrège des données time-series sur des fenêtres temporelles fixes
(minute, heure, jour) pour accélérer les dashboards.
**Exemple** : `temperature_1min` agrège la moyenne, le min et le max de la
table `measurement` par minute et par capteur, rafraîchie toutes les 30s.
**Référencé par** : `doc/technical/data/timeseries-strategy.md`

### Alarme
**Définition** : Notification déclenchée quand une grandeur franchit un seuil
(haut, bas, gradient, déviation) pendant une durée minimale, avec
hystérésis pour éviter les oscillations.
**Anti-pattern** : Notification immédiate sur dépassement sans durée minimale
ni hystérésis (génère un déluge de fausses alarmes).
**Référencé par** : `doc/functional/business-rules.md` R-010

## C

### Calibration
**Définition** : Opération qui ajuste un capteur ou instrument pour que sa
réponse corresponde à une référence connue, avec traçabilité du certificat.
**Exemple** : Capteur de pression calibré annuellement contre un manomètre
étalon, avec dérive maximale tolérée de ±0.2% pleine échelle.

## H

### Historian
**Définition** : Système de stockage long terme des données de processus
industriel, optimisé pour l'écriture massive et la lecture par interpolation.
**Exemples** : OSIsoft PI System (legacy), TimescaleDB, InfluxDB,
AWS Timestream.

### Hystérésis
**Définition** : Différence entre seuil de déclenchement et seuil de retour à
la normale d'une condition, qui empêche les oscillations rapides.
**Exemple** : Climatisation déclenche à 25°C, s'arrête à 22°C. L'hystérésis
de 3°C évite que la clim s'allume / s'éteigne en permanence.

## M

### Mesure (telemetry datapoint)
**Définition** : Quadruplet `(timestamp, valeur, unité, statut)` produit par
un capteur à un instant donné. Une mesure sans son statut est inutilisable.
**Exemple** : `(2026-04-17T14:32:01.123Z, 312.4, K, good)` pour une mesure de
température capteur.
**Référencé par** : `doc/functional/business-rules.md` R-002

## O

### OEE (Overall Equipment Effectiveness)
**Définition** : Indicateur composite de performance d'un équipement de
production, produit de trois ratios : disponibilité × performance × qualité.
**Exemple** : Disponibilité 90% × Performance 95% × Qualité 99% = OEE 84.6%.

### OPC UA
**Définition** : Standard industriel d'échange de données entre équipements
et systèmes (IEC 62541), avec sémantique riche (timestamp, statut, qualité,
modèle d'information).
**Anti-pattern** : Lire une valeur OPC UA sans son champ statut associé.

## S

### Sparkplug B
**Définition** : Spécification de la Eclipse Foundation au-dessus de MQTT qui
ajoute la sémantique industrielle (state management, payload typé) que MQTT
seul n'apporte pas.
**Exemple** : Évite que chaque équipe IoT ré-invente son propre format de
payload MQTT.

### SIL (Safety Integrity Level)
**Définition** : Niveau d'intégrité de sécurité (SIL1 à SIL4) selon
IEC 61508, qui quantifie la probabilité maximale de défaillance d'une
fonction de sécurité.
**Cas particulier** : Une fonction SIL > 0 ne partage jamais son code ni sa
CPU avec la logique de contrôle commande (cf. R-040).

### Statut de mesure
**Définition** : Qualificatif d'une donnée de capteur selon convention OPC UA :
`good`, `bad`, `uncertain`, `stale` (donnée trop ancienne), `forced` (valeur
imposée par opérateur).
**Référencé par** : R-002, R-011

## T

### Tag
**Définition** : Identifiant nommé d'un point de mesure ou de commande dans
un système industriel (équivalent d'une « variable » exposée par l'automate).
**Exemple** : `area01.line02.pump03.flow_setpoint`.

---

## Termes en attente de validation

> Termes proposés par Codie ou Archi mais pas encore validés par Specia ou Métier.

- ...

## Termes dépréciés

> Termes anciens à ne plus utiliser.

- ...
