# 03_fan_service

## Goal
Create a ROS 2 service server that turns a cooling fan ON or OFF.
Create a service client that sends the request and prints the response.

## Concepts to learn
- Request/Response communication (Services)
- Standard service types (`std_srvs/srv/SetBool`)
- Calling services from CLI and Python

## Task checklist
- [ ] Write the fan service server node
- [ ] Test the server using `ros2 service call`
- [ ] Write the fan service client node
- [ ] Verify service listing and type with `ros2 service`

## Break it on purpose
- Stop the service server while the client tries to call it, and observe how the client behaves.

## What I learned
<!-- Write your own notes here after finishing this project -->
