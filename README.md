<p align="center">
  <img src="./LogoDHS.png" alt="DHS suite easy deploy" width="214" />
</p>

# DHS Suite Easy Deploy

The DHS suite Easy Deploy is a tool allowing the installation of Collaborative Softwares in Docker Swarm environment, in particular if the machine where the suite will be installed is not in a swarm it will be added. The Docker swarm created will be a single node swarm and it is important to have on the machine these TCP/UDP ports opened 2376/2377/7946/4789.

## Prerequirements

The softwares needed to allow the installation are:

- Docker engine>=v20.10.21

- Docker compose>=v2.12.2

- Java-17-openjdk

- Solr>=8.0

- Postgres>=10.12

- Kafka>=3.3.1

- Zookeeper=3.8

Rememeber that the minimum resources needed to install correctly the entire DHS suite are:

- CPU = 16cores + Ycores for TF

- RAM = 32GB + 6GB x Ycore for TF

- DISK = 350GB

## Download the package to be installed

The package having the installation content is downloadable by:

    curl -u vritrovato83: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 -LJO "https://github.com/SercoSPA/dhs-suite-easy-deploy/archive/refs/tags/1.0.0.zip"

and this package must be downloaded under /home folder by 'root' user.

After the download it is needed to unzip the package and go inside it where is the installer script:

    unzip /home/dhs-suite-easy-deploy-1.0.0.zip

    cd /home/dhs-suite-easy-deploy-1.0.0

The version of the package for this installation is 1.0.0.

## Usage

### Softwares version installed

The softwares that can be installed with installer script are:

- COPSI: copsi 1.0.1

- DAFNE: dafne frontend 3.0.2, dafne backend 3.0.1, postgres 12.5 (release version: 3.0.2)

- TF: esa_tf_restapi and esa_tf_worker latest version, scheduler dask 2021.8.1-py3.9, nginx 1.21.6 (release version: 1.3.0-osf)

- SF: virtuoso-opensource-7 latest version, sf-datareceiver v2.0, semantic_framework v2.3 (release version: 2.3)

- KEYCLOAK: custom version ciam-swarm-keycloak 1.0

- GSS: gss-admin/catalogue/ingest 1.2.0

### How to launch the installation

The installer script has 2 parameters, ip machine and list of softwares installable. If it wants to install ALL softwares the command to be executed from 'root' user is (only for gss softwares before the launching, it is needed to set the IP adress of the machine in ALL config files and it is needed to install the COTS softwares, refer to section "Softwares configuration"):

    ./2-click-installer.sh "<ip_machine>" "copsi,dafne,tf,sf,iam,gss"

every commands in the script above is executed as 'colluser' user, pre-created before the execution of installation commands.

If it wants to install a subset of softwares, for instance copsi and dafne, execute this command from 'root' user:

    ./2-click-installer.sh "<ip_machine>" "copsi,dafne"

In order to configure the DHS suite as it wants it is needed to refer to section "Softwares configuration". In order to restart the services, refer to section "How to restart services".

This installation will create these docker volumes:

COPSI:

- copsi-config
- copsi-html

DAFNE:

- dafne-be-config
- dafne-be-logs
- dafne-db
- dafne-fe-config
- dafne-fe-html

KEYCLOAK:

- pg-data
- pg-scripts

SF:

- dr-api_logs
- kb_db
- sf-api_logs
- sf-config

TF:

- tf-config
- tf-data
- tf-logs
- tf-output
- tf-plugins
- tf-traces

### How to remove 

#### All docker services

    docker stack rm copsi-service dafne-service tf-service sf-service iam-service gss-admin-service gss-catalogue-service gss-ingest-service

#### All docker volumes

    docker volume rm copsi-config copsi-html dafne-be-config dafne-be-logs dafne-db dafne-fe-config dafne-fe-html dr-api_logs kb_db pg-data pg-scripts sf-api_logs sf-config tf-config tf-data tf-logs tf-plugins tf-traces tf-output

#### Docker network 

    docker network rm collnetwork

#### Docker Swarm

    docker swarm leave --force

#### User 'colluser'

    userdel -r colluser

### How to restart services

#### COPSI

    docker stack rm copsi-service    
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/copsi_install_pkg/docker-compose.yml copsi-service

#### DAFNE

    docker stack rm dafne-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/dafne_install_pkg/docker-compose.yml dafne-service

#### TF

    docker stack rm tf-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/esa_tf_install_pkg/docker-compose.yml tf-service

#### SF

    docker stack rm sf-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/sf_install_pkg/docker-compose.yml sf-service

#### KEYCLOAK

    docker stack rm iam-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/keycloak/docker-compose.yml iam-service

#### GSS

    docker stack rm gss-admin-service
    docker stack rm gss-catalogue-service
    docker stack rm gss-ingest-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/gss_install_pkg/docker-compose_admin.yml gss-admin-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/gss_install_pkg/docker-compose_catalogue.yml gss-catalogue-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/gss_install_pkg/docker-compose_ingest.yml gss-ingest-service    

## Softwares configuration 

The softwares can be configured changing the content of these files:

COPSI:

- /var/lib/docker/volumes/copsi-config/_data/config.json

DAFNE:

- /var/lib/docker/volumes/dafne-be-config/_data/config.json

- /var/lib/docker/volumes/dafne-be-config/_data/db_credentials.env

- /var/lib/docker/volumes/dafne-fe-config/_data/config.json

SF:

- /var/lib/docker/volumes/sf-config/_data/configuration.json

- /var/lib/docker/volumes/sf-config/_data/keycloak_configuration.json

TF:

- /var/lib/docker/volumes/tf-config/_data/esa_tf.config

- /var/lib/docker/volumes/tf-config/_data/hubs_credentials.yaml

- /var/lib/docker/volumes/tf-config/_data/traceability_config.yaml

GSS:

- ./gss_install_pkg/config/admin/application.properties

- ./gss_install_pkg/config/catalogue/application.properties

- ./gss_install_pkg/config/catalogue/gss-catalogue.xml

- ./gss_install_pkg/config/ingest/gss-producer.xml

- ./gss_install_pkg/config/ingest/gss-consumer.xml

Please refer to documentation of each software regarding how to configure the files above and only for GSS softwares please refer also to [COPE-SERCO-TN-23-1461] - GSS COTS installation v1.1.

## Copyright

Copyright (c) DHS Suite Easy Deploy Ltd. and Contributors. See LICENSE for details.
