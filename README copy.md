[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/i24jwLeu)
# Zoveelste To-Do Applicatie voor de wereld

## Beschrijving
In het huidige digitale tijdperk zijn webapplicaties de ruggengraat geworden van talloze bedrijven en diensten. Het ontwikkelen van een goed gestructureerde en schaalbare webapplicatie is essentieel voor het bieden van een naadloze gebruikerservaring.

Om onze reis naar een naadloze cloudomgeving voort te zetten, willen we deze applicatie migreren naar een gecontaineriseerde versie die in de cloud draait. We willen graag dat jij deze migratie voor ons uitvoert.

## Architectuur

![Architectuur Diagram](/images/Architecture.png)
Dit is de huidige applicatiearchitectuur. Gebruik dit als benchmark voor beveiliging, hoge beschikbaarheid en prestaties.

**health check:** De backend bevat een health endpoint die indien nodig als health check kan worden gebruikt.

**Informatie over deployment:** / configuratie kan altijd worden gevonden in het README.md bestand van de verschillende componenten.

## Technologie

De opdracht is om de applicatie volledig geautomatiseerd te deployen naar een AWS omgeving met behulp van AWS CloudFormation.

**Container Orchestration - VERPLICHT:**
- De applicatie MOET gedeployed worden op **AWS ECS (Elastic Container Service)** of **AWS EKS (Elastic Kubernetes Service)**
- EC2 instances mogen NIET gebruikt worden voor het hosten van de applicatie containers
- Keuze tussen ECS of EKS moet gemotiveerd worden in de documentatie
- Container orchestration moet volledig geconfigureerd zijn via CloudFormation

**Build Pipeline:**
- De applicatie- en weblaag moeten gedockerizeerd worden
- Container images moeten automatisch gebouwd worden (bijvoorbeeld via GitHub Actions)
- Images moeten beschikbaar zijn in een container registry (ECR aanbevolen)
- Image tags moeten versioned zijn

**High Availability & Scalability:**
- Beide frontend en backend moeten hoogbeschikbaar zijn (multiple tasks/pods over multiple availability zones)
- Autoscaling moet geconfigureerd zijn om te reageren op veranderende load (ECS Service Auto Scaling of Kubernetes HPA)
- De applicatie moet bestand zijn tegen het falen van individuele containers/nodes
- Voor EKS: worker nodes moeten verspreid zijn over meerdere AZs
- Voor ECS: tasks moeten verspreid zijn over meerdere AZs

**Toegankelijkheid:**
- De applicatie moet bereikbaar zijn via **één IP-adres of hostname**
- Load balancing moet voorzien zijn om verkeer te distribueren (ALB of NLB)

## Beveiliging & Compliance

**Netwerk Segmentatie:**
- Intern en extern verkeer moet gescheiden zijn
- Gebruik verschillende subnets voor internet-facing en private componenten
- Configureer NAT gateways voor private resources die internet toegang nodig hebben
- Public subnets voor internet-facing resources
- Private subnets voor backend en database componenten

**Access Control:**
- Implementeer het principe van least privilege
- Gebruik security groups om verkeer tussen componenten te controleren
- Gebruik indien nodig Network ACLs voor extra beveiliging
- De IAM rol "LabAccess" is beschikbaar voor het koppelen van policies

**Beheer & Toegang:**
- ECS/EKS worker nodes moeten toegankelijk zijn via een bastion host (indien directe toegang nodig is voor debugging)
- De bastion host is de enige machine met directe SSH toegang van buitenaf
- Voor EKS: gebruik kubectl via bastion of AWS Systems Manager Session Manager
- Voor ECS: gebruik ECS Exec voor container toegang
- Containers zelf hebben geen directe SSH toegang nodig

**Data Beveiliging:**
- Encryptie at rest moet waar mogelijk geactiveerd zijn
- API keys, wachtwoorden en andere gevoelige informatie mogen NIET hardcoded worden in IaC
- Gebruik AWS Secrets Manager of Parameter Store voor gevoelige gegevens
- Container images in ECR moeten scan enabled hebben voor security vulnerabilities 

## Monitoring [extra]

**Datadog Implementatie:**
- Installeer Datadog agents op alle componenten van je infrastructuur
  - Voor ECS: gebruik Datadog ECS Task Definition of sidecar containers
  - Voor EKS: gebruik Datadog Kubernetes DaemonSet
