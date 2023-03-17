
  HOW TO LAUNCH THE INSTALLATION: 

  ./script.sh "10.144.1.99" "dhs-suite-easy-deploy" "https://vritrovato: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@github.com/SercoSPA/dhs-suite-easy-deploy.git" "copsi,dafne,tf,sf,iam"

  HOW TO REMOVE SERVICES: 

  docker stack rm copsi-service dafne-service tf-service sf-service iam-service
  docker volume rm copsi-config copsi-html dafne-be-config dafne-be-logs dafne-db dafne-fe-config dafne-fe-html dr-api_logs kb_db pg-data pg-scripts sf-api_logs sf_config tf-config tf-data tf-logs tf-plugins tf-traces tf-output
  docker network rm collnetwork
  docker swarm leave --force
  userdel -r colluser

  GENERAL COMMANDS

    from root on centos

   -useradd colluser

   -visudo --> add row --> %wheel ALL=(ALL) NOPASSWD: ALL

   -usermod -aG wheel colluser

   -usermod -aG docker colluser

   -docker swarm init --advertise-addr "ip_machine"

   -docker network create --driver=overlay --attachable -o com.docker.network.bridge.enable_icc=true collnetwork

  COPSI

  Pre-requirements:

   -Centos7 64 bit

   -RAM 8 GB

   -CPU 4 cores

   -Storage 100 GB

   -Docker engine>=v20.03.5

   -Docker compose>=v1.24.1

   -User for copsi must be in the docker group

  Commands:
   
    from colluser on centos

   -sudo su - colluser
   
   -sudo git pull "package"
   
   -sudo cd "package"
   
   -sudo docker volume create copsi-config

   -sudo cp data/copsi/config/config.json /var/lib/docker/volumes/copsi-config/_data/

   -sudo docker volume create copsi-html
  
   -sudo cp data/copsi/html/index.html /var/lib/docker/volumes/copsi-html/_data/
   
   -sudo docker stack deploy --compose-file docker-compose.yml copsi-service

  DAFNE

  Pre-requirements:

   -memory > 8GB

   -CPU 4 cores

   -Centos7 64 bit

   -Storage 150 GB
   
   -Docker engine (>=19.03.5) 
   
   -dockercompose (>=1.24.1) 
   
   -user for dafne must be in the docker group

  Commands:

    from colluser on centos

   -sudo su - colluser
   
   -sudo git pull "package"
   
   -sudo cd "package"
   
   -sudo docker volume create dafne-fe-config

   -sudo docker volume create dafne-fe-html

   -sudo cp data/dafne/front-end/config/* /var/lib/docker/volumes/dafne-fe-config/_data/

   -sudo cp data/dafne/front-end/html/* /var/lib/docker/volumes/dafne-fe-html/_data/

   -sudo docker volume create dafne-be-config
  
   -sudo cp data/dafne/back-end/config/* /var/lib/docker/volumes/dafne-be-config/_data/

   -sudo docker volume create dafne-db

   -sudo docker volume create dafne-be-logs 
   
   -sudo docker stack deploy --compose-file docker-compose.yml dafne-service

  TF

  Pre-requirements:

   -memory > 6Gb per core 

   -disk image size > 50Gb 
   
   -Docker engine (>=20.10) 
   
   -dockercompose (>=2.0) 
   
   -make (>=3.81) 
   
   -curl (>=7.75) 
   
   -unzip (>=6.0) 
   
   -tar (>=2.8)

  Commands:

   from colluser on centos

   -sudo su - colluser
   
   -sudo git pull "package"
   
   -sudo cd "package"
   
   -sudo docker volume create tf-config
   
   -sudo cp config/* /var/lib/docker/volumes/tf-config/_data/
   
   -sudo docker volume create tf-data
   
   -sudo mkdir /var/lib/docker/volumes/tf-data/_data/land-cover
   
   -sudo docker volume create tf-plugins
   
   -sudo docker volume create tf-traces
   
   -sudo docker volume create tf-logs
   
   -sudo docker volume create tf-output
   
   -sudo docker stack deploy --compose-file docker-compose.yml tf-service

  Variables to be set with desired values in docker-compose.yml file:

   -ROOT_PATH 
   
   -OUTPUT_OWNER_ID
   
   -OUTPUT_GROUP_OWNER_ID
   
   -TF_DEBUG
   
   -APPLICATION_HOSTNAME 
   
   -APPLICATION_PROTO 
   
   -OIDC_ACTIVE 
   
   -OIDC_ROOT_URL 
   
   -REALM_NAME 
   
   -CLIENT_ID 
   
   -CLIENT_SECRET 
   
   -KEYCLOAK_HOST_HEADER 
   
   -GUARD_ROLE
 
  KEYCLOAK  

  Commands:

  -sudo su - colluser

  -sudo docker volume create pg-scripts

  -sudo docker volume create pg-data

  -sudo cp init-user-db.sh /var/lib/docker/volumes/pg-scripts/_data/

  -sudo docker login -u onda.ops.team -p w]Ts+T72 https://docker-registry.onda-dias.eu

  -sudo docker build -t ciam-swarm-keycloak:1.0 .

  -sudo docker stack deploy --compose-file docker-compose.yml iam-service

  SF

  Pre-requirements:

   -Docker engine >=v19.03.08

   -Docker compose >=v1.25.5

   -8 CPU, 16 GB RAM, 50GB Disk

   -User for semantic must be in the docker group

  Commands:

   from colluser on centos

   -sudo su - colluser

   -sudo git pull "package"
   
   -sudo cd "package"
   
   -sudo docker volume create sf_config
   
   -sudo docker volume create kb_db
   
   -sudo docker volume create dr-api_logs
   
   -sudo docker volume create sf-api_logs

   -sudo cp config/* /var/lib/docker/volumes/sf_config/_data/

   -sudo docker stack deploy --compose-file docker-compose.yml sf-service
