# Beoordelingsrubric PE - Cloud Infrastructure

**Totaal: 60 punten**
- Minimumvereisten: 60 punten
  - CloudFormation Infrastructure: 30 punten
  - Documentatie: 5 punten
  - Evaluatiepresentatie: 10 punten
  - Extra punten (automatisering): 8 punten
- Extra punten (monitoring - optioneel): 7 punten

---

## 1. CloudFormation Infrastructure (30 punten)

*Deze score omvat single command deployment en alle 3 omgevingen*

### Test Omgeving (5 punten)
| Punten | Criteria |
|--------|----------|
| 5 | **Perfect geïmplementeerd:**<br>- Frontend container draait correct<br>- Backend container draait correct<br>- Single-AZ RDS database (MySQL)<br>- Containers communiceren correct<br>- Frontend → Backend → Database flow werkt<br>- Minimale configuratie zoals gespecificeerd<br>- Deployment werkt met 1 commando |
| 4 | **Goed:**<br>- Alle componenten deployed<br>- Communicatie werkt grotendeels<br>- Kleine configuratie issues<br>- 1 commando deployment met kleine issues |
| 3 | **Voldoende:**<br>- Componenten deployed maar functionele problemen<br>- Communicatie tussen componenten heeft issues<br>- Deployment werkt maar vereist extra stappen |
| 1-2 | **Onvoldoende:**<br>- Ernstige functionele problemen<br>- Componenten communiceren niet goed<br>- Deployment vereist veel manual interventie |
| 0 | Omgeving werkt niet of is niet deploybaar |

### Acceptance Omgeving (10 punten)
| Punten | Criteria |
|--------|----------|
| 9-10 | **Perfect geïmplementeerd:**<br>- Frontend HA: min. 2 containers/tasks over 2+ AZs<br>- Backend HA: min. 2 containers/tasks over 2+ AZs in private subnets<br>- Single-AZ RDS MySQL database<br>- Load balancer (ALB) met health checks<br>- Container orchestration (ECS/EKS) correct geconfigureerd<br>- Autoscaling policies geconfigureerd<br>- Correcte netwerk segmentatie (public/private subnets)<br>- Applicatie volledig functioneel<br>- Deployment met 1 commando |
| 7-8 | **Goed:**<br>- HA geconfigureerd voor frontend en backend<br>- Database correct<br>- Load balancer werkend<br>- Autoscaling aanwezig maar suboptimale configuratie<br>- Netwerk segmentatie grotendeels correct<br>- Kleine issues in configuratie |
| 5-6 | **Voldoende:**<br>- HA gedeeltelijk geïmplementeerd (frontend OF backend)<br>- Autoscaling basis configuratie<br>- Load balancer aanwezig<br>- Netwerk segmentatie heeft problemen<br>- Enkele componenten niet optimaal |
| 3-4 | **Minimaal:**<br>- Resources deployed maar geen echte HA<br>- Beperkte autoscaling<br>- Netwerk segmentatie ontbreekt of incorrect<br>- Functionele problemen |
| 1-2 | Omgeving deployed maar nauwelijks functioneel |
| 0 | Omgeving werkt niet of is niet deploybaar |

