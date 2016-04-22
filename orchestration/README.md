nap-compose.yml
ports:
  - container_port:host_port:tcp //default tcp
  - container_port:host_port:udp
  - container_port::tcp
  - container_port::udp
  - container_port
  - container_port:host_port

network: a

volumes:
  - container_path:host_path:rw //default
  - container_path:host_path:ro
  - container_path:host_path
  - container_path::ro
  - container_path

yml解读

remote api