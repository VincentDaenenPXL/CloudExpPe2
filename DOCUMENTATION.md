# Documentatie: To-Do Applicatie op AWS

Dit document beschrijft de architectuur, de technische keuzes en de deployment-procedure voor de To-Do webapplicatie op AWS.

## 1. Overzicht en Keuze voor ECS Fargate

Voor de container-orchestratie is gekozen voor **AWS Elastic Container Service (ECS) met het Fargate launch type**. Dit is een strategische keuze die de voorkeur krijgt boven AWS Elastic Kubernetes Service (EKS) om de volgende redenen:

*   **Eenvoud en Snelheid:** ECS is aanzienlijk eenvoudiger en sneller op te zetten dan een volledig Kubernetes-cluster (EKS). Dit vermindert de management-overhead en versnelt de development-cyclus, wat cruciaal is binnen de context van dit project.
*   **Serverless:** Fargate is een serverless compute engine voor containers. Het neemt het volledige beheer van de onderliggende serverinfrastructuur uit handen. Dit sluit perfect aan bij de vereiste om geen EC2-instances direct te beheren en stelt ons in staat ons volledig te focussen op de applicatie.
*   **Naadloze AWS-integratie:** Als een native AWS-dienst integreert ECS perfect met andere services zoals IAM, VPC, Application Load Balancers en CloudWatch, wat de configuratie via CloudFormation vereenvoudigt.

## 2. Architectuur

De infrastructuur is volledig gedefinieerd in CloudFormation en is opgedeeld in modulaire stacks.

*   **`ecr.yaml`**: Creëert de ECR repositories voor de Docker-images. Deze stack wordt **eenmalig en apart** gedeployed als setup.
*   **`main.yaml`**: De root-stack die de applicatie-infrastructuur aanstuurt. Het accepteert nu parameters voor de ECR Repository URIs.
*   **`network.yaml`**: Geneste stack die de VPC, subnets, NAT Gateways en route tables creëert.
*   **`ecs-cluster.yaml`**: Geneste stack die het lege ECS-cluster opzet.
*   **`application-service.yaml`**: Geneste stack die de backend-applicatie deployt, inclusief een interne ALB, ECS Service en auto-scaling.
*   **`web-service.yaml`**: Geneste stack die de frontend-applicatie deployt, inclusief een publieke ALB, ECS Service en auto-scaling.

De web- en applicatie-taken draaien in **private subnets** voor maximale beveiliging. Alleen de load balancers zijn toegankelijk van buitenaf (voor de web-laag) of vanuit de VPC (voor de applicatie-laag).

## 3. Deployment Instructies

Volg deze stappen om de applicatie uit te rollen. De deployment is opgesplitst om het "kip-of-ei"-probleem op te lossen: de ECR-repositories moeten bestaan voordat de pipeline er images naartoe kan pushen.

### Stap 1: Eenmalige Setup - ECR Repositories Aanmaken

Dit commando hoef je maar één keer uit te voeren voor je AWS-account. Het zet een permanente stack op die de ECR-repositories beheert.

1.  Voer het `deploy` commando uit voor de `ecr.yaml` template:
    ```bash
    aws cloudformation deploy --template-file cloudformation/ecr.yaml --stack-name todo-app-repositories
    ```
2.  Navigeer in de AWS Console naar CloudFormation en selecteer de `todo-app-repositories` stack. Ga naar het **Outputs** tabblad en **kopieer de URIs** van beide repositories. Je hebt deze nodig in Stap 4.

### Stap 2: GitHub Secrets Voorbereiden

Ga in je GitHub repository naar `Settings > Secrets and variables > Actions` en voeg je AWS-credentials toe:
*   `AWS_ACCESS_KEY_ID`
*   `AWS_SECRET_ACCESS_KEY`
*   `AWS_REGION`
*   `AWS_SESSION_TOKEN` (indien nodig voor je credentials)

### Stap 3: Bouw en Push de Docker Images

1.  Commit en push alle wijzigingen naar de `main` branch.
    ```bash
    git add .
    git commit -m "feat: Finalize CloudFormation and application setup"
    git push origin main
    ```
2.  Ga naar het **Actions** tabblad in je GitHub repository en wacht tot de `Build and Push` workflow succesvol is afgerond.
3.  **Noteer de commit SHA** van je laatste commit (bv. `754871c...`). Dit wordt je `ImageTag`.