### Production Omgeving (15 punten)
| Punten | Criteria |
|--------|----------|
| 14-15 | **Productie-klaar (excellent):**<br>- Volledige HA implementatie (frontend + backend, 2+ AZs)<br>- Geoptimaliseerde autoscaling (target tracking, juiste thresholds)<br>- Single-AZ RDS MySQL productie-configuratie<br>- Correcte netwerk architectuur (public/private subnets, NAT gateway)<br>- Container orchestration (ECS/EKS) productie-klaar<br>- Security groups volgens least privilege<br>- Encryptie at rest geactiveerd voor database<br>- Secrets management geïmplementeerd (Parameter Store of Secrets Manager)<br>- Load balancer (ALB) met health checks en connection draining<br>- ECR image scanning enabled<br>- Bastion host correct geconfigureerd (indien nodig)<br>- Applicatie volledig functioneel en performant<br>- Deployment met 1 commando werkt perfect |
| 11-13 | **Productie-klaar (goed):**<br>- HA volledig geïmplementeerd<br>- Autoscaling werkend maar niet volledig geoptimaliseerd<br>- Database correct geconfigureerd<br>- Netwerk architectuur correct<br>- Container orchestration correct<br>- Security grotendeels correct (kleine issues)<br>- Secrets management aanwezig<br>- 1-2 productie vereisten niet optimaal |
| 8-10 | **Bijna productie-klaar:**<br>- HA geïmplementeerd<br>- Autoscaling basis configuratie<br>- Netwerk segmentatie correct<br>- Container orchestration werkend<br>- Security heeft enkele issues<br>- Secrets management basic<br>- Meerdere vereisten niet optimaal |
| 5-7 | **Basis productie setup:**<br>- HA aanwezig maar niet optimaal<br>- Autoscaling basic<br>- Netwerk segmentatie aanwezig<br>- Security heeft significante issues<br>- Beperkte secrets management<br>- Veel productie vereisten ontbreken |
| 2-4 | **Onvolledige productie:**<br>- HA gedeeltelijk geïmplementeerd<br>- Netwerk basis setup<br>- Significante security problemen<br>- Veel productie vereisten ontbreken |
| 0-1 | Omgeving werkt niet of is niet deploybaar |

---

## 2. Applicatie Vereisten (Opgenomen in CloudFormation score)

### Component Scheiding & Communicatie
| Aspect | Vereist |
|--------|---------|
| ✓ | Frontend, backend en database zijn gescheiden componenten |
| ✓ | Componenten communiceren correct met elkaar |
| ✓ | Frontend → Backend API communicatie werkt |
| ✓ | Backend → Database communicatie werkt |

### Database Implementatie
| Aspect | Vereist |
|--------|---------|
| ✓ | AWS RDS MySQL gebruikt (Aurora optioneel maar niet aanbevolen) |
| ✓ | Database credentials veilig opgeslagen (Parameter Store of Secrets Manager) |
| ✓ | Correcte configuratie per omgeving (Single-AZ voor alle omgevingen) |

### High Availability Implementatie
| Aspect | Vereist |
|--------|---------|
| ✓ | Load balancers geconfigureerd (ALB) |
| ✓ | Health checks actief op container level |
| ✓ | Ongezonde containers/tasks worden automatisch vervangen |
| ✓ | Applicatie blijft beschikbaar bij uitval van 1 container (demonstreerbaar) |
| ✓ | Container orchestration (ECS of EKS) correct geconfigureerd |

### Container Orchestration
| Aspect | Vereist |
|--------|---------|
| ✓ | ECS of EKS gebruikt (niet EC2 instances direct) |
| ✓ | Voor ECS: Fargate of EC2 launch type |
| ✓ | Voor EKS: Managed node groups of Fargate |
| ✓ | Containers draaien in private subnets (backend) |
| ✓ | Frontend containers bereikbaar via ALB |
| ✓ | Container images in ECR |
| ✓ | Task definitions / Pod specs correct geconfigureerd |

---

## 3. Extra Punten - Geavanceerde Automatisering (8 punten)

**LET OP:** Deze punten worden alleen toegekend als minimumvereisten (30p CloudFormation) behaald zijn.

### Packaging & Deployments (3 punten)
| Punten | Criteria |
|--------|----------|
| 3 | **Excellent:**<br>- Nested stacks correct gebruikt<br>- Herbruikbare templates<br>- CloudFormation packages correct ingezet<br>- Volledig geautomatiseerd deploy script<br>- CI/CD pipeline geïmplementeerd (bijv. GitHub Actions) |
| 2 | **Goed:**<br>- Nested stacks of herbruikbare templates<br>- Deploy script aanwezig<br>- Goede structuur maar kan geoptimaliseerd worden |
| 1 | **Basis:**<br>- Enkele herbruikbare elementen<br>- Basis deployment automatisering<br>- Veel ruimte voor verbetering |
| 0 | **Onvoldoende:**<br>- Weinig tot geen herbruikbaarheid<br>- Grotendeels manual proces |

