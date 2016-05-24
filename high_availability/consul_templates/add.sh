upstream service_reg_name_app {
  least_conn;
  {{range service "service_reg_name"}}
  server {{.Address}}:{{.Port}};
  {{else}}server 127.0.0.1:65535;{{end}}
}
server {
  listen 80;
  server_name service_name.yingz.info;
  location / {
    proxy_pass http://service_reg_name_app;
  }
} 
