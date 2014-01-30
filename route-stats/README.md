This script will parse through the config.yml file to get a list of routers and routes to be checked on each router.  It will then write details to a file for each host in the form of "key=value" in the /var/log/route-stats directory.  

It is dependent upon modified mpls.yml and routes.yml files that as of this writing are not present in the master py-junos-eznc repo.  However they are included here.
