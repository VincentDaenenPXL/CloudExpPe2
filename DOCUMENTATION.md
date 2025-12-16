# Documentatie: To-Do Applicatie in AWS CloudFormation

Dit document beschrijft de implementatie van de gecontaineriseerde To-Do applicatie in AWS, volledig geautomatiseerd met CloudFormation. Het doel is om een schaalbare, hoog beschikbare en veilige webapplicatie te deployen naar een AWS-omgeving, met ondersteuning voor verschillende omgevingen (Test, Acceptance, Production).

---

## 1. Overzicht

### Korte Beschrijving van de Oplossing
Deze oplossing implementeert een multi-tier To-Do applicatie bestaande uit een frontend (Web Layer), een backend (Application Layer) en een relationele database. De gehele infrastructuur is gedefinieerd en wordt beheerd via AWS CloudFormation. De applicatielagen zijn gecontaineriseerd en worden georkestreerd met AWS ECS Fargate, waarbij gebruik wordt gemaakt van Application Load Balancers (ALB's) voor verkeersdistributie. De database is een managed AWS RDS MySQL-instance. De infrastructuur is ontworpen om beveiliging, hoge beschikbaarheid en schaalbaarheid te garanderen, met omgevingsspecifieke configuraties voor kostenoptimalisatie en productiegereedheid.

### Keuze tussen ECS of EKS (met Motivatie)
De keuze is gevallen op **AWS ECS (Elastic Container Service) met Fargate launch type**.
[**Dit is een verplicht en belangrijk onderdeel dat verder moet worden uitgewerkt door de gebruiker.**]
Mogelijke motivatiepunten (uit te breiden door gebruiker):
*   **Eenvoud en Integratie:** ECS is dieper geïntegreerd met de rest van het AWS-ecosysteem, wat de configuratie en het beheer vaak eenvoudiger maakt dan EKS (Kubernetes), vooral voor teams die al bekend zijn met AWS-services.
*   **Minder Operationele Overhead:** Met Fargate is er geen behoefte om EC2-instances voor worker nodes te beheren, wat de operationele overhead aanzienlijk vermindert. AWS beheert de onderliggende infrastructuur.
*   **Schaalbaarheid:** ECS Fargate biedt ingebouwde schaalbaarheid voor taken, die automatisch CPU en geheugen provisioneert op basis van gedefinieerde vereisten.
*   **Kostenmodel:** Het Fargate-model waarbij alleen betaald wordt voor de gebruikte vCPU- en geheugenresources, kan kosteneffectiever zijn voor sommige workloads.
*   **Leercurve:** De leercurve voor ECS is over het algemeen minder steil dan voor EKS, wat de adoptie en het beheer kan versnellen.
*   **Projectvereisten:** Voor dit project voldoet ECS Fargate ruimschoots aan de vereisten voor containerorkestratie zonder de extra complexiteit van Kubernetes te introduceren.

### Architectuur Diagram van de Uiteindelijke Implementatie
[Voeg hier een up-to-date architectuur diagram toe van jouw uiteindelijke AWS implementatie. Dit diagram moet alle componenten bevatten, inclusief je ECS Fargate setup, netwerkcomponenten (VPC, publieke/private subnets, NAT Gateway(s), Internet Gateway, publieke en interne ALB's), RDS database, Secrets Manager en CloudWatch Logs.]
![Architectuur Diagram](/images/Architecture.png) <!-- Pas dit pad aan indien nodig. Dit is een placeholder voor de locatie van je diagram. -->

---

## 2. Deployment Instructies

### Stap-voor-stap Instructies om de Oplossing te Deployen
Om de gehele applicatie-infrastructuur te deployen met CloudFormation, volg je deze stappen:

1.  **Code Kloon:** Kloon de projectrepository naar je lokale machine.
2.  **Docker Images Bouwen:** Bouw de Docker images voor zowel de Application Layer als de Web Layer.
    *   Navigeer naar de `ApplicationLayer` directory en bouw de image: `docker build -t application-layer .`
    *   Navigeer naar de `WebLayer` directory en bouw de image: `docker build -t web-layer .`
3.  **ECR Repositories Aanmaken:** Zorg ervoor dat de ECR repositories voor beide lagen bestaan in je AWS-account in de `us-east-1` regio (of de gewenste regio). Deze moeten overeenkomen met de `ApplicationLayerECRRepositoryUri` en `WebLayerECRRepositoryUri` parameters in `main.yaml`.
4.  **Docker Images Taggen en Pushen:** Tag de lokaal gebouwde Docker images met een unieke `ImageTag` (bijv. een git commit SHA, `v1.0.0`, of een timestamp) en push ze naar de respectievelijke ECR repositories. Het is cruciaal om een unieke `ImageTag` te gebruiken voor elke nieuwe deployment.
    *   Voor Application Layer:
        `docker tag application-layer:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/application-layer-repo:YOUR_IMAGE_TAG`
        `docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/application-layer-repo:YOUR_IMAGE_TAG`
    *   Voor Web Layer:
        `docker tag web-layer:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/web-layer-repo:YOUR_IMAGE_TAG`
        `docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/web-layer-repo:YOUR_IMAGE_TAG`
5.  **CloudFormation Pakketteren:** Gebruik de `aws cloudformation package` commando om je nested stacks te pakketteren en te uploaden naar een S3-bucket.
    *   Zorg voor een bestaande S3 bucket voor het opslaan van de gepakketteerde templates.
    *   `aws cloudformation package --template-file cloudformation/main.yaml --s3-bucket YOUR_CF_PACKAGE_BUCKET --output-template-file packaged-main.yaml`
6.  **CloudFormation Deployen:** Voer de `aws cloudformation deploy` commando uit met de gewenste omgeving en parameters.

### Vereiste Prerequisites
Om de deployment uit te voeren, heb je de volgende tools en configuraties nodig op je lokale machine:
*   **AWS CLI:** Geconfigureerd met de juiste credentials en standaardregio.
*   **Docker:** Voor het bouwen en pushen van container images.
*   **AWS Credentials:** Een AWS IAM gebruiker of rol met voldoende rechten om CloudFormation stacks te creëren, ECR repositories te gebruiken, en alle benodigde AWS-resources (VPC, EC2, RDS, ECS, ALB, Secrets Manager, SSM Parameter Store, IAM rollen) te provisioneren in de doelregio.
*   **Een EC2 Key Pair:** Voor de Production omgeving is een bestaande EC2 Key Pair (bijv. `vockey`) vereist in de deploy-regio voor de Bastion Host.

### Exacte Commando's om te Deployen
Hier zijn de voorbeeld commando's voor het deployen van de applicatie voor elke omgeving. Vervang de placeholders `YOUR_...` met je werkelijke waarden.

```bash
# 1. Pakketteren van de CloudFormation templates (eenmalig, na elke wijziging in templates)
aws cloudformation package \
  --template-file cloudformation/main.yaml \
  --s3-bucket YOUR_CF_PACKAGE_BUCKET \
  --output-template-file packaged-main.yaml

# 2. Deployment voor de TEST omgeving
aws cloudformation deploy \
  --template-file packaged-main.yaml \
  --stack-name MyTodoApp-Test \
  --parameter-overrides \
    Environment=Test \
    ImageTag=YOUR_IMAGE_TAG \ # Gebruik hier de tag van je gebouwde Docker images
    ApplicationLayerECRRepositoryUri=YOUR_APP_LAYER_ECR_URI \
    WebLayerECRRepositoryUri=YOUR_WEB_LAYER_ECR_URI \
    LabRoleArn=YOUR_LAB_ROLE_ARN \
    BastionAllowedCIDR=0.0.0.0/0 \
    KeyName=YOUR_KEY_PAIR_NAME \ # Niet gebruikt in Test, maar vereist als parameter in main.yaml
  --capabilities CAPABILITY_NAMED_IAM

# 3. Deployment voor de ACCEPTANCE omgeving
aws cloudformation deploy \
  --template-file packaged-main.yaml \
  --stack-name MyTodoApp-Acceptance \
  --parameter-overrides \
    Environment=Acceptance \
    ImageTag=YOUR_IMAGE_TAG \ # Gebruik hier de tag van je gebouwde Docker images
    ApplicationLayerECRRepositoryUri=YOUR_APP_LAYER_ECR_URI \
    WebLayerECRRepositoryUri=YOUR_WEB_LAYER_ECR_URI \
    LabRoleArn=YOUR_LAB_ROLE_ARN \
    BastionAllowedCIDR=0.0.0.0/0 \
    KeyName=YOUR_KEY_PAIR_NAME \
  --capabilities CAPABILITY_NAMED_IAM

# 4. Deployment voor de PRODUCTION omgeving
aws cloudformation deploy \
  --template-file packaged-main.yaml \
  --stack-name MyTodoApp-Production \
  --parameter-overrides \
    Environment=Production \
    ImageTag=YOUR_IMAGE_TAG \ # Gebruik hier de tag van je gebouwde Docker images
    ApplicationLayerECRRepositoryUri=YOUR_APP_LAYER_ECR_URI \
    WebLayerECRRepositoryUri=YOUR_WEB_LAYER_ECR_URI \
    LabRoleArn=YOUR_LAB_ROLE_ARN \
    BastionAllowedCIDR=0.0.0.0/0 \
    KeyName=YOUR_KEY_PAIR_NAME \ # Vereist voor Bastion Host
  --capabilities CAPABILITY_NAMED_IAM
```
*(Vervang alle `YOUR_...` placeholders met je specifieke waarden. `ImageTag` zal dezelfde zijn voor beide lagen, zoals afgesproken.)*

---

## 3. Technische Details per Component

### Netwerk Architectuur
De netwerkarchitectuur wordt volledig gedefinieerd in de `network.yaml` CloudFormation nested stack en past zich dynamisch aan op basis van de gedeployde omgeving (`Environment` parameter).

*   **VPC (Virtual Private Cloud):** Er wordt één VPC gecreëerd per omgeving met een specifiek CIDR-blok:
    *   **Test:** `10.0.0.0/16`
    *   **Acceptance:** `10.10.0.0/16`
    *   **Production:** `10.20.0.0/16`
    DNS support (`EnableDnsSupport: true`) en DNS hostnames (`EnableDnsHostnames: true`) zijn ingeschakeld, wat essentieel is voor service discovery en ALB DNS-namen.
*   **Subnets:** De VPC is gesegmenteerd in publieke en private subnets, verdeeld over Availability Zones (AZs) voor hoge beschikbaarheid in hogere omgevingen:
    *   **Publieke Subnets:** Bevatten resources die direct toegankelijk moeten zijn vanaf het internet, zoals de publieke Application Load Balancer voor de Web Layer en NAT Gateways (en de Bastion Host in Production). Taken die in publieke subnets draaien, krijgen een publiek IP-adres (`MapPublicIpOnLaunch: true`).
        *   **Test:** 1 publiek subnet in de eerste beschikbare AZ.
        *   **Acceptance:** 2 publieke subnets in de eerste twee beschikbare AZs.
        *   **Production:** 3 publieke subnets in de eerste drie beschikbare AZs.
    *   **Private Subnets:** Bevatten applicatiecomponenten (ECS services voor de Web- en Application Layer) en de database, die geen directe internettoegang hebben (`AssignPublicIp: DISABLED` voor ECS taken).
        *   **Test:** 1 privé subnet in de eerste beschikbare AZ.
        *   **Acceptance:** 2 privé subnets in de eerste twee beschikbare AZs.
        *   **Production:** 3 privé subnets in de eerste drie beschikbare AZs.
*   **Internet Gateway (IGW):** Gekoppeld aan de VPC om internettoegang mogelijk te maken voor resources in publieke subnets en om inkomend verkeer naar de publieke ALB te routeren.
*   **NAT Gateways:** Geconfigureerd in de publieke subnets. Resources in de private subnets kunnen via een NAT Gateway internettoegang verkrijgen (bijv. voor het ophalen van updates of externe API calls) zonder publiek toegankelijk te zijn. NAT Gateways worden per AZ ingezet om single points of failure te voorkomen.
    *   **Test:** 1 NAT Gateway in AZ1.
    *   **Acceptance:** 2 NAT Gateways in AZ1 en AZ2 voor redundantie.
    *   **Production:** 3 NAT Gateways in AZ1, AZ2 en AZ3 voor maximale redundantie.
*   **Route Tables:**
    *   **Publieke Route Table:** Stuurt al het uitgaande verkeer voor `0.0.0.0/0` (alles) naar de Internet Gateway. Alle publieke subnets zijn hiermee geassocieerd.
    *   **Private Route Tables:** Stuurt al het uitgaande verkeer voor `0.0.0.0/0` naar de respectievelijke NAT Gateways. Elke private subnet heeft een route table associatie die naar de NAT Gateway in dezelfde AZ wijst om asymmetrische routing te voorkomen.

### Container Orchestration Setup
De containerorkestratie wordt beheerd met **AWS ECS (Elastic Container Service)**, specifiek met het **Fargate launch type**, gedefinieerd via de `ecs-cluster.yaml`, `application-service.yaml` en `web-service.yaml` nested stacks.

*   **ECS Cluster:** Een ECS Cluster (`!Sub '${Environment}-ECSCluster'`) wordt gecreëerd per omgeving. Dit cluster dient als een logische groepering voor de ECS services en taken.
*   **Task Definitions:** Er zijn aparte Task Definitions voor de Web Layer (`!Sub '${Environment}-WebTask'`) en Application Layer (`!Sub '${Environment}-ApplicationTask'`).
    *   Deze zijn geconfigureerd met `FARGATE` als `RequiresCompatibilities`, wat betekent dat de onderliggende EC2-instances (worker nodes) volledig beheerd worden door AWS.
    *   Ze gebruiken `awsvpc` network mode, wat elke taak een eigen Elastic Network Interface (ENI) in de VPC geeft.
    *   Task Definitions specificeren ook de `Cpu` (`512` - 0.5 vCPU) en `Memory` (`1024` - 1GB) toewijzing voor de containers, evenals de `ExecutionRoleArn` voor Fargate om logs te pushen en images op te halen.
*   **ECS Services:** Aparte ECS Services (`!Sub '${Environment}-WebService'` en `!Sub '${Environment}-ApplicationService'`) worden gecreëerd om de taken te beheren.
    *   Ze worden geconfigureerd met `FARGATE` als `LaunchType`.
    *   `DeploymentConfiguration` zorgt voor rollende updates met `MaximumPercent: 200` en `MinimumHealthyPercent: 100`, wat betekent dat er altijd minimaal 100% van de gewenste taken online blijven tijdens een deployment.
    *   `DesiredCount` wordt dynamisch ingesteld via `ScalingConfig` mappings.
    *   `NetworkConfiguration` zorgt ervoor dat taken in de private subnets worden geplaatst (`AssignPublicIp: DISABLED`) en gekoppeld zijn aan de juiste Security Groups.

### Container Configuratie
*   **Web Layer Container (`web-layer`):**
    *   **Image:** `!Sub '${WebLayerECRRepositoryUri}:${ImageTag}'`. Gebruikt dezelfde `ImageTag` als de Application Layer.
    *   **Port:** Exposeert poort `8000` voor de Gunicorn Python-webserver.
    *   **Environment Variables:** Ontvangt `INTERNAL_ALB_DNS_NAME` als `!Ref BackendApiUrl` om de Flask-applicatie te laten communiceren met de interne ALB van de Application Layer.
    *   **Health Check:** De Flask-applicatie (`app.py`) bevat een nieuw `/health` endpoint dat `200 OK` teruggeeft voor ALB health checks.
    *   **Resources:** Gereserveerde resources zijn `Cpu: '512'` (0.5 vCPU) en `Memory: '1024'` (1GB).
*   **Application Layer Container (`application-layer`):**
    *   **Image:** `!Sub '${ApplicationLayerECRRepositoryUri}:${ImageTag}'`. Gebruikt dezelfde `ImageTag` als de Web Layer.
    *   **Port:** Exposeert poort `4000` voor de backend-applicatie.
    *   **Environment Variables:** Ontvangt `AWS_REGION`. Essentiële database verbindingsgegevens worden opgehaald via environment variables: `DB_ENDPOINT` (`!Ref DBEndpoint`), `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`.
    *   **Secrets:** `DB_USERNAME` en `DB_PASSWORD` worden veilig opgehaald uit AWS Secrets Manager via `ValueFrom: !Sub "${DBSecretArn}:username::"` en `ValueFrom: !Sub "${DBSecretArn}:password::"`. `DB_NAME` komt uit SSM Parameter Store via `!Sub 'arn:${AWS::Partition}:ssm:${AWS::Region}:${AWS::AccountId}:parameter/${Environment}/TodoAppDB/dbname'`.
    *   **Resources:** Gereserveerde resources zijn `Cpu: '512'` (0.5 vCPU) en `Memory: '1024'` (1GB).

### Database Setup
De database wordt geconfigureerd als een AWS RDS MySQL instance, gedefinieerd in de `database.yaml` nested stack.

*   **Type:** AWS RDS DBInstance met MySQL Engine versie `8.0`.
*   **DB Instance Class:** Dynamisch bepaald via een `Mapping` (`DatabaseConfig`) op basis van de `Environment` parameter:
    *   **Test/Acceptance:** `db.t3.micro`
    *   **Production:** `db.t3.small`
*   **Opslag:** `20 GB` gealloceerde opslag.
*   **Netwerk:** De database wordt in de **private subnets** geplaatst via een `DBSubnetGroup` en is **niet publiek toegankelijk** (`PubliclyAccessible: false`). Toegang wordt strikt gecontroleerd via Security Groups.
*   **Hoge Beschikbaarheid (HA):**
    *   **Test:** `MultiAZ: false` (kostenbesparing, geen redundante stand-by instance).
    *   **Acceptance/Production:** `MultiAZ: true` voor failover functionaliteit tussen Availability Zones, wat zorgt voor een hogere beschikbaarheid van de database.
*   **Beveiliging:**
    *   **Encryptie at rest:** `StorageEncrypted: true` is geactiveerd voor de Production omgeving om data op de opslag media te beschermen.
    *   **Secrets Management:** Database credentials (Master Username en Password) worden veilig beheerd via AWS Secrets Manager (`DBSecret`). Credentials worden dynamisch gegenereerd bij creatie en zijn niet hardcoded in de templates. De applicatie haalt deze credentials op via dynamic references, wat een beveiligde manier is om gevoelige informatie te benaderen.
    *   **Deletion Protection:** `DeletionProtection: true` is geactiveerd voor de Production omgeving om accidentele verwijdering van de database instance te voorkomen.
*   **Parameters:** De database verkrijgt zijn `VpcId`, `PrivateSubnetIds` en `DBSecurityGroupId` van de parent `main.yaml` stack.

### Load Balancing (ALB Configuration)
Er worden twee Application Load Balancers (ALB's) ingezet: één publiek voor de Web Layer en één intern voor de Application Layer, gedefinieerd in de `web-service.yaml` en `application-service.yaml` nested stacks.

*   **Publieke ALB (`WebAlb`):**
    *   **Type:** `internet-facing`, wat betekent dat deze toegankelijk is vanaf het internet.
    *   **Subnets:** Gedeployed in de publieke subnets om verkeer van buitenaf te kunnen ontvangen.
    *   **Security Groups:** Gekoppeld aan `AlbSecurityGroupId`, die HTTP (`TCP/80`) verkeer van overal toestaat.
    *   **Listener:** Luistert op poort `80` (HTTP) en stuurt al het verkeer door naar de `WebAlbTargetGroup`.
    *   **Target Group (`WebAlbTargetGroup`):** Doelpoort `8000` (waar de Web Layer Gunicorn-applicatie luistert). Health Check op `/health` pad, verwacht een `200` HTTP status. `deregistration_delay.timeout_seconds` is ingesteld op 30 seconden voor connection draining.
*   **Interne ALB (`InternalALB` - gedefinieerd in `ApplicationServiceStack`):**
    *   **Type:** `internal`, wat betekent dat deze alleen toegankelijk is vanuit de VPC.
    *   **Subnets:** Gedeployed in de private subnets voor de Application Layer.
    *   **Security Groups:** Gekoppeld aan `InternalAlbSGId`, die verkeer toestaat vanuit de `WebServiceSecurityGroup`.
    *   **Listener:** Luistert op poort `80` (HTTP) en stuurt al het verkeer door naar de `InternalTargetGroup`.
    *   **Target Group (`InternalTargetGroup`):** Doelpoort `4000` (waar de Application Layer luistert). Health Check op `/health` pad, verwacht een `200` HTTP status. `deregistration_delay.timeout_seconds` is ingesteld op 30 seconden.

### Security Configuratie
De beveiligingsconfiguratie wordt beheerd via de `security.yaml` nested stack, die Security Groups en een optionele Bastion Host configureert. Het principe van least privilege wordt toegepast door het verkeer tussen componenten strikt te controleren.

*   **Security Groups:** Gedetailleerde Security Groups controleren het verkeer:
    *   **BastionSecurityGroup:** Alleen gecreëerd voor de Production omgeving. Staat SSH verkeer (`TCP/22`) toe vanaf een configureerbaar CIDR-blok (`BastionAllowedCIDR`).
    *   **AlbSecurityGroup:** Staat HTTP (`TCP/80`) verkeer van overal (`0.0.0.0/0`) toe naar de publieke `WebAlb`.
    *   **WebServiceSecurityGroup:** Staat verkeer toe van de `AlbSecurityGroup` (poort 8000) naar de Web Layer ECS taken. Taken worden in private subnets geplaatst met `AssignPublicIp: DISABLED`.
    *   **InternalAlbSG:** Staat verkeer toe van de `WebServiceSecurityGroup` (poort 80) naar de interne `InternalALB` die voor de Application Layer staat.
    *   **ApplicationServiceSG:** Staat verkeer toe van de `InternalAlbSG` (poort 4000) naar de Application Layer ECS taken. Ook vanuit de `BastionSecurityGroup` (poort 4000) voor beheertoegang in de Production omgeving.
    *   **DBSecurityGroup:** Staat verkeer toe van de `ApplicationServiceSG` (poort 3306 - MySQL) naar de RDS database. Ook vanuit de `BastionSecurityGroup` (poort 3306) voor beheertoegang in de Production omgeving.
*   **Bastion Host:** Een EC2 instance die alleen in de Production omgeving wordt gecreëerd (`t2.micro`). Het biedt een beveiligde springplank voor beheertoegang tot private resources. SSH toegang is mogelijk via een gespecificeerde `KeyName` (`vockey` in de deploy commando's) vanaf een toegestaan CIDR-blok (`BastionAllowedCIDR`).
*   **IAM Rollen:** De `LabRoleArn` parameter (vermeld als `arn:aws:iam::992382752163:role/LabRole` in de deployment commando's) wordt doorgegeven aan child stacks en wordt gebruikt voor:
    *   **ECS Task Execution Roles:** Geeft ECS permissies om logstreams te creëren en Docker images op te halen.
    *   **ECS Task Roles:** Geeft de taken de permissies die ze nodig hebben om AWS API-aanroepen te doen (bijv. Secrets Manager, SSM Parameter Store).
    *   **Application Auto Scaling Roles:** Voor het aansturen van auto scaling policies.
    [Vul hier eventueel meer specifieke IAM details in als je aparte rollen hebt voor Execution en Task, of andere specifieke permissies.]

### Monitoring Setup (Datadog Integratie)
[Beschrijf hoe Datadog monitoring is geïmplementeerd.
*   Hoe zijn Datadog agents geïnstalleerd (sidecar/DaemonSet)?
*   Hoe is de installatie geautomatiseerd via CloudFormation?
*   Hoe worden API keys veilig opgeslagen?
**Deze details zijn nog niet zichtbaar in de CloudFormation templates die zijn bekeken en moeten nog geïmplementeerd/gedocumenteerd worden.** Dit is een 'extra' punt dat kan bijdragen aan de score.]

---

## 4. Per Omgeving

### Verschillen tussen Test, Acceptance en Production
De implementatie maakt uitgebreid gebruik van CloudFormation `Conditions` en `Mappings` om de configuratie dynamisch aan te passen per omgeving (`Environment` parameter: `Test`, `Acceptance`, `Production`). De `ImageTag` parameter is voor alle omgevingen van toepassing, wat betekent dat dezelfde versie van de applicatiecode wordt gebruikt, ongeacht de omgeving.

*   **Test Omgeving (Doel: Functioneel testen met minimale kosten):**
    *   **Netwerk:** Eenvoudig netwerk met 1 publiek en 1 privé subnet in één AZ. 1 NAT Gateway.
    *   **Database:** `db.t3.micro`, Single-AZ (geen HA), geen encryptie, geen deletion protection.
    *   **HA/Scaling:** Geen hoge beschikbaarheid of autoscaling vereist (minimale resources). `DesiredCount: 1` voor Web- en Application Services.
    *   **Beveiliging:** Geen Bastion Host.
*   **Acceptance Omgeving (Doel: Volledige acceptance testing met productie-gelijke setup):**
    *   **Netwerk:** Hogere beschikbaarheid met 2 publieke en 2 privé subnets, elk in een aparte AZ. 2 NAT Gateways voor redundantie.
    *   **Database:** `db.t3.micro`, Multi-AZ (HA geactiveerd), geen encryptie, geen deletion protection.
    *   **HA/Scaling:** Hoge beschikbaarheid is geactiveerd voor de database. ECS Service Auto Scaling is geconfigureerd voor de Application en Web Layers op basis van gemiddelde CPU-utilisatie (TargetValue: 70.0%). `MinCapacity: 2`, `MaxCapacity: 4`, `DesiredCount: 2` voor Web- en Application Services, verdeeld over 2 AZs.
    *   **Beveiliging:** Geen Bastion Host.
*   **Production Omgeving (Doel: Productie-klare omgeving met optimale performance en beveiliging):**
    *   **Netwerk:** Maximale beschikbaarheid met 3 publieke en 3 privé subnets, elk in een aparte AZ. 3 NAT Gateways voor maximale redundantie.
    *   **Database:** `db.t3.small` (hogere performance), Multi-AZ (HA geactiveerd), **encryptie at rest geactiveerd**, **deletion protection geactiveerd**.
    *   **HA/Scaling:** Geoptimaliseerde hoge beschikbaarheid voor de database. ECS Service Auto Scaling is geconfigureerd voor de Application en Web Layers op basis van gemiddelde CPU-utilisatie (TargetValue: 70.0%). `MinCapacity: 2`, `MaxCapacity: 6`, `DesiredCount: 2` voor Web- en Application Services, verdeeld over 3 AZs.
    *   **Beveiliging:** Inclusief een **Bastion Host** voor beveiligd beheertoegang. Encryptie at rest voor de database en secrets management voor gevoelige data.

### Hoe Parameter Switching Werkt
De `Environment` parameter, die wordt doorgegeven aan het hoofd CloudFormation template (`main.yaml`), is de centrale schakel voor parameter switching.
*   In `main.yaml` en de nested stacks (`network.yaml`, `security.yaml`, `database.yaml`, `application-service.yaml`, `web-service.yaml`) wordt deze parameter gebruikt in `Conditions` (bijv. `IsProduction: !Equals [!Ref Environment, Production]`, `IsAcceptanceOrProduction: !Or [!Condition IsAcceptance, !Condition IsProduction]`).
*   Deze `Conditions` bepalen of bepaalde resources worden gecreëerd (bijv. extra subnets, NAT Gateways, Bastion Host, Multi-AZ database) of welke configuratiewaarden worden toegepast (bijv. `DBInstanceClass`, `StorageEncrypted`, `DeletionProtection`) via `!If` statements.
*   Ook `Mappings` (bijv. `SubnetConfig` in `network.yaml`, `DatabaseConfig` in `database.yaml`, `ScalingConfig` in `application-service.yaml` en `web-service.yaml`) worden gebruikt om omgevingsspecifieke waarden (zoals CIDR-blokken, DB instance types, of gewenste aantallen taken voor scaling) op te halen op basis van de `Environment` parameter.

### Container Scaling Configuratie per Omgeving
*   **Application Layer:** Application Auto Scaling is geconfigureerd voor de ECS Service (`ApplicationService`) voor Acceptance en Production omgevingen. De `ScalableTarget` is ingesteld voor `ecs:service:DesiredCount`. De scaling policy is van het type `TargetTrackingScaling` en richt zich op gemiddelde CPU-utilisatie (`ECSServiceAverageCPUUtilization`) met een `TargetValue` van 70.0%.
*   De `MinCapacity` en `MaxCapacity` worden dynamisch bepaald door de `ScalingConfig` mapping in `application-service.yaml` op basis van de `Environment`.
    *   **Test:** Geen autoscaling geactiveerd (`Min: 1`, `Max: 2`, `Desired: 1`).
    *   **Acceptance:** `MinCapacity: 2`, `MaxCapacity: 4`, `DesiredCount: 2`.
    *   **Production:** `MinCapacity: 2`, `MaxCapacity: 6`, `DesiredCount: 2`.
*   **Web Layer:** Application Auto Scaling is geconfigureerd voor de ECS Service (`WebService`) voor Acceptance en Production omgevingen. De `ScalableTarget` is ingesteld voor `ecs:service:DesiredCount`. De scaling policy is van het type `TargetTrackingScaling` en richt zich op gemiddelde CPU-utilisatie (`ECSServiceAverageCPUUtilization`) met een `TargetValue` van 70.0%.
*   De `MinCapacity` en `MaxCapacity` worden dynamisch bepaald door de `ScalingConfig` mapping in `web-service.yaml` op basis van de `Environment`.
    *   **Test:** Geen autoscaling geactiveerd (`Min: 1`, `Max: 2`, `Desired: 1`).
    *   **Acceptance:** `MinCapacity: 2`, `MaxCapacity: 4`, `DesiredCount: 2`.
    *   **Production:** `MinCapacity: 2`, `MaxCapacity: 6`, `DesiredCount: 2`.

### Screenshots van Gedeployde Omgevingen
[**Deze sectie moet door de gebruiker worden aangevuld met actuele screenshots van de deployed omgevingen en Datadog-dashboards.**]
*   **Screenshot 1: Werkende Applicatie (URL)**
*   **Screenshot 2: AWS Console - ECS Cluster (overzicht)**
*   **Screenshot 3: AWS Console - ECS Services (Web & App Layer)**
*   **Screenshot 4: AWS Console - RDS Instance**
*   **Screenshot 5: AWS Console - Load Balancers (Web & Internal ALB)**
*   **Screenshot 6: Datadog Dashboard (indien geïmplementeerd)**
[Voeg indien nodig meer relevante screenshots toe.]

---

## 5. Gemaakte Keuzes

### Waarom ECS of EKS Gekozen (Belangrijkste Onderdeel)
De keuze is gevallen op **AWS ECS (Elastic Container Service) met Fargate launch type**.
[**Dit is het belangrijkste onderdeel van de motivatie en moet door de gebruiker worden aangevuld.**]
Mogelijke motivatiepunten (uit te breiden door gebruiker):
*   **Eenvoud en Integratie:** ECS is dieper geïntegreerd met de rest van het AWS-ecosysteem, wat de configuratie en het beheer vaak eenvoudiger maakt dan EKS (Kubernetes), vooral voor teams die al bekend zijn met AWS-services.
*   **Minder Operationele Overhead:** Met Fargate is er geen behoefte om EC2-instances voor worker nodes te beheren, wat de operationele overhead aanzienlijk vermindert. AWS beheert de onderliggende infrastructuur.
*   **Schaalbaarheid:** ECS Fargate biedt ingebouwde schaalbaarheid voor taken, die automatisch CPU en geheugen provisioneert op basis van gedefinieerde vereisten.
*   **Kostenmodel:** Het Fargate-model waarbij alleen betaald wordt voor de gebruikte vCPU- en geheugenresources, kan kosteneffectiever zijn voor sommige workloads.
*   **Leercurve:** De leercurve voor ECS is over het algemeen minder steil dan voor EKS, wat de adoptie en het beheer kan versnellen.
*   **Projectvereisten:** Voor dit project voldoet ECS Fargate ruimschoots aan de vereisten voor containerorkestratie zonder de extra complexiteit van Kubernetes te introduceren.

### Voor ECS: Waarom Fargate of EC2 Launch Type
De keuze is gevallen op **AWS Fargate** als launch type voor de ECS taken.
[**Motiveer specifiek waarom je Fargate hebt gebruikt, bespreek de voor- en nadelen die van invloed waren op jouw beslissing. Dit moet door de gebruiker worden aangevuld.**]
Mogelijke motivatiepunten (uit te breiden door gebruiker):
*   **Serverloos:** Elimineert de noodzaak om EC2-instances te selecteren, te patchen, te schalen en te beheren. Fargate beheert de onderliggende servers volledig.
*   **Kostenoptimalisatie:** Betaal alleen voor de gealloceerde resources per taak, niet voor idle EC2-instances.
*   **Beveiliging:** Verbeterde isolatie doordat elke taak in zijn eigen virtuele machine draait.
*   **Snellere Deployment:** Minder infrastructuur om te provisioneren en te beheren, kan leiden tot snellere deployment cycli.

### Afwegingen tussen Alternatieven
[**Bespreken hier eventuele andere architectuurkeuzes of technologieën die je hebt overwogen en waarom je uiteindelijk je huidige implementatie hebt gekozen. Denk aan netwerkontwerp, databasekeuzes, load balancing opties, etc. Dit moet door de gebruiker worden aangevuld.**]

### Optimalisaties die Zijn Toegepast
[**Beschrijf eventuele optimalisaties die je hebt doorgevoerd met betrekking tot kosten, prestaties, beveiliging of beheer. Dit kunnen specifieke CloudFormation-instellingen, resource types of service-configuraties zijn. Dit moet door de gebruiker worden aangevuld.**]
Mogelijke optimalisaties (uit te breiden door gebruiker):
*   **Kosten:**
    *   Gebruik van `db.t3.micro` voor Test/Acceptance en `t2.micro` voor Bastion Host.
    *   Conditional deployment van NAT Gateways per omgeving.
    *   Conditional `MultiAZ` voor RDS.
*   **Prestaties:**
    *   Gebruik van interne ALB voor backend communicatie.
    *   Application Auto Scaling voor Web- en Application Layers.
    *   `db.t3.small` voor Production RDS.
*   **Beveiliging:**
    *   Netwerksegmentatie (publieke/private subnets).
    *   Strikte Security Group regels (least privilege).
    *   Secrets Manager voor DB-credentials.
    *   Conditional `StorageEncrypted` en `DeletionProtection` voor RDS in Production.
    *   Bastion Host voor beheertoegang in Production.
    *   `AssignPublicIp: DISABLED` voor ECS taken in private subnets.

---

Dit document is bedoeld als leidraad. **De gemarkeerde secties `[**Dit moet door de gebruiker worden aangevuld.**]` en `[Voeg hier ... toe]` moeten door jou worden ingevuld met de specifieke details, motivaties en screenshots van jouw project om aan alle vereisten te voldoen.**