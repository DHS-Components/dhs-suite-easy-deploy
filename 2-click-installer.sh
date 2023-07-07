
   function installCopsi()
   {

     checkservicecopsi=`docker service ls | grep "copsi-" | wc -l`

     if [[ "$checkservicecopsi" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The COPSI software is already installed"

     else
 
       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation COPSI"

       status="NOK"

       mkdir -p /shared/copsi-config/
 
       mkdir -p /shared/copsi-html/

       if [[ "$?" == "0" ]];then

                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/config.json /shared/copsi-config/"

                if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/html/index.html /shared/copsi-html/"

		   if [[ "$?" == "0" ]];then

		     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for COPSI"

                     runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/copsi_install_pkg/docker-compose.yml copsi-service > /dev/null 2>&1"

                     if [[ "$?" == "0" ]];then

                        status="OK"

		        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for COPSI is terminated correctly"

                     fi

	           fi

	        fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm copsi-service > /dev/null 2>&1"

          rm -rf /shared/copsi-config/

          rm -rf /shared/copsi-html/

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation COPSI is not terminated correctly, COPSI service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation COPSI is terminated with success"

       fi

     fi

   }

   function installDafne()
   {
     
     checkservicedafne=`docker service ls | grep "dafne-" | wc -l`

     if [[ "$checkservicedafne" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The DAFNE software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation DAFNE"

       status="NOK"

       if [[ "$?" == "0" ]];then

             mkdir -p /shared/dafne-fe-config/

             mkdir -p /shared/dafne-be-config/

             mkdir -p /shared/dafne-db/

             mkdir -p /shared/dafne-be-logs/

	     mkdir -p /shared/dafne-fe-html/

             if [[ "$?" == "0" ]];then
	     
	        runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/config/* /shared/dafne-fe-config/"
                if [[ "$?" == "0" ]];then
		    
			    runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/back-end/config/* /shared/dafne-be-config/"

                            if [[ "$?" == "0" ]];then

				  runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/html/* /shared/dafne-fe-html/"
			    
                                  if [[ "$?" == "0" ]];then

                                        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for DAFNE"

                                        runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/dafne_install_pkg/docker-compose.yml dafne-service > /dev/null 2>&1"

                                        if [[ "$?" == "0" ]];then

                                            status="OK"

                                            echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for DAFNE is terminated correctly"

                                        fi

		                  fi

			    fi

                fi

             fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm dafne-service > /dev/null 2>&1"

          rm -rf /shared/dafne-fe-config/

          rm -rf /shared/dafne-be-config/

          rm -rf /shared/dafne-db/

          rm -rf /shared/dafne-be-logs/

          rm -rf /shared/dafne-fe-html/

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation DAFNE is not terminated correctly, DAFNE service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation DAFNE is terminated with success"

       fi

     fi

   }

   function installTF()
   {

     checkservicetf=`docker service ls | grep "tf-" | wc -l`

     if [[ "$checkservicetf" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The TF software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation TF"

       status="NOK"

       if [[ "$?" == "0" ]];then

	   mkdir /shared/tf-config/

           mkdir /shared/tf-output/

           mkdir /shared/tf-data/

           mkdir /shared/tf-plugins/

           mkdir /shared/tf-traces/

           mkdir /shared/tf-logs/

           runuser -l colluser -c "sudo cp /home/colluser/$1/esa_tf_install_pkg/config/* /shared/tf-config/"

           if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo mkdir -p /shared/tf-data/land-cover/"

                   if [[ "$?" == "0" ]];then

                                        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for TF"

                                        runuser -l colluser -c "cd /home/colluser/$1/esa_tf_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/esa_tf_install_pkg/docker-compose.yml tf-service > /dev/null 2>&1"
                                        
				        if [[ "$?" == "0" ]];then

                                            status="OK"

                                            echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for TF is terminated correctly"

                                        fi 

		   fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm tf-service > /dev/null 2>&1"

          rm -rf /shared/tf-config/

          rm -rf /shared/tf-output/

          rm -rf /shared/tf-data/

          rm -rf /shared/tf-plugins/

          rm -rf /shared/tf-traces/

          rm -rf /shared/tf-logs/

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation TF is not terminated correctly, TF service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation TF is terminated with success"

       fi

     fi
   }

   function installIam()
   {

     checkserviceiam=`docker service ls | grep "iam-" | wc -l`

     if [[ "$checkserviceiam" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The KEYCLOAK software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation KEYCLOAK"

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for KEYCLOAK"

       runuser -l colluser -c "sudo docker volume create pg-scripts > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo docker volume create pg-data > /dev/null 2>&1"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo cp /home/colluser/"$1"/keycloak/init-user-db.sh /var/lib/docker/volumes/pg-scripts/_data/"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "cd /home/colluser/\"$1\"/keycloak; sudo docker build -t ciam-swarm-keycloak:1.0 . > /dev/null 2>&1;"

                   if [[ "$?" == "0" ]];then

		       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation volumes for KEYCLOAK is terminated correctly"

                       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for KEYCLOAK"

                       runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/"$1"/keycloak/docker-compose.yml iam-service > /dev/null 2>&1"

                       if [[ "$?" == "0" ]];then

                           status="OK"

                           echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for KEYCLOAK is terminated correctly"

                       fi 

		   fi

	       fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker volume rm pg-data > /dev/null 2>&1"

          runuser -l colluser -c "sudo docker volume rm pg-scripts > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker stack rm iam-service > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation KEYCLOAK is not terminated correctly, KEYCLOAK service and all relative volumes have been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation KEYCLOAK is terminated with success"

       fi

     fi

   }

   function installSF()
   {

     checkservicesf=`docker service ls | grep "sf-" | wc -l`

     if [[ "$checkservicesf" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The SF software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation SF"

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for SF"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo docker volume create sf-config > /dev/null 2>&1"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo docker volume create kb_db > /dev/null 2>&1"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo docker volume create dr-api_logs > /dev/null 2>&1"

                   if [[ "$?" == "0" ]];then

                       runuser -l colluser -c "sudo docker volume create sf-api_logs > /dev/null 2>&1"

                       if [[ "$?" == "0" ]];then

                           runuser -l colluser -c "sudo cp /home/colluser/$1/sf_install_pkg/config/* /var/lib/docker/volumes/sf-config/_data/"

                           if [[ "$?" == "0" ]];then

			       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation volumes for SF is terminated correctly"

                               echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for SF"

                               runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/sf_install_pkg/docker-compose.yml sf-service > /dev/null 2>&1"
                               
			       if [[ "$?" == "0" ]];then

                                   status="OK"

                                   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for SF is terminated correctly"

                               fi 

                           fi

		       fi

		   fi

	       fi

	   fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker volume rm sf-config > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm kb_db > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm dr-api_logs > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm sf-api_logs > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker stack rm sf-service > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation SF is not terminated correctly, SF service and all relative volumes have been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation SF is terminated with success"

       fi

     fi

   }

   function installGSS()
   {

     checkservicegss=`docker service ls | grep "gss-" | wc -l`

     if [[ "$checkservicegss" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The GSS software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation GSS"

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for GSS"

       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_admin.yml gss-admin-service > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then
	   
	  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS ADMIN is terminated correctly"
	   
          runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_catalogue.yml gss-catalogue-service > /dev/null 2>&1"
		   
          if [[ "$?" == "0" ]];then
		   
	       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS CATALOGUE is terminated correctly"
	   
	       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_ingest.yml gss-ingest-service > /dev/null 2>&1"
				
	       if [[ "$?" == "0" ]];then
				
	            echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS INGEST is terminated correctly"

		    status="OK"

		    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for GSS is terminated correctly"
				
	       fi

          fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm gss-admin-service > /dev/null 2>&1"
		  
          runuser -l colluser -c "sudo docker stack rm gss-catalogue-service > /dev/null 2>&1"
		  
	  runuser -l colluser -c "sudo docker stack rm gss-ingest-service > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation GSS is not terminated correctly, GSS services have been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation GSS is terminated with success"

       fi

     fi

   }

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click installation begin"

   #Installation needed

   #install Docker engine=v20.10.21

   #install Docker compose=v2.12.2

   #Preliminary commands

   ip_machine=$1

   listtoinstall=$2

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

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created 'colluser' user"
  
   fi

   docker network create --driver=overlay --attachable -o com.docker.network.bridge.enable_icc=true collnetwork > /dev/null 2>&1

   if [[ "$?" == "0" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created Network for Swarm"

   else

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The Network for Swarm already exists"

   fi

   runuser -l colluser -c "sudo ls /home/dhs-suite-easy-deploy-1.0.0 > /dev/null 2>&1"

   if [[ "$?" == "0" ]] ; then

     runuser -l colluser -c "sudo mv /home/dhs-suite-easy-deploy-1.0.0 /home/colluser/"

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The package dhs-suite-easy-deploy-1.0.0 to be installed has been moved from /home to /home/colluser"

     runuser -l colluser -c "sudo touch /home/colluser/firstrundone"

   else

     if [ ! -f /home/colluser/firstrundone ];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] The package dhs-suite-easy-deploy-1.0.0 to be installed doesn't exist in /home"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] If the script has been launched at first time please download before in /home the package dhs-suite-easy-deploy-1.0.0 from repository (view the README.md file for the details) and re-execute the script"

       exit

     fi

   fi

   #COPSI

   if [[ "$listtoinstall" == *"copsi"* ]];then

      installCopsi "dhs-suite-easy-deploy-1.0.0"

   fi

   #DAFNE

   if [[ "$listtoinstall" == *"dafne"* ]];then

      installDafne "dhs-suite-easy-deploy-1.0.0"

   fi

   #TF

   if [[ "$listtoinstall" == *"tf"* ]];then

      installTF "dhs-suite-easy-deploy-1.0.0"

   fi

   #KEYCLOAK

   if [[ "$listtoinstall" == *"iam"* ]];then

      installIam "dhs-suite-easy-deploy-1.0.0"

   fi

   #SF

   if [[ "$listtoinstall" == *"sf"* ]];then

      installSF "dhs-suite-easy-deploy-1.0.0"

   fi

   #SF

   if [[ "$listtoinstall" == *"gss"* ]];then

      installGSS "dhs-suite-easy-deploy-1.0.0"

   fi

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click installation is terminated with success"
