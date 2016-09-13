run the agent (A): ./agent
run the local controller (LC): ./local
run the global controller (GC): ./global

they all run the respective *_config.yaml in ./config/localhost

there is no connection between GC--LC--A
it works in two modes: 1. GC--A, 2. LC--A

the GC successfully receives the IP address(es) from the machine where the LC or the A are