- De installatie van de Datadog agent moet geautomatiseerd zijn via CloudFormation
- Configuratie moet per omgeving verschillend kunnen zijn
- API keys voor Datadog moeten veilig opgeslagen worden (niet hardcoded)

**Dashboards:**
Creëer per omgeving (Test/Acceptance/Production) een dashboard met:
- APM (Application Performance Monitoring) metrics voor de applicatie
- Container metrics (CPU, memory, running tasks/pods)
- Database metrics (queries, connections, performance)
- RUM (Real User Monitoring) metrics voor frontend gebruikerservaring
- Autoscaling metrics (CPU, memory, aantal instances)
- Health check status van alle componenten

# Evaluatie (60p)

## **Minimumvereisten:**

### CloudFormation Infrastructure (30p)

De volledige infrastructuur moet deploybaar zijn met **1 (één) CloudFormation commando**. Een parameter moet meegegeven worden om te bepalen voor welke omgeving wordt gedeployed (Test/Acceptance/Production).

**Voorbeeld deployment commando:**
```bash
aws cloudformation deploy --template-file template.yaml --parameter-overrides Environment=Production
```

De infrastructuur moet deploybaar zijn in 3 verschillende omgevingen met de volgende specificaties:

#### **Test Omgeving (5p)**
*Doel: Functioneel testen met minimale kosten*

**Vereisten:**
- **Container Orchestration:** ECS of EKS basis configuratie
  - Enkele task/pod van frontend is voldoende
  - Enkele task/pod van backend is voldoende
  - Voor EKS: 1-2 worker nodes is voldoende
  - Voor ECS: Fargate of minimale EC2 capacity
- **High Availability:** NIET vereist
- **Netwerk:** Basis netwerk setup is voldoende
- **Database:** Single-AZ RDS met tst/dev template (MySQL of Aurora)
- **Scaling:** Geen autoscaling vereist
- **Kosten:** Minimaal (gebruik kleinste task sizes / instance types)

#### **Acceptance Omgeving (10p)**
*Doel: Volledige acceptance testing met productie-gelijke setup*

**Vereisten:**
- **Container Orchestration:** ECS of EKS met HA configuratie
  - Minimaal 2 frontend tasks/pods over 2 verschillende Availability Zones
  - Minimaal 2 backend tasks/pods over 2 verschillende Availability Zones
  - Voor EKS: minimaal 2 worker nodes verspreid over 2+ AZs
  - Voor ECS Fargate: tasks verspreid over 2+ AZs
  - Voor ECS EC2: minimaal 2 container instances over 2+ AZs
  - Load balancer (ALB) voor distributie van verkeer
- **High Availability:** VERPLICHT
- **Netwerk:** 
  - Frontend tasks/pods bereikbaar via public load balancer
  - Backend tasks/pods in private subnets (GEEN directe internet toegang)
  - Database in private subnets
- **Database:** Single-AZ RDS met tst/dev template (MySQL of Aurora)
- **Scaling:** 
  - ECS Service Auto Scaling of Kubernetes HPA geconfigureerd voor frontend
  - ECS Service Auto Scaling of Kubernetes HPA geconfigureerd voor backend
  - Scaling policies gedefinieerd (bijv. CPU > 70% of request count)

#### **Production Omgeving (15p)**
*Doel: Productie-klare omgeving met optimale performance en beveiliging*

**Vereisten:**
- **Container Orchestration:** ECS of EKS productie-klaar
  - Minimaal 2 frontend tasks/pods over minimaal 2 Availability Zones
  - Minimaal 2 backend tasks/pods over minimaal 2 Availability Zones
  - Voor EKS: minimaal 3 worker nodes verspreid over 3 AZs
  - Voor ECS Fargate: tasks optimaal verspreid
  - Voor ECS EC2: minimaal 3 container instances over 3 AZs
  - Load balancer met health checks en connection draining
- **High Availability:** VERPLICHT en GEOPTIMALISEERD
- **Netwerk:**
  - Frontend tasks/pods bereikbaar via public load balancer
  - Backend tasks/pods in private subnets (GEEN directe internet toegang)
  - Database in private subnets
  - Bastion host voor beheer (indien nodig)
