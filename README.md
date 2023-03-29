<p align="center">
  <img src="./LogoDHS.png" alt="DHS suite easy deploy" width="214" />
</p>

# DHS Suite Easy Deploy

The DHS suite is a tool allowing the installation of Collaborative Softwares in Docker Swarm environment, in particular if the machine where the suite will be installed is not in a swarm it will be added. The Docker swarm created will be a single node swarm and it is important to have on the machine these TCP/UDP ports opened 2376/2377/7946/4789.

## Prerequirements

The softwares needed to allow the installation are:

- Docker engine>=v20.10.21

- Docker compose>=v2.12.2

Rememeber that the minimum resources needed to install correctly the entire DHS suite are:

- CPU = 16cores + Ycores for TF

- RAM = 32GB + 6GB x Ycore for TF

- DISK = 350GB

## Download the package to be installed

The package having the installation content is downloadable by:

    curl -u vritrovato83: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 -LJO "https://github.com/SercoSPA/dhs-suite-easy-deploy/archive/refs/tags/1.0.0.zip"

and this package must be downloaded under /home folder by 'root' user.

After the download is needed to unzip the package and go inside it where is the installer script:

    unzip /home/dhs-suite-easy-deploy-1.0.0.zip

    cd /home/dhs-suite-easy-deploy-1.0.0

The version of the package for this installation is 1.0.0.

## Usage

### Softwares version installed

The softwares it can be installed with installer script are:

- COPSI: copsi 1.0.1

- DAFNE: dafne frontend 3.0.2, dafne backend 3.0.1, postgres 12.5

- TF: esa_tf_restapi and esa_tf_worker latest version, scheduler dask 2021.8.1-py3.9, nginx 1.21.6

- SF: virtuoso-opensource-7 latest version, sf-datareceiver v2.0, semantic_framework v2.3

- KEYCLOAK: custom version ciam-swarm-keycloak 1.0

### How to launch the installation

The installer script has 2 parameters, ip machine and list of softwares installable. If it wants to install ALL softwares the command to be executed from 'root' user is:

    ./2-click-installer.sh "<ip_machine>" "copsi,dafne,tf,sf,iam"

If it wants to install a subset of softwares, for instance copsi and dafne, execute this command from 'root' user:

    ./2-click-installer.sh "<ip_machine>" "copsi,dafne"

In order to configure the DHS suite as it wants it is needed to refer to section "Softwares configuration" and then, to restart the services, refer to section "How to restart services".

This installation will be create these docker volumes:

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

    docker stack rm copsi-service dafne-service tf-service sf-service iam-service

#### All docker volumes

    docker volume rm copsi-config copsi-html dafne-be-config dafne-be-logs dafne-db dafne-fe-config dafne-fe-html dr-api_logs kb_db pg-data pg-scripts sf-api_logs sf-config tf-config tf-data tf-logs tf-plugins tf-traces tf-output

#### Docker network 

    docker network rm collnetwork

#### Docker Swarm

    docker swarm leave --force

#### User 'colluser'

    userdel -r colluser

### How to restart services

#### Copsi

    docker stack rm copsi-service    
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/copsi_install_pkg/docker-compose.yml copsi-service

#### Dafne

    docker stack rm dafne-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/dafne_install_pkg/docker-compose.yml dafne-service

#### Tf

    docker stack rm tf-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/esa_tf_install_pkg/docker-compose.yml tf-service

#### Sf

    docker stack rm sf-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/sf_install_pkg/docker-compose.yml sf-service

#### Keycloak

    docker stack rm iam-service
    docker stack deploy --compose-file /home/colluser/dhs-suite-easy-deploy-1.0.0/keycloak/docker-compose.yml iam-service

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

Please refer to documentation of each software regarding how to configure the files above.

## Copyright

Copyright (c) DHS Suite Easy Deploy Ltd. and Contributors. See LICENSE for details.
