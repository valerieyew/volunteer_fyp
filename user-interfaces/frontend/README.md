The volunteer management platform helps to make it easier for employees in our client company to initiate volunteer events and sign up for them. 

This project has two main components – the web application and the transport algorithm. We have divided the development of the web application into the frontend React application, and the backend which comprises of the microservices:

  (1) Accounts (authentication and authorization)
  
  (2) Events (events management)
  
  (3) Community (allow for communication between event organisers and participants)
  
  (4) Transport (takes the input pickup locations, destination and available bus capacities, and derives an optimised route for an event)
  
The transport component is a routing algorithm to help organizers choose a combination of buses easily for each event such that they can fetch all of the participants in a reasonable amount of time. 

To do so, we utilize 

  (1) an external routing engine, Open Source Routing Machine (OSRM),  
  
  (2) Python’s Scikit-Learn K-means library for clustering, and 
  
  (3) Python’s py2opt RouteFinder library to find the optimal route and duration.