- **Database:** Single-AZ RDS met tst/dev template (MySQL of Aurora)
- **Scaling:**
  - Geoptimaliseerde autoscaling configuratie (ECS Service Auto Scaling of Kubernetes HPA)
  - Target tracking scaling policies (CPU, memory, of custom metrics)
  - Juiste min/max/desired capacity voor productie load
  - Voor EKS: Cluster Autoscaler of Karpenter geconfigureerd
  - Voor ECS EC2: Auto Scaling Group voor container instances
- **Monitoring [extra]:** Volledige Datadog integratie
- **Beveiliging:** 
  - Encryptie at rest voor database
  - Secrets management voor gevoelige data
  - Container image scanning enabled in ECR


### Applicatie Vereisten

**Container Orchestration:**
- Frontend en backend moeten draaien als containers in ECS of EKS
- Containers moeten health checks hebben geconfigureerd
- Container resources (CPU, memory) moeten correct gedefinieerd zijn
- Voor productie: resource limits en requests moeten optimaal gezet zijn

**Architectuur:**
- Alle componenten moeten gescheiden zijn:
  - Frontend (web layer) - als container(s)
  - Backend (application layer) - als container(s)
  - Database - als managed RDS service
- Componenten communiceren met elkaar via netwerkverbindingen
- De frontend communiceert met de backend via API calls (via service discovery of load balancer)
- De backend communiceert met de database

**Database:**
- Gebruik AWS RDS (MySQL of Aurora)
- Database credentials moeten veilig opgeslagen worden (AWS Secrets Manager of Parameter Store)
- Containers moeten credentials ophalen via environment variables of mounted secrets

**High Availability:**
- Implementatie volgens de vereisten per omgeving (zie boven)
- Container health checks moeten geconfigureerd zijn (liveness & readiness)
- Load balancers moeten ongezonde containers/tasks detecteren en verkeer stoppen
- Voor EKS: pod disruption budgets overwegen voor productie
- Voor ECS: deployment configuration met minimum healthy percent

**Scaling:**
- Autoscaling moet geoptimaliseerd zijn voor productie workloads
- Scaling policies moeten gebaseerd zijn op relevante metrics (CPU, memory, request count)
- Voor EKS: Horizontal Pod Autoscaler (HPA) en optioneel Cluster Autoscaler
- Voor ECS: Service Auto Scaling met target tracking

**Documentatie:**
- Alle implementatiestappen moeten gedocumenteerd zijn in 1 markdown document op GitHub
- Inclusief:
  - Architectuur diagrammen (inclusief ECS/EKS setup)
  - Keuze tussen ECS en EKS met motivatie
  - Deployment instructies
  - Container configuratie uitleg
  - Screenshots van werkende oplossing
  - Uitleg van gemaakte keuzes



**Bovenstaande vereisten zijn het **minimum** om tot de evaluatiepresentatie te komen en beoordeeld te worden op extra's en documentatie.**

## **Extra Punten** (8p)

Geavanceerde automatiseringsconcepten worden alleen beoordeeld als het minimumniveau is bereikt.

**Beoordelingscriteria:**

1. **Packaging & Deployments (+3p)**
   - Gebruik van nested stacks
   - Herbruikbare templates
   - Proper gebruik van CloudFormation packages
   - Deploy scripts die het volledige proces automatiseren

2. **Gelaagde Stacks en Modules (+2p)**
   - Modulaire opzet (netwerk, compute, database als aparte stacks)
   - Cross-stack references
   - Dependency management tussen stacks
   - Logische scheiding van concerns

3. **Pseudo-parameters en Dynamische Referenties (+1p)**
   - Gebruik van AWS::StackName, AWS::Region, AWS::AccountId
   - Dynamic references voor Secrets Manager/Parameter Store
   - Intrinsic functions (Fn::GetAtt, Fn::Sub, Fn::Join, etc.)

4. **Conditions (+2p)**
   - Environment-specifieke resources via Conditions
   - Conditional resource creation
   - Conditional parameters
   - Logische operators (And, Or, Not)

### Monitoring Vereisten (7p)

**Datadog Implementatie:**
- Datadog agents geïnstalleerd op alle componenten
  - Voor ECS: Datadog agent als sidecar container of via ECS Task Definition
  - Voor EKS: Datadog agent via DaemonSet