### Gelaagde Stacks en Modules (2 punten)
| Punten | Criteria |
|--------|----------|
| 2 | **Excellent:**<br>- Modulaire opzet (netwerk, compute, database als aparte stacks)<br>- Cross-stack references correct gebruikt<br>- Dependencies goed beheerd<br>- Logische scheiding van concerns<br>- Stacks kunnen onafhankelijk ge-update worden |
| 1 | **Basis:**<br>- Enkele modulaire elementen<br>- Basic stack scheiding<br>- Dependencies niet optimaal |
| 0 | **Onvoldoende:**<br>- Monolithische template(s)<br>- Geen modulaire opzet |

### Pseudo-parameters en Dynamische Referenties (1 punt)
| Punten | Criteria |
|--------|----------|
| 1 | **Excellent:**<br>- AWS pseudo-parameters gebruikt (::StackName, ::Region, ::AccountId)<br>- Dynamic references voor Parameter Store/Secrets Manager<br>- Intrinsic functions correct toegepast (Fn::GetAtt, Fn::Sub, Fn::Join, etc.)<br>- Vermindert hardcoding significant |
| 0 | **Onvoldoende:**<br>- Geen of nauwelijks gebruik van deze concepten<br>- Veel hardcoded waarden |

### Conditions (2 punten)
| Punten | Criteria |
|--------|----------|
| 2 | **Excellent:**<br>- Conditions gebruikt voor environment-specifieke resources<br>- Conditional resource creation<br>- Conditional parameters<br>- Logische operators (And, Or, Not) toegepast<br>- DRY principe toegepast (1 template, 3 omgevingen) |
| 1 | **Basis:**<br>- Enkele conditions gebruikt<br>- Basis conditional logic<br>- Nog aparte templates per omgeving |
| 0 | **Onvoldoende:**<br>- Geen conditions gebruikt<br>- Aparte templates voor elke omgeving |

---

## 4. Monitoring - Datadog (7 punten - EXTRA/OPTIONEEL)

**LET OP:** Dit is een **optioneel** onderdeel voor extra punten. Niet verplicht voor de minimumvereisten.

### Datadog Installatie & Automatisering (2 punten)
| Punten | Criteria |
|--------|----------|
| 2 | Datadog agent volledig geautomatiseerd via CloudFormation op alle componenten, configuratie per omgeving, API keys veilig opgeslagen |
| 1 | Geautomatiseerde installatie maar kleine manual stappen nodig of configuratie niet volledig per omgeving |
| 0 | Niet geïmplementeerd, grotendeels manual, of niet werkend |

### Dashboards per Omgeving (5 punten)

**Totaal voor alle omgevingen (Test/Acceptance/Production):**

| Punten | Criteria |
|--------|----------|
| 5 | **Volledig dashboard voor elke omgeving:**<br>- APM metrics (request rate, response times, errors, traces)<br>- Container metrics (CPU, memory, running tasks/pods, restarts)<br>- Database metrics (query performance, connections, CPU/memory)<br>- RUM metrics (page load times, sessions, errors)<br>- Autoscaling metrics (scaling events, health checks)<br>- Duidelijke visualisaties en logische indeling<br>- Alle 3 omgevingen hebben complete dashboards |
| 3-4 | **Meeste metrics:**<br>- 3-4 van de 5 metric categorieën volledig<br>- 1-2 omgevingen hebben complete dashboards<br>- Visualisaties aanwezig maar kunnen beter |
| 1-2 | **Basis metrics:**<br>- 2-3 van de 5 metric categorieën<br>- Basics van monitoring aanwezig<br>- Visualisaties basic<br>- Niet alle omgevingen hebben dashboards |
| 0 | **Onvoldoende:**<br>- Geen betekenisvolle metrics<br>- Dashboards ontbreken of zijn niet bruikbaar |

---

## 5. Documentatie (5 punten)

