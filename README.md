
  PREREQUIREMENTS:

  Execute the following from 'root' user:

  - install Docker engine>=v20.10.21

  - install Docker compose>=v2.12.2 

  - download the package into /home from:

    curl -u vritrovato83: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 -LJO "https://github.com/SercoSPA/dhs-suite-easy-deploy/archive/refs/tags/1.0.0.zip" 

  - unzip the package and go inside it:

    unzip /home/dhs-suite-easy-deploy-1.0.0.zip
  
    cd /home/dhs-suite-easy-deploy-1.0.0

  HOW TO LAUNCH THE INSTALLATION: 

  The script has 3 parameters, ip machine, name of repository (the repository downloaded is the 1.0.0 version), list of softwares installable. If it wants to install ALL softwares please execute this command:  

    ./2-click-installer.sh "<ip_machine>" "dhs-suite-easy-deploy" "copsi,dafne,tf,sf,iam"

  The version of softwares installed are:

  - COPSI: copsi 1.0.1

  - DAFNE: dafne frontend 3.0.2, dafne backend 3.0.1, postgres 12.5 

  - TF: esa_tf_restapi and esa_tf_worker latest version, scheduler dask 2021.8.1-py3.9, nginx 1.21.6

  - SF: virtuoso-opensource-7 latest version, sf-datareceiver v2.0, semantic_framework v2.3

  - KEYCLOAK: custom version ciam-swarm-keycloak:1.0

  If it wants to install a subset of softwares, for instance copsi and dafne, execute this command:

    ./2-click-installer.sh "<ip_machine>" "dhs-suite-easy-deploy" "copsi,dafne"

  HOW TO REMOVE ALL SERVICES/ALL VOLUMES/NETWORK/SWARM/USER: 

  - docker stack rm copsi-service dafne-service tf-service sf-service iam-service 
  
  - docker volume rm copsi-config copsi-html dafne-be-config dafne-be-logs dafne-db dafne-fe-config dafne-fe-html dr-api_logs kb_db pg-data pg-scripts sf-api_logs sf-config tf-config tf-data tf-logs tf-plugins tf-traces tf-output
  
  - docker network rm collnetwork
  
  - docker swarm leave --force
  
  - userdel -r colluser

  WHERE TO CONFIG THE SOFTWARES:

  - COPSI:

    /var/lib/docker/volumes/copsi-config/_data/config.json

  - DAFNE:

    /var/lib/docker/volumes/dafne-be-config/_data/config.json
 
    /var/lib/docker/volumes/dafne-be-config/_data/db_credentials.env
 
    /var/lib/docker/volumes/dafne-fe-config/_data/config.json

  - SF:

    /var/lib/docker/volumes/sf-config/_data/configuration.json
 
    /var/lib/docker/volumes/sf-config/_data/keycloak_configuration.json

  - TF:

    /var/lib/docker/volumes/tf-config/_data/esa_tf.config
 
    /var/lib/docker/volumes/tf-config/_data/hubs_credentials.yaml
 
    /var/lib/docker/volumes/tf-config/_data/traceability_config.yaml