- Installatie volledig geautomatiseerd via CloudFormation
- Configuratie per omgeving mogelijk via parameters
- Container metrics moeten zichtbaar zijn in Datadog

**Dashboards per Omgeving:**
Elk dashboard (Test/Acceptance/Production) moet minimaal bevatten:

1. **APM Metrics:**
   - Request rate
   - Response times
   - Error rates
   - Transaction traces

2. **Container Metrics:**
   - Running tasks/pods count per service
   - CPU usage per container
   - Memory usage per container
   - Container restarts
   - For EKS: Node metrics

3. **Database Metrics:**
   - Query performance
   - Connection count
   - Database CPU/Memory
   - Slow query log

4. **RUM Metrics:**
   - Page load times
   - User sessions
   - JavaScript errors
   - Core Web Vitals

5. **Autoscaling & Health Metrics:**
   - Aantal actieve tasks/pods per service
   - CPU/Memory usage per container
   - Health check status (container level)
   - Scaling events (scale up/down)
   - For EKS: Node count en node health
   - For ECS: Container instance metrics (indien EC2 launch type)
   - Scaling events (scale up/down)

<br><br>

## **Evaluatiestappen:**
--- 


### **7/12 om 23:00 - Deadline Indiening**

**Wat in te dienen:**
- Volledige CloudFormation templates
- ECS Task Definitions of Kubernetes manifests (geïntegreerd in CloudFormation)
- Build pipeline configuratie (GitHub Actions of andere)
- Dockerfile(s) voor frontend en backend
- Applicatie code (indien aangepast)
- **Documentatie** (zie hieronder)

De indiening moet gebeuren via je GitHub repository. De timestamp van je laatste commit vóór de deadline telt.

### **Documentatie (5p)**

**Format:** 
- 1 markdown document in je GitHub repository
- Bestandsnaam: `DOCUMENTATION.md` of `README.md`

**Verplichte Inhoud:**

1. **Overzicht**
   - Korte beschrijving van de oplossing
   - **Keuze tussen ECS of EKS met motivatie**
   - Architectuur diagram van de uiteindelijke implementatie (inclusief container orchestration)

2. **Deployment Instructies**
   - Stap-voor-stap instructies om de oplossing te deployen
   - Vereiste prerequisites (AWS CLI, kubectl (EKS), docker, credentials, etc.)
   - Exacte commando's om te deployen

3. **Technische Details per Component**
   - Netwerk architectuur (VPC, subnets, routing)
   - Container orchestration setup (ECS clusters/services of EKS cluster/deployments)
   - Container configuratie (task definitions / pod specs)
   - Database setup
   - Load balancing (ALB configuration)
   - Security configuratie (IAM roles, security groups)
   - Monitoring setup (Datadog integration)

4. **Per Omgeving**
   - Verschillen tussen Test/Acceptance/Production
   - Hoe de parameter switching werkt
   - Container scaling configuratie per omgeving
   - Screenshots van deployed omgevingen (AWS Console + Datadog)

5. **Gemaakte Keuzes**
   - **Waarom ECS of EKS gekozen (belangrijkste onderdeel)**
   - Voor EKS: Waarom Fargate of managed node groups
   - Voor ECS: Waarom Fargate of EC2 launch type
   - Afwegingen tussen alternatieven
   - Optimalisaties die zijn toegepast

**Belangrijke Waarschuwing:**
- Als je oplossing tijdens de verdediging anders is dan op het moment van de deadline, moet dit EXPLICIET vermeld worden bij de start van de presentatie
- Een volledige lijst van wijzigingen moet gegeven worden
- **Het niet vermelden resulteert in een '0' voor de volledige PE**
- De beoordeling is gebaseerd op de staat van de indiening op het moment van de deadline
<br><br>

### **Les van 8-9/12 - Evaluatiepresentatie (10p)**

**Tijdschema:** 
Wordt gepubliceerd op Blackboard de week voor de presentaties

**Voorbereiding:**
- Zorg dat je AWS omgeving toegankelijk is
- 1 omgeving moet reeds gedeployed zijn (jouw keuze: Test/Acceptance/Production)
- Voor EKS: kubectl geconfigureerd en werkend
- Zorg voor een stabiele internetverbinding
- Heb je documentatie open en beschikbaar

