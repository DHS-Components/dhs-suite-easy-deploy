
   function installCopsi()
   {

     checkservicecopsi=`docker service ls | grep "copsi" | wc -l`

     if [[ "$checkservicecopsi" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The COPSI software is already installed"

     else
 
       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation COPSI"

       status="NOK"

       runuser -l colluser -c "sudo docker volume create copsi-config"

       if [[ "$?" == "0" ]];then

          runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/config.json /var/lib/docker/volumes/copsi-config/_data/"

          if [[ "$?" == "0" ]];then

             runuser -l colluser -c "sudo docker volume create copsi-html"

             if [[ "$?" == "0" ]];then

                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/html/index.html /var/lib/docker/volumes/copsi-html/_data/"

                if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/copsi_install_pkg/docker-compose.yml copsi-service"

                   if [[ "$?" == "0" ]];then

                      runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/copsi_install_pkg/docker-compose.yml copsi-service"

                      status="OK"

                   fi

	        fi

	     fi

          fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm copsi-service"

	  runuser -l colluser -c "sudo docker volume rm copsi-config"

	  runuser -l colluser -c "sudo docker volume rm copsi-html"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] End installation COPSI not correctly"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] End installation COPSI correctly"

       fi

     fi

   }

   function installDafne()
   {
     
     checkservicedafne=`docker service ls | grep "dafne" | wc -l`

     if [[ "$checkservicedafne" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The DAFNE software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation DAFNE"

       status="NOK"

       if [[ "$?" == "0" ]];then

          runuser -l colluser -c 'sudo docker volume create dafne-fe-config'

          if [[ "$?" == "0" ]];then
	  
	     runuser -l colluser -c 'sudo docker volume create dafne-fe-html'

             if [[ "$?" == "0" ]];then
	     
	        runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/config/* /var/lib/docker/volumes/dafne-fe-config/_data/"

                if [[ "$?" == "0" ]];then
		
		    runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/html/* /var/lib/docker/volumes/dafne-fe-html/_data/"

                    if [[ "$?" == "0" ]];then
		    
		        runuser -l colluser -c "sudo docker volume create dafne-be-config"

                        if [[ "$?" == "0" ]];then
			
			    runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/back-end/config/* /var/lib/docker/volumes/dafne-be-config/_data/"

                            if [[ "$?" == "0" ]];then
			    
			        runuser -l colluser -c "sudo docker volume create dafne-db"

                                if [[ "$?" == "0" ]];then

                                    runuser -l colluser -c "sudo docker volume create dafne-be-logs"

                                    if [[ "$?" == "0" ]];then

                                        runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/dafne_install_pkg/docker-compose.yml dafne-service"

                                        status="OK"

                                    fi

			        fi

	                    fi

			fi

                    fi

		fi

             fi

	  fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c 'sudo docker volume rm dafne-fe-config'   

          runuser -l colluser -c 'sudo docker volume rm dafne-fe-html'	  

          runuser -l colluser -c "sudo docker volume rm dafne-be-config"

          runuser -l colluser -c "sudo docker volume rm dafne-db"

	  runuser -l colluser -c "sudo docker volume rm dafne-be-logs"

          runuser -l colluser -c "sudo docker stack rm dafne-service"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] End installation DAFNE not correctly"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] End installation DAFNE correctly"

       fi

     fi

   }

   function installTF()
   {

     checkservicetf=`docker service ls | grep "tf" | wc -l`

     if [[ "$checkservicetf" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The TF software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation TF"

       status="NOK"

       runuser -l colluser -c "sudo docker volume create tf-config"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo cp /home/colluser/$1/esa_tf_install_pkg/config/* /var/lib/docker/volumes/tf-config/_data/"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo docker volume create tf-data"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo mkdir -p /var/lib/docker/volumes/tf-data/_data/land-cover"

                   if [[ "$?" == "0" ]];then

                       runuser -l colluser -c "sudo docker volume create tf-plugins"

                       if [[ "$?" == "0" ]];then

                           runuser -l colluser -c "sudo docker volume create tf-traces"

                           if [[ "$?" == "0" ]];then

                               runuser -l colluser -c "sudo docker volume create tf-logs"

			       if [[ "$?" == "0" ]];then

                                    runuser -l colluser -c "sudo docker volume create tf-output"

                                    if [[ "$?" == "0" ]];then

                                        runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/esa_tf_install_pkg/docker-compose.yml tf-service"
                                        
				        status="OK"	

                                    fi

			       fi

			   fi

		       fi

		   fi

	       fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker volume rm tf-config" 

	  runuser -l colluser -c "sudo docker volume rm tf-data"

	  runuser -l colluser -c "sudo docker volume rm tf-plugins"

	  runuser -l colluser -c "sudo docker volume rm tf-traces"

	  runuser -l colluser -c "sudo docker volume rm tf-logs"

	  runuser -l colluser -c "sudo docker volume rm tf-output"

	  runuser -l colluser -c "sudo docker stack rm tf-service"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] End installation TF not correctly"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] End installation TF correctly"

       fi

     fi
   }

   function installIam()
   {

     checkserviceiam=`docker service ls | grep "iam" | wc -l`

     if [[ "$checkserviceiam" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The IAM software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation KEYCLOAK"

       status="NOK"

       runuser -l colluser -c "sudo docker volume create pg-scripts"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo docker volume create pg-data"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo cp /home/colluser/"$1"/keycloak/init-user-db.sh /var/lib/docker/volumes/pg-scripts/_data/"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo docker login -u onda.ops.team -p w]Ts+T72 https://docker-registry.onda-dias.eu"

                   if [[ "$?" == "0" ]];then

                       runuser -l colluser -c "cd /home/colluser/\"$1\"/keycloak; sudo docker build -t ciam-swarm-keycloak:1.0 .;"

                       if [[ "$?" == "0" ]];then

                           runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/"$1"/keycloak/docker-compose.yml iam-service"

                           status="OK"

		       fi

		   fi

	       fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker volume rm pg-data"

          runuser -l colluser -c "sudo docker volume rm pg-scripts"

	  runuser -l colluser -c "sudo docker stack rm iam-service"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] End installation KEYCLOAK not correctly"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] End installation KEYCLOAK correctly"

       fi

     fi

   }

   function installSF()
   {

     checkservicesf=`docker service ls | grep "sf" | wc -l`

     if [[ "$checkservicesf" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The SF software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation SF"

       status="NOK"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo docker volume create sf_config"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo docker volume create kb_db"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo docker volume create dr-api_logs"

                   if [[ "$?" == "0" ]];then

                       runuser -l colluser -c "sudo docker volume create sf-api_logs"

                       if [[ "$?" == "0" ]];then

                           runuser -l colluser -c "sudo cp /home/colluser/$1/sf_install_pkg/config/* /var/lib/docker/volumes/sf_config/_data/"

                           if [[ "$?" == "0" ]];then

                               runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/sf_install_pkg/docker-compose.yml sf-service"
                               
			       status="OK"  

                           fi

		       fi

		   fi

	       fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker volume create sf_config"

	  runuser -l colluser -c "sudo docker volume create kb_db"

	  runuser -l colluser -c "sudo docker volume create dr-api_logs"

	  runuser -l colluser -c "sudo docker volume create sf-api_logs"

	  runuser -l colluser -c "sudo docker stack rm sf-service"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] End installation SF not correctly"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] End installation SF correctly"

       fi

     fi

   }

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click begin"

   #Installation needed

   #install Docker engine=v20.10.21

   #install Docker compose=v2.12.2

   #Preliminary commands

   ip_machine=$1

   repository=$2

   listtoinstall=$3

   checkuser=`cat /etc/passwd | grep "colluser" | wc -l`

   if [[ "$checkuser" == "1" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The user 'colluser' already exists"
  
   else

     useradd colluser

     usermod -aG wheel colluser

     usermod -aG docker colluser

     chmod +w /etc/sudoers

     sed -i '/%wheel/d' /etc/sudoers

     echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created colluser"
  
   fi

   docker node ls

   if [[ "$?" == "0" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The swarm already exists"

   else

     docker swarm init --advertise-addr "$ip_machine"

     docker network create --driver=overlay --attachable -o com.docker.network.bridge.enable_icc=true collnetwork

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created swarm"

   fi

   runuser -l colluser -c "sudo ls /home/colluser/$repository"

   if [[ "$?" == "0" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The repository already exists"

   else

     runuser -l colluser -c "sudo curl -u vritrovato83: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 -LJO \"https://github.com/SercoSPA/$repository/archive/refs/tags/1.0.0.zip\""

     runuser -l colluser -c "sudo unzip 1.0.0.zip -d $repository"  

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Repository downloaded under /home/colluser"

   fi

   #COPSI

   if [[ "$listtoinstall" == *"copsi"* ]];then

      installCopsi "$repository"

   fi

   #DAFNE

   if [[ "$listtoinstall" == *"dafne"* ]];then

      installDafne "$repository"

   fi

   #TF

   if [[ "$listtoinstall" == *"tf"* ]];then

      installTF "$repository"

   fi

   #KEYCLOAK

   if [[ "$listtoinstall" == *"iam"* ]];then

      installIam "$repository"

   fi

   #SF

   if [[ "$listtoinstall" == *"sf"* ]];then

      installSF "$repository"

   fi

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click end"
