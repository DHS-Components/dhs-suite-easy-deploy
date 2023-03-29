
   function installCopsi()
   {

     checkservicecopsi=`docker service ls | grep "copsi-" | wc -l`

     if [[ "$checkservicecopsi" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The COPSI software is already installed"

     else
 
       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation COPSI"

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for COPSI"

       runuser -l colluser -c "sudo docker volume create copsi-config > /dev/null 2>&1"
 
       if [[ "$?" == "0" ]];then

          runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/config.json /var/lib/docker/volumes/copsi-config/_data/"

          if [[ "$?" == "0" ]];then

             runuser -l colluser -c "sudo docker volume create copsi-html > /dev/null 2>&1"

             if [[ "$?" == "0" ]];then

                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/html/index.html /var/lib/docker/volumes/copsi-html/_data/"

                if [[ "$?" == "0" ]];then

	           echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation volumes for COPSI is terminated correctly"

		   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for COPSI"

                   runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/copsi_install_pkg/docker-compose.yml copsi-service > /dev/null 2>&1"

                   if [[ "$?" == "0" ]];then

                      status="OK"

		      echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for COPSI is terminated correctly"

                   fi

	        fi

	     fi

          fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm copsi-service > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm copsi-config > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm copsi-html > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation COPSI is not terminated correctly, COPSI service and all relative volumes have been removed"

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

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for DAFNE"

       if [[ "$?" == "0" ]];then

          runuser -l colluser -c 'sudo docker volume create dafne-fe-config > /dev/null 2>&1'

          if [[ "$?" == "0" ]];then
	  
	     runuser -l colluser -c 'sudo docker volume create dafne-fe-html > /dev/null 2>&1'

             if [[ "$?" == "0" ]];then
	     
	        runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/config/* /var/lib/docker/volumes/dafne-fe-config/_data/"

                if [[ "$?" == "0" ]];then
		
		    runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/front-end/html/* /var/lib/docker/volumes/dafne-fe-html/_data/"

                    if [[ "$?" == "0" ]];then
		    
		        runuser -l colluser -c "sudo docker volume create dafne-be-config > /dev/null 2>&1"

                        if [[ "$?" == "0" ]];then
			
			    runuser -l colluser -c "sudo cp /home/colluser/$1/dafne_install_pkg/data/dafne/back-end/config/* /var/lib/docker/volumes/dafne-be-config/_data/"

                            if [[ "$?" == "0" ]];then
			    
			        runuser -l colluser -c "sudo docker volume create dafne-db > /dev/null 2>&1"

                                if [[ "$?" == "0" ]];then

                                    runuser -l colluser -c "sudo docker volume create dafne-be-logs > /dev/null 2>&1"

                                    if [[ "$?" == "0" ]];then

					echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation volumes for DAFNE is terminated correctly"

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

		fi

             fi

	  fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c 'sudo docker volume rm dafne-fe-config > /dev/null 2>&1'   

          runuser -l colluser -c 'sudo docker volume rm dafne-fe-html > /dev/null 2>&1'	  

          runuser -l colluser -c "sudo docker volume rm dafne-be-config > /dev/null 2>&1"

          runuser -l colluser -c "sudo docker volume rm dafne-db > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm dafne-be-logs > /dev/null 2>&1"

          runuser -l colluser -c "sudo docker stack rm dafne-service > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation DAFNE is not terminated correctly, DAFNE service and all relative volumes have been removed"

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

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for TF"

       runuser -l colluser -c "sudo docker volume create tf-config > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

           runuser -l colluser -c "sudo cp /home/colluser/$1/esa_tf_install_pkg/config/* /var/lib/docker/volumes/tf-config/_data/"

           if [[ "$?" == "0" ]];then

               runuser -l colluser -c "sudo docker volume create tf-data > /dev/null 2>&1"

               if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo mkdir -p /var/lib/docker/volumes/tf-data/_data/land-cover"

                   if [[ "$?" == "0" ]];then

                       runuser -l colluser -c "sudo docker volume create tf-plugins > /dev/null 2>&1"

                       if [[ "$?" == "0" ]];then

                           runuser -l colluser -c "sudo docker volume create tf-traces > /dev/null 2>&1"

                           if [[ "$?" == "0" ]];then

                               runuser -l colluser -c "sudo docker volume create tf-logs > /dev/null 2>&1"

			       if [[ "$?" == "0" ]];then

                                    runuser -l colluser -c "sudo docker volume create tf-output > /dev/null 2>&1"

                                    if [[ "$?" == "0" ]];then

					echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation volumes for TF is terminated correctly"

                                        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for TF"

                                        runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/esa_tf_install_pkg/docker-compose.yml tf-service > /dev/null 2>&1"
                                        
				        if [[ "$?" == "0" ]];then

                                            status="OK"

                                            echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for TF is terminated correctly"

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

          runuser -l colluser -c "sudo docker volume rm tf-config > /dev/null 2>&1" 

	  runuser -l colluser -c "sudo docker volume rm tf-data > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm tf-plugins > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm tf-traces > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm tf-logs > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker volume rm tf-output > /dev/null 2>&1"

	  runuser -l colluser -c "sudo docker stack rm tf-service > /dev/null 2>&1"

          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation TF is not terminated correctly, TF service and all relative volumes have been removed"

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

                   runuser -l colluser -c "cd /home/colluser/\"$1\"/keycloak; sudo docker build -t ciam-swarm-keycloak:1.0 .;"

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

   docker node ls

   if [[ "$?" == "0" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The Docker Swarm already exists"

   else

     docker swarm init --advertise-addr "$ip_machine" > /dev/null 2>&1

     docker network create --driver=overlay --attachable -o com.docker.network.bridge.enable_icc=true collnetwork > /dev/null 2>&1

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created Docker Swarm"

   fi

   runuser -l colluser -c "sudo ls /home/dhs-suite-easy-deploy-1.0.0"

   if [[ "$?" == "1" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] The package dhs-suite-easy-deploy-1.0.0 to be installed doesn't exist in /home"

     echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] If the script has been launched at first time please download before in /home the package dhs-suite-easy-deploy-1.0.0 from repository (view the README.md file for the details) and re-execute the script"

     exit

   else

     runuser -l colluser -c "sudo mv /home/dhs-suite-easy-deploy-1.0.0 /home/colluser/"

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The package dhs-suite-easy-deploy-1.0.0 to be installed has been moved from /home to /home/colluser"

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

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click installation is terminated with success"
