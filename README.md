# city-utilities-restful-wrapper
A REST service to request data from my energy provider.

Implemented alongside RESTful Sensor integration:
https://www.home-assistant.io/integrations/sensor.rest/

Credentials can be provided in a `credentials.py` file.

Building the docker image:
`docker build -t energy-service .` in the root directory

Running a docker container:
`docker run -d --name cu-energy-service -p 80:80 energy-service`