
   function installCopsi()
   {

     checkservicecopsi=`docker service ls | grep "copsi-" | wc -l`

     if [[ "$checkservicecopsi" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The COPSI software is already installed"

     else
 
       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation COPSI"

       /home/colluser/$1/utils/remove_tag.sh copsi_tag	

       docker node update --label-add copsi_tag=true $copsi_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] copsi_tag added to $copsi_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] copsi_tag NOT added to $copsi_tag node"

       status="NOK"

       mkdir -p /shared/copsi-config/

       if [[ "$?" == "0" ]];then

                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/config.json /shared/copsi-config/"
                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/footprints_customization.json /shared/copsi-config/"
                runuser -l colluser -c "sudo cp /home/colluser/$1/copsi_install_pkg/data/copsi/config/product_details.json /shared/copsi-config/"


		   if [[ "$?" == "0" ]];then

		     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for COPSI"
			
		     runuser -l colluser -c "sudo docker stack deploy --compose-file /home/colluser/$1/copsi_install_pkg/docker-compose.yml copsi-service > /dev/null 2>&1"

                     if [[ "$?" == "0" ]];then

                        status="OK"

		        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for COPSI is terminated correctly"

                     fi

	           fi

       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm copsi-service > /dev/null 2>&1"

          rm -rf /shared/copsi-config/

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

       /home/colluser/$1/utils/remove_tag.sh dafne_tag

       docker node update --label-add dafne_tag=true $dafne_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] dafne_tag added to $dafne_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] dafne_tag NOT added to $dafne_tag node"

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
       
        /home/colluser/$1/utils/remove_tag.sh tf_tag

      docker node update --label-add tf_tag=true $tf_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] tf_tag added to $tf_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] tf_tag NOT added to $tf_tag node"

       status="NOK"

       if [[ "$?" == "0" ]];then

	   mkdir /shared/tf-config/

           mkdir /shared/tf-output/

           mkdir /shared/tf-data/

           mkdir /shared/tf-plugins/

           mkdir /shared/tf-traces/

           mkdir /shared/tf-logs/
	   
	   mkdir /shared/tf-nginx/

           runuser -l colluser -c "sudo cp /home/colluser/$1/esa_tf_install_pkg/config/* /shared/tf-config/"

           runuser -l colluser -c "sudo cp -rp /home/colluser/$1/esa_tf_install_pkg/nginx/* /shared/tf-nginx/"

           if [[ "$?" == "0" ]];then

                   runuser -l colluser -c "sudo mkdir -p /shared/tf-data/land-cover/"

                   if [[ "$?" == "0" ]];then

                                        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for TF"

					 runuser -l colluser -c "cd /home/colluser/$1/esa_tf_install_pkg/; source .env; sudo docker stack deploy --compose-file /home/colluser/$1/esa_tf_install_pkg/docker-compose.yml tf-service > /dev/null 2>&1"

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

          rm -rf /shared/tf-nginx


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
   
       /home/colluser/$1/utils/remove_tag.sh iam_tag

       docker node update --label-add iam_tag=true $iam_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] iam_tag added to $iam_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] iam_tag NOT added to $iam_tag node"

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

       /home/colluser/$1/utils/remove_tag.sh sf_tag

       docker network create --driver=bridge token-network > /dev/null 2>&1

       if [[ "$?" == "0" ]] ; then

    	 echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created Network for SF"

  	 else

    	 echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The Network for SF already exists"

       fi

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation volumes for SF"

       if [[ "$?" == "0" ]];then

           echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for SF"

           cd /home/colluser/$1/sf_install_pkg/; docker compose up > /dev/null 2>&1 & 
                               
           if [[ "$?" == "0" ]];then

              status="OK"

              echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation services for SF is terminated correctly"

           fi 

           fi


       if [[ "$status" == "NOK" ]];then


          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation SF is not terminated correctly, SF service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation SF is terminated with success"

       fi

     fi

   }


   function installGSS-admin(){

    checkservicegssadmin=`docker service ls | grep "gss-admin-service" | wc -l`

     if [[ "$checkservicegssadmin" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The GSS admin software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation GSS admin"

       /home/colluser/$1/utils/remove_tag.sh gss_admin_tag

       docker node update --label-add gss_admin_tag=true $gss_admin_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_admin_tag added to $gss_admin_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_admin_tag NOT added to $gss_admin_tag node"

       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for GSS admin"

       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_admin.yml gss-admin-service > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS ADMIN is terminated correctly"      

	  status="OK"
   
       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm gss-admin-service > /dev/null 2>&1"


          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation GSS admin is not terminated correctly, GSS admin service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation GSS admin is terminated with success"

       fi

     fi

   }


  function installGSS-ingest(){
	
    checkservicegssingest=`docker service ls | grep "gss-ingest-service" | wc -l`

     if [[ "$checkservicegssingest" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The GSS ingest software is already installed"

     else

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation GSS ingest"
       
       /home/colluser/$1/utils/remove_tag.sh gss_ingest_tag

       docker node update --label-add gss_ingest_tag=true $gss_ingest_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_ingest_tag added to $gss_ingest_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_ingest_tag NOT added to $gss_ingest_tag node"
       status="NOK"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for GSS ingest"

       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_ingest.yml gss-ingest-service > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS ingest is terminated correctly"     

          status="OK"		  
   
       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm gss-ingest-service > /dev/null 2>&1"


          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation GSS ingest is not terminated correctly, GSS ingest service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation GSS ingest is terminated with success"

       fi

    fi

   }


    function installGSS-catalogue(){
	
    checkservicegsscatalogue=`docker service ls | grep "gss-catalogue-service" | wc -l`

     if [[ "$checkservicegsscatalogue" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The GSS catalogue software is already installed"

     else

	echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation GSS catalogue"

       /home/colluser/$1/utils/remove_tag.sh gss_catalogue_tag

   	docker node update --label-add gss_catalogue_tag=true $gss_catalogue_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_catalogue_tag added to $gss_catalogue_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_catalogue_tag NOT added to $gss_catalogue_tag node"
		status="NOK"

	mkdir -p /shared/gss-catalogue-config/

	cp ./gss_install_pkg/config/catalogue/application.properties /shared/gss-catalogue-config/	   

	echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for GSS catalogue"

       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_catalogue.yml gss-catalogue-service > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS catalogue is terminated correctly"     

          status="OK"		  
   
       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm gss-catalogue-service > /dev/null 2>&1"


          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation GSS catalogue is not terminated correctly, GSS catalogue service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation GSS catalogue is terminated with success"

       fi

    fi

   }
   
    function installGSS-notification(){
	
    checkservicegssnotification=`docker service ls | grep "gss-notification-service" | wc -l`

     if [[ "$checkservicegssnotification" != 0  ]];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The GSS notification software is already installed"

     else

	echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin installation GSS notification"

        /home/colluser/$1/utils/remove_tag.sh gss_notification_tag

        docker node update --label-add gss_notification_tag=true $gss_notification_tag > /dev/null 2>&1 && echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_notification_tag added to $gss_notification_tag node" || echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] gss_notification_tag NOT added to $gss_notification_tag node"

        status="NOK"   

	echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Begin creation services for GSS notification"

       runuser -l colluser -c "cd /home/colluser/$1/gss_install_pkg/; sudo docker stack deploy --compose-file /home/colluser/$1/gss_install_pkg/docker-compose_notification.yml gss-notification-service > /dev/null 2>&1"

       if [[ "$?" == "0" ]];then

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Creation service for GSS notification is terminated correctly"     

          status="OK"		  
   
       fi

       if [[ "$status" == "NOK" ]];then

          runuser -l colluser -c "sudo docker stack rm gss-notification-service > /dev/null 2>&1"


          echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Installation GSS notification is not terminated correctly, GSS notification service has been removed"

       else

          echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Installation GSS notification is terminated with success"

       fi

    fi

   }


   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click installation begin"

   #Installation needed

   #install Docker engine=v20.10.21

   #install Docker compose=v2.12.2

   #Preliminary commands
   #Please be sure that the file  /etc/exports is configure to export the /shared folder to the machines of the same subnet 

   #check if /shared folder is configured in /etc/exports NFS configuration file
   shared=$(grep shared /etc/exports | wc -l)
   
   if [ $shared -eq -0 ] 

   then 

	echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] /shared folder not configured in /etc/exports"
	exit 10;

   else

	echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] /shared folder correctly configured in /etc/exports"

   fi
	
   showmount > /dev/null 2>&1

   if [ $? -ne 0 ]
   
   then

        echo echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] Please install showmount"

   fi

   exported=$(showmount -e $nfs_server_ip | grep shared | wc -l)

   if [ $exported -eq -0 ]

   then

        echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] /shared folder not correctly exported"
        exit 10;

   else

        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] /shared folder correctly exported"

   fi   

   #Source the configuration file
   source config.cfg

   listtoinstall=$1

   # Apply the nfs server IP to docker-compose files using nfs setting. Existing files must contain valid IP 
   find . -type f -name docker-compose.*.yml -exec sed -i "s/addr=[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/addr=$nfs_server_ip/" {} \;

   #clear all the tags before node update
   #./utils/remove_all_tags.sh

   checkuser=`cat /etc/passwd | grep "colluser" | wc -l`

   if [[ "$checkuser" == "1" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The user 'colluser' already exists"
  
   else

     useradd -m colluser

     #usermod -aG wheel colluser

     usermod -aG docker colluser

     chmod +w /etc/sudoers

     #sed -i '/%wheel/d' /etc/sudoers

     #echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
     echo "%colluser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created 'colluser' user"

     if [ -e /home/colluser ]; then

	   echo "colluser home directory exists"

     else

	   mkdir /home/colluser

	   chown colluser:colluser /home/colluser

	   echo "colluser home directory created"

     fi 
  
   fi

   docker network create --driver=overlay --attachable -o com.docker.network.bridge.enable_icc=true collnetwork > /dev/null 2>&1

   if [[ "$?" == "0" ]] ; then

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Created Network for Swarm"

   else

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The Network for Swarm already exists"

   fi

   runuser -l colluser -c "sudo ls /home/dhs-suite-easy-deploy-1.1.0 > /dev/null 2>&1"

   if [[ "$?" == "0" ]] ; then

     runuser -l colluser -c "sudo mv /home/dhs-suite-easy-deploy-1.1.0 /home/colluser/"

     echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] The package dhs-suite-easy-deploy-1.1.0 to be installed has been moved from /home to /home/colluser"

     runuser -l colluser -c "sudo touch /home/colluser/firstrundone"

   else

     if [ ! -f /home/colluser/firstrundone ];then

       echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] The package dhs-suite-easy-deploy-1.1.0 to be installed doesn't exist in /home"

       echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] If the script has been launched at first time please download before in /home the package dhs-suite-easy-deploy-1.1.0 from repository (view the README.md file for the details) and re-execute the script"

       exit

     fi

   fi

   #COPSI

   if [[ "$listtoinstall" == *"copsi"* ]];then

      installCopsi "dhs-suite-easy-deploy-1.1.0"

   fi

   #DAFNE

   if [[ "$listtoinstall" == *"dafne"* ]];then

      installDafne "dhs-suite-easy-deploy-1.1.0"

   fi

   #TF

   if [[ "$listtoinstall" == *"tf"* ]];then

      installTF "dhs-suite-easy-deploy-1.1.0"

   fi

   #KEYCLOAK

   if [[ "$listtoinstall" == *"iam"* ]];then

      installIam "dhs-suite-easy-deploy-1.1.0"

   fi

   #SF

   if [[ "$listtoinstall" == *"sf"* ]];then

      installSF "dhs-suite-easy-deploy-1.1.0"

   fi

   #GSS ADMIN

   if [[ "$listtoinstall" == *"gss-admin"* ]];then

      installGSS-admin "dhs-suite-easy-deploy-1.1.0"

   fi

   #GSS INGEST

   if [[ "$listtoinstall" == *"gss-ingest"* ]];then

      installGSS-ingest "dhs-suite-easy-deploy-1.1.0"

   fi

   #GSS CATALOGUE

   if [[ "$listtoinstall" == *"gss-catalogue"* ]];then

      installGSS-catalogue "dhs-suite-easy-deploy-1.1.0"

   fi

   #GSS NOTIFICATION

   if [[ "$listtoinstall" == *"gss-notification"* ]];then

      installGSS-notification "dhs-suite-easy-deploy-1.1.0"

   fi

   echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] Script 2 click installation is terminated with success"