**Verloop van de Demo (max. 15 minuten):**

1. **Demonstratie Werkende Applicatie (3-4 min)**
   - Toon de applicatie werkt (functionaliteit)
   - Demonstreer high availability:
     - Voor ECS: stop een task, toon dat service automatisch nieuwe task start
     - Voor EKS: delete een pod, toon dat replica set nieuwe pod creëert
   - Toon dat de applicatie bereikbaar blijft via 1 endpoint

2. **Live Deployment (5-6 min)**
   - Deploy 1 omgeving live (keuze van de lector)
   - Demonstreer dat het met 1 commando werkt
   - Verklaar wat er gebeurt tijdens de deployment
   - Toon container startup in ECS/EKS console

3. **AWS Console & Container Platform Walkthrough (3-4 min)**
   - Toon de deployed resources in de AWS Console
   - Voor ECS: toon clusters, services, tasks, task definitions
   - Voor EKS: toon cluster, worker nodes, en gebruik kubectl om pods te tonen
   - Verklaar de opzet van elke component
   - Toon security groups, load balancers, databases, ECR repositories

4. **Datadog Dashboard [extra] (2-3 min)**
   - Toon de Datadog dashboards per omgeving
   - Verklaar de zichtbare metrics (inclusief container metrics)

5. **Vragen & Antwoorden**
   - Lector stelt vragen over implementatie
   - Verdedig gemaakte keuzes (vooral ECS vs EKS keuze)

**Verwachtingen:**

**Technische Kennis:**
- Je kunt alle gebruikte AWS services uitleggen (ECS/EKS, ECR, ALB, RDS, etc.)
- Je begrijpt hoe containers werken en hoe ze met elkaar communiceren
- **Je kunt de keuze tussen ECS en EKS goed verdedigen**
- Je begrijpt container orchestration concepten (scheduling, service discovery, health checks)
- Voor EKS: je begrijpt Kubernetes basics (pods, deployments, services)
- Voor ECS: je begrijpt ECS concepten (tasks, services, clusters)
- Je kunt CloudFormation syntax en concepten uitleggen

**Demonstratie:**
- De applicatie werkt zonder errors
- High availability is aantoonbaar (container kan gestopt worden)
- Deployment werkt smooth
- Containers starten correct op
- Monitoring is zichtbaar in Datadog met container metrics [extra]

**Communicatie:**
- Duidelijke uitleg van technische concepten
- Kunnen beantwoorden van kritische vragen
- Professionele presentatie
<br><br>

# Belangrijk

## Academische Integriteit

**Plagiaat:**
- Plagiaat is NIET toegestaan (zie PXL examenregeling)
- Straffen variëren van puntenaftrek tot uitsluiting van alle examens
- Zowel het kopiëren als het delen van oplossingen wordt als plagiaat beschouwd
- De persoon die zijn/haar oplossing deelt is evenzeer schuldig

**Samenwerking:**
- Dit is een **individuele opdracht**
- Geen enkele vorm van communicatie over de PE met medestudenten is toegestaan
- Geen code delen, geen screenshots delen, geen ideeën bespreken
- Overtreding wordt beschouwd als plagiaat

## Git Workflow Vereisten

**Commit Frequentie:**
- Minimaal **1 commit per uur werk**
- Commits moeten betekenisvolle messages hebben
- Commit history moet progressie van het werk tonen

**Sanctie:**
- Het niet naleven van de commit frequentie resulteert automatisch in een **'0' voor de volledige PE**
- Geen uitzonderingen

## Checklist voor Indiening

Controleer voor de deadline:
- [ ] CloudFormation templates zijn volledig en werken
- [ ] Build pipeline is geconfigureerd
- [ ] Alle 3 omgevingen zijn deploybaar
- [ ] Documentatie is compleet
- [ ] Datadog dashboards zijn aangemaakt
- [ ] Git history toont regelmatige commits
- [ ] Gevoelige informatie is niet hardcoded
- [ ] Repository is toegankelijk voor docent

## Licentie

Deze bibliotheek is gelicenseerd onder de MIT-0 Licentie. Zie het [LICENSE](LICENSE) bestand.
