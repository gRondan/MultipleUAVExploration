from connections import connections

my_ip = connections.get_server_ip()
connections.run_server(my_ip)