### Structuur en Volledigheid (3 punten)
| Punten | Criteria |
|--------|----------|
| 3 | **Excellent:**<br>- Alle verplichte secties aanwezig (overzicht, deployment, technische details, per omgeving, gemaakte keuzes)<br>- Architectuur diagrammen duidelijk en compleet<br>- Deployment instructies stap-voor-stap en werkend<br>- Prerequisites duidelijk vermeld<br>- Code snippets waar relevant<br>- Screenshots van deployed omgevingen |
| 2 | **Goed:**<br>- Meeste secties aanwezig<br>- Architectuur diagram aanwezig<br>- Deployment instructies grotendeels compleet<br>- 1-2 kleine onderdelen ontbreken |
| 1 | **Basis:**<br>- Basis documentatie aanwezig<br>- Belangrijke onderdelen ontbreken<br>- Instructies onvolledig<br>- Weinig visuele ondersteuning |
| 0 | **Onvoldoende:**<br>- Minimale documentatie<br>- Meeste secties ontbreken<br>- Niet bruikbaar om oplossing te begrijpen |

### Kwaliteit en Duidelijkheid (2 punten)
| Punten | Criteria |
|--------|----------|
| 2 | **Excellent:**<br>- Professioneel geschreven<br>- Technisch accuraat<br>- Duidelijke uitleg van keuzes en afwegingen (vooral ECS vs EKS)<br>- Goed gestructureerd en leesbaar<br>- Markdown correct gebruikt<br>- Screenshots van werkende oplossing |
| 1 | **Basis:**<br>- Begrijpbaar maar kan beter<br>- Enkele onduidelijkheden<br>- Basis structuur<br>- Weinig uitleg van keuzes |
| 0 | **Onvoldoende:**<br>- Onduidelijk of verwarrend<br>- Technische fouten<br>- Slecht gestructureerd |

---

## 6. Evaluatiepresentatie (10 punten)

### Demonstratie (4 punten)
| Punten | Criteria |
|--------|----------|
| 4 | **Excellent:**<br>- Applicatie werkt perfect (functionaliteit + HA)<br>- Live deployment verloopt smooth<br>- HA overtuigend gedemonstreerd (instance stoppen, app blijft werken)<br>- Binnen tijdslimiet (15 min)<br>- Professionele presentatie |
| 3 | **Goed:**<br>- Applicatie werkt<br>- Deployment werkt met kleine issues<br>- HA getoond<br>- Binnen tijdslimiet<br>- Goede presentatie |
| 2 | **Voldoende:**<br>- Applicatie werkt grotendeels<br>- Deployment werkt met issues<br>- HA niet overtuigend getoond<br>- Tijdslimiet overschreden of rommelige presentatie |
| 1 | **Onvoldoende:**<br>- Applicatie heeft problemen<br>- Deployment faalt of werkt niet<br>- HA niet getoond |
| 0 | Geen werkende demonstratie |

### Technische Kennis (4 punten)
| Punten | Criteria |
|--------|----------|
| 4 | **Excellent:**<br>- Alle AWS services kunnen uitgelegd worden<br>- CloudFormation concepten volledig begrepen<br>- Kan architectuur beslissingen goed verdedigen<br>- Begrijpt interacties tussen componenten<br>- Kan kritische vragen beantwoorden |
| 3 | **Goed:**<br>- Meeste services kunnen uitgelegd worden<br>- CloudFormation basis concepten begrepen<br>- Kan meeste beslissingen verdedigen<br>- Kan standaard vragen beantwoorden |
| 2 | **Voldoende:**<br>- Basis kennis van gebruikte services<br>- Moeite met uitleggen van keuzes<br>- Onduidelijk over sommige implementaties<br>- Kan alleen eenvoudige vragen beantwoorden |
| 1 | **Onvoldoende:**<br>- Weinig begrip van gebruikte technologieën<br>- Kan beslissingen niet verdedigen<br>- Kan geen vragen beantwoorden |
| 0 | Geen kennis aanwezig |

### AWS Console & Monitoring (2 punten)
| Punten | Criteria |
|--------|----------|
| 2 | **Excellent:**<br>- Kan alle deployed resources tonen en uitleggen<br>- Navigeert vlot door AWS Console<br>- Voor ECS: toont clusters, services, tasks, task definitions<br>- Voor EKS: toont cluster, nodes, en gebruikt kubectl<br>- Toont ECR repositories en images<br>- Als Datadog geïmplementeerd: dashboards tonen relevante data<br>- Kan metrics interpreteren |
| 1 | **Basis:**<br>- Kan resources tonen<br>- Basis navigatie in Console<br>- Kan belangrijkste componenten uitleggen<br>- Beperkte interpretatie |
| 0 | **Onvoldoende:**<br>- Kan resources niet vinden/tonen<br>- Geen begrip van deployed componenten |

