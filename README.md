
  PREREQUIREMENTS (root user):

  - install Docker engine=v20.10.21

  - install Docker compose=v2.12.2 

  - download the package from:

    curl -u vritrovato83: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 -LJO "https://github.com/SercoSPA/dhs-suite-easy-deploy/archive/refs/tags/1.0.0.zip" 

  - unzip the package and go inside it:

    unzip 1.0.0.zip -d dhs-suite-easy-deploy
  
    cd dhs-suite-easy-deploy

  HOW TO LAUNCH THE INSTALLATION: 

  ./script.sh "<ip_machine>" "dhs-suite-easy-deploy" "copsi,dafne,tf,sf,iam"

  HOW TO REMOVE SERVICES/VOLUMES/NETWORK/SWARM/USER: 

  - docker stack rm copsi-service dafne-service tf-service sf-service iam-service
  
  - docker volume rm copsi-config copsi-html dafne-be-config dafne-be-logs dafne-db dafne-fe-config dafne-fe-html dr-api_logs kb_db pg-data pg-scripts sf-api_logs sf_config tf-config tf-data tf-logs tf-plugins tf-traces tf-output
  
  - docker network rm collnetwork
  
  - docker swarm leave --force
  
  - userdel -r colluser