### Stap 4: Finale Applicatie-Deployment

Nu de repositories bestaan én gevuld zijn met de juiste images, kun je de applicatie-infrastructuur deployen.

1.  **Package de templates:** Omdat `main.yaml` geneste stacks gebruikt, moet je eerst het `package` commando uitvoeren.
    ```bash
    aws cloudformation package --template-file cloudformation/main.yaml --s3-bucket <JOUW_S3_BUCKET_NAAM> --output-template-file packaged-main.yaml
    ```
    *Vervang `<JOUW_S3_BUCKET_NAAM>` door de naam van een S3-bucket waar je templates kunt opslaan.*

2.  **Deploy de applicatie:** Voer het `deploy` commando uit op het nieuwe `packaged-main.yaml` bestand en geef de ECR URIs mee die je in Stap 1 hebt gekopieerd.

    ```bash
    # VERVANG de placeholders <> met jouw waarden
    aws cloudformation deploy --template-file packaged-main.yaml --stack-name MyTodoApp-<Environment> --parameter-overrides Environment=<Environment> ImageTag=<jouw-git-commit-sha>     ApplicationLayerECRRepositoryUri=<URI_VAN_JE_APP_REPO> WebLayerECRRepositoryUri=<URI_VAN_JE_WEB_REPO> --capabilities CAPABILITY_IAM
    ```
    *   **`<Environment>`**: `Test`, `Acceptance`, of `Production`.
    *   **`<jouw-git-commit-sha>`**: De SHA van de commit uit Stap 3.
    *   **`<URI_VAN_JE_..._REPO>`**: De URIs uit de Outputs van de `todo-app-repositories` stack.

Na een succesvolle deployment vind je onder de **Outputs** van de `MyTodoApp-<Environment>` stack de `WebAppURL`.

## 4. Validatie en Testen

Na een succesvolle deployment kun je de volgende tests uitvoeren om de functionaliteit te valideren.

### Test 1: Werking van de Applicatie

1.  Navigeer in je browser naar de `WebAppURL` uit de CloudFormation-outputs.
2.  **Verwacht resultaat:** De To-Do applicatie laadt en toont (eventueel lege) een lijst met taken. Dit bevestigt dat de frontend (WebLayer) kan communiceren met de backend (ApplicationLayer).

### Test 2: High Availability (voor Acceptance/Production)

Deze test simuleert het falen van een container om te bewijzen dat de applicatie beschikbaar blijft.

1.  Ga naar de **AWS ECS Console**.
2.  Navigeer naar je cluster (bv. `Acceptance-ECSCluster`).
3.  Klik op een van de services, bijvoorbeeld `Acceptance-WebService`.
4.  Ga naar het tabblad **Tasks**. Je zou hier 2 actieve taken moeten zien.
5.  Selecteer één van de taken en klik op **Stop**.
6.  **Verwacht resultaat:**
    *   Terwijl de taak stopt, blijf je de `WebAppURL` in je browser vernieuwen. De applicatie moet bereikbaar blijven, omdat de load balancer het verkeer automatisch naar de overgebleven gezonde taak stuurt.
    *   Na enkele ogenblikken zal ECS automatisch een nieuwe taak opstarten om de gestopte taak te vervangen, waardoor het totaal weer op het gewenste aantal van 2 komt.

### Test 3: Auto-Scaling (voor Acceptance/Production)

Het testen van auto-scaling vereist het genereren van een aanzienlijke load. Je kunt de configuratie echter wel valideren.

1.  Ga in de **AWS ECS Console** naar je service (bv. `Acceptance-WebService`).
2.  Klik op het tabblad **Tasks**. Aan de rechterkant zie je een sectie **Auto Scaling**.
3.  **Validatie:**
    *   Hier zie je de geconfigureerde `TargetTrackingScaling` policy. Het toont aan dat de service is ingesteld om te schalen wanneer de gemiddelde CPU boven de 70% komt.
    *   Je kunt de `Min capacity` (minimum aantal taken) en `Max capacity` (maximum aantal taken) controleren.
    *   Tijdens de presentatie kun je naar deze configuratie verwijzen als bewijs dat auto-scaling is ingesteld volgens de vereisten.