---

## 7. Verplichte Vereisten (Pass/Fail)

Deze vereisten moeten voldaan zijn, anders resulteert dit in een **'0' voor de volledige PE**:

| Vereiste | Pass | Fail |
|----------|------|------|
| **Git Commits** | Minimaal 1 commit per uur werk, regelmatige commits tonen progressie | Onvoldoende commits of verdachte commit pattern |
| **Deadline** | Indiening voor 10/12 om 23:00 | Te laat ingediend |
| **Plagiaat** | Eigen werk, geen gekopieerde code/oplossingen | Plagiaat gedetecteerd |
| **Wijzigingen na deadline** | Alle wijzigingen expliciet vermeld bij start verdediging | Niet vermelde wijzigingen |
| **Individueel werk** | Volledig zelfstandig gemaakt | Bewijs van samenwerking |

---

## Punten Overzicht

| Component | Punten |
|-----------|--------|
| **CloudFormation Infrastructure** | **30** |
| - Test omgeving | (5) |
| - Acceptance omgeving | (10) |
| - Production omgeving | (15) |
| **Documentatie** | **5** |
| - Structuur en volledigheid | (3) |
| - Kwaliteit en duidelijkheid | (2) |
| **Evaluatiepresentatie** | **10** |
| - Demonstratie | (4) |
| - Technische kennis | (4) |
| - AWS Console & Monitoring | (2) |
| **Subtotaal Minimumvereisten** | **45** |
| **Monitoring (Datadog) - EXTRA/OPTIONEEL** | **+7** |
| - Automatisering | (2) |
| - Dashboards (alle omgevingen) | (5) |
| **Extra Punten (Automatisering)** | **8** |
| - Packaging & Deployments | (3) |
| - Gelaagde stacks en modules | (2) |
| - Pseudo-parameters en dynamic references | (1) |
| - Conditions | (2) |
| **TOTAAL MOGELIJK** | **60** |

**Minimaal te behalen voor presentatie:** 20 punten CloudFormation Infrastructure

**Slagingsgrens PE:** 30/60 punten (50%)


---

## Veelvoorkomende Aftrekpunten

| Issue | Aftrek |
|-------|--------|
| Hardcoded credentials in code | -2 tot -5 punten |
| Geen netwerk segmentatie | -3 tot -5 punten |
| Security groups te permissive (0.0.0.0/0 voor private resources) | -2 tot -3 punten |
| Geen health checks op containers | -2 punten |
| Applicatie niet bereikbaar na demo | -3 tot -5 punten |
| HA niet demonstreerbaar (container kill test) | -3 tot -5 punten |
| Deployment duurt >10 minuten zonder uitleg | -1 tot -2 punten |
| Code/configuratie rommelig zonder comments | -1 tot -2 punten |
| EC2 instances direct gebruikt (geen ECS/EKS) | -10 punten |
| Geen container orchestration | -10 punten |
| Container images niet in ECR | -2 punten |

---

## Tips voor Maximale Score

1. **Test vroeg en vaak** - Deploy regelmatig om problemen vroeg te detecteren
2. **Automatiseer alles** - Manual stappen = lagere score
3. **Documenteer tijdens development** - Niet op het laatste moment
4. **Security first** - Geen shortcuts bij beveiliging
5. **Gebruik Conditions** - 1 template voor 3 omgevingen is beter dan 3 templates
6. **Modulariseer** - Nested stacks maken onderhoud makkelijker
7. **Test je demo** - Oefen de volledige presentatie meerdere keren (inclusief HA test!)
8. **Commit regelmatig** - Bescherm jezelf met een goede commit history
9. **Container orchestration** - Kies ECS of EKS vroeg en leer het goed kennen
10. **Clean code** - Gebruik comments en duidelijke resource namen
11. **Motiveer je keuzes** - Vooral de keuze tussen ECS en EKS goed documenteren
12. **Datadog optioneel** - Focus eerst op basis infrastructuur, Datadog is bonus

---

*Laatste update: November 2025*
