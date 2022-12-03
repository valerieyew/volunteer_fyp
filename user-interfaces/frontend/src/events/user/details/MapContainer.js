import React from 'react';
import { GoogleMap, LoadScript, InfoWindow } from '@react-google-maps/api';
import { useState, useEffect } from 'react';
import { Marker } from '@react-google-maps/api';
// import locations from '../../../data/output_locations.json';

const MapContainer = ({ locations }) => {

  const mapStyles = {
    height: "55vh",
    width: "80%",
  };

  const defaultCenter = {

    lat: 1.373232754683607, lng: 103.81026134919627
  }
  const [currentPosition, setCurrentPosition] = useState({});
  const [destination, setDestination] = useState([]);

  const success = position => {
    const currentPosition = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    }
    setCurrentPosition(currentPosition);
  };

  const [selected, setSelected] = useState([]);

  const onSelect = item => {
    setSelected(item);
    console.log("ITEMMMM ", item);
  }

  const [clusters, setClusters] = useState([]);
  // const getData = () => {
  // for (let i = 1; i <= locations.no_of_clusters; i++ ){
  //   setClusters([...clusters, locations['cluster_' + i]]);
  // }


  useEffect(() => {
    navigator.geolocation.getCurrentPosition(success);
    // getData();
    setDestination(locations[0]);
    setClusters(locations[1]);
    console.log(locations);
  })

  const markers = [
    "https://i.ibb.co/xCpY4dH/blue-dot.png", "https://i.ibb.co/r5h2nkL/pink-dot.png",
    "https://maps.google.com/mapfiles/ms/icons/purple-dot.png", "https://i.ibb.co/ScC9JGG/yellow-dot.png",
    "https://i.ibb.co/Z6CRBG5/green-dot.png",
    "https://i.ibb.co/5kH8Mwp/mm-20-orange.png","https://i.ibb.co/F5mY3PM/mm-20-brown.png",
    "https://i.ibb.co/YTrppnD/mm-20-gray.png", "https://i.ibb.co/8bSRB1B/red-dot.png",
     
  ]
  let counter = 0;
  let busCount = 0;

  const cluster1 = [
    {
      name: "Tuas Crescent MRT Station (EW31)",
      location: {
        lat: 1.32102695188066,
        lng: 103.649078232635
      },
    },
    {
      name: "Pioneer MRT Station (EW28)	",
      location: {
        lat: 1.33758688240768,
        lng: 103.697321513018
      },
    },
    {
      name: "Chinese Garden MRT Station (EW25)	",
      location: {
        lat: 1.34235282081403,
        lng: 103.732596738363
      },
    },
    {
      name: "Admiralty MRT Station (NS10)",
      location: {
        lat: 1.44058500086852,
        lng: 103.800988000403
      },
    }
  ];

  const cluster2 = [
    {
      name: "Buangkok MRT Station (NE15)",
      location: {
        lat: 1.38287785835055,
        lng: 103.893121564391
      },
    },
    {
      name: "Hougang MRT Station (NE14)",
      location: {
        lat: 1.37129229221246,
        lng: 103.892380518741
      },
    },
    {
      name: "Kovan MRT Station (NE13)	",
      location: {
        lat: 1.36017917065238,
        lng: 103.885064856353
      },
    }
  ];

  const cluster3 = [
    {
      name: "WOODLANDS MRT STATION",
      location: {
        lat: 1.43606698186149,
        lng: 103.787930806962
      },
    },
    {
      name: "ADMIRALTY MRT STATION",
      location: {
        lat: 1.44058500086852,
        lng: 103.800988000403
      },
    },
    {
      name: "Sembawang MRT Station (NS11)",
      location: {
        lat: 1.44905082158503,
        // const destination = [
        //   {
        //     name: "Somerset MRT Station (NS23)",
        //     location: { 
        //       lat: 1.30026416739007,
        //       lng: 103.839085753124
        //     },
        //   }
        // ];        lng: 103.820046140211
      },
    }
  ];





  //   const [directions, setDirections] = React.useState({})

  //   const DirectionsService = new window.google.maps.DirectionsService()

  //   const directionsRequest = ({ DirectionsService, origin, destination }) =>
  //   new Promise((resolve, reject) => {
  //     DirectionsService.route(
  //       {
  //         origin: new window.google.maps.LatLng(origin.location.lat, origin.location.lon),
  //         destination: new window.google.maps.LatLng(
  //           destination.location.lat,
  //           destination.location.lon
  //         ),
  //         travelMode: window.google.maps.TravelMode.DRIVING,
  //       },
  //       (result, status) => {
  //         if (status === window.google.maps.DirectionsStatus.OK) {
  //           resolve(result)
  //         } else {
  //           reject(status)
  //         }
  //       }
  //     )
  //   })

  //   const DIRECTION_REQUEST_DELAY = 300

  //     const delay = (time) =>
  //     new Promise((resolve) => {
  //         setTimeout(() => {
  //         resolve()
  //         }, time)
  //     })

  //     const waypoints = locations.map(p =>({
  //         location: {lat: p.location.lat, lng:p.location.long},
  //         stopover: true
  //     }))
  //     const origin = waypoints.shift().location;
  //     const destination = waypoints.pop().location;
  //     const Route = DirectionsService.route(
  //         {
  //           origin: origin,
  //           destination: destination,
  //           travelMode: window.google.maps.TravelMode.DRIVING,
  //           waypoints: waypoints
  //         },
  //         (result, status) => {
  //           if (status === window.google.maps.DirectionsStatus.OK) {
  //             this.setState({
  //               directions: result
  //             });
  //           } else {
  //             this.setState({ error: result });
  //           }
  //         }
  //       );

  //     const directionsToSelectedOrHoveredOrigin =
  //     directions[selectedOrHoveredOriginId]
  //   React.useEffect(() => {
  //     if (selectedOrHoveredOriginId && !directionsToSelectedOrHoveredOrigin) {
  //       const DirectionsService = new window.google.maps.DirectionsService()
  //       const fetchDirections = async () => {
  //         const selectedOrHoveredOrigin = origins.find(
  //           ({ id }) => selectedOrHoveredOriginId === id
  //         )
  //         const tempDirectionsToOrigin = []
  //         for (const destination of destinations) {
  //           const direction = await directionsRequest({
  //             DirectionsService,
  //             origin: {
  //               lat: selectedOrHoveredOrigin.coordinates.lat,
  //               lon: selectedOrHoveredOrigin.coordinates.lon,
  //             },
  //             destination: {
  //               lat: destination.coordinates.lat,
  //               lon: destination.coordinates.lon,
  //             },
  //           })
  //           await delay(DIRECTION_REQUEST_DELAY)
  //           tempDirectionsToOrigin.push(direction)
  //         }
  //         setDirections((prevState) => ({
  //           ...prevState,
  //           [selectedOrHoveredOriginId]: tempDirectionsToOrigin,
  //         }))
  //       }
  //       fetchDirections()
  //     }
  //   }, [
  //     destinations,
  //     directionsToSelectedOrHoveredOrigin,
  //     selectedOrHoveredOriginId,
  //     origins,
  //   ])

  return (
    <LoadScript googleMapsApiKey="AIzaSyBWcbR4iX_PUyxg3V7IVaBFD-nJvG6Xj1o">

      <div className="text-center  font-oswald text-[#873307] uppercase text-xl font-bold mb-8"
      >
        {/* <div>Estimated Cost: ${locations[0][0].total_cost}</div> */}
        {clusters.map((cluster) => {
          return (
            <div className="flex justify-center" key={busCount++}>
              <img
                src={markers[busCount]}
                className="w-55 h-55"
                alt="marker"
              />
              Bus {busCount + 1}: {cluster.bus_size} seater (est. duration: {cluster.duration} minutes)
            </div>


          );
        })}
      </div>
      <div className='flex justify-center'>
        <GoogleMap mapContainerStyle={mapStyles} zoom={11.5} center={defaultCenter}>
          {destination.map((item) => {
            return (
              <Marker
                key={item.destination[0]}
                position={{
                  lat: item.destination[1],
                  lng: item.destination[2]
                }}
                onClick={() => onSelect(item.destination)}
                icon={{
                  url: "https://i.ibb.co/8bSRB1B/red-dot.png",
                  scaledSize: { width: 55, height: 55 }
                }}
              />
            );
          })}
          {/* {clusters.map((cluster) => {
          return (
            clusters[cluster].map((item) => {

            }
            );
            
          );
        })} */}
        { clusters.map((cluster) => {
        return (
          <div key={counter++}>
            {/* <div>{template_name}</div> */}
            {
              
              cluster.locations_with_coordinates.slice(0,-1).map(item => {
                console.log(item);
                return(<Marker
                  key={item[0]}
                  position={{ 
                    lat: item[1],
                    lng: item[2]
                  }}
                  onClick={() => onSelect(item)}
                  icon={{
                    // fillColor: 'green',
                    // strokeColor: 'white'
                    url: markers[counter],
                    // anchor: anchorPoint
                    scaledSize: {width: 45, height: 45}
                    // scale: 5.0
                  }}
                />)
              })
            }
          </div>
        )
        })}
        
        {/* {cluster1.map((item) => {
          return (
            <Marker
              key={item.name}
              position={item.location}
              onClick={() => onSelect(item)}
              icon={{
                // fillColor: 'green',
                // strokeColor: 'white'
                url: "http://maps.google.com/mapfiles/ms/icons/pink-dot.png",
                // anchor: anchorPoint
              }}
            />
          );
        })}
        {cluster2.map((item) => {
          return (
            <Marker
              key={item.name}
              position={item.location}
              onClick={() => onSelect(item)}
              icon={{
                // fillColor: 'green',
                // strokeColor: 'white'
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                // anchor: anchorPoint
              }}
            />
          );
        })}

        {cluster3.map((item) => {
          return (
            <Marker
              key={item.name}
              position={item.location}
              onClick={() => onSelect(item)}
              icon={{
                // fillColor: 'green',
                // strokeColor: 'white'
                url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
                // anchor: anchorPoint
              }}
            />
          );
        })} */}
          {/* {cluster2.map((item) => {
          return (
            <Marker
              key={item.name}
              position={item.location}
              onClick={() => onSelect(item)}
              icon={{
                // fillColor: 'green',
                // strokeColor: 'white'
                url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                // anchor: anchorPoint
              }}
            />
          );
        })} */}
          {selected[1] && (
            <InfoWindow
              position={{
                lat: parseFloat(selected[1]),
                lng: parseFloat(selected[2])
              }}
              clickable={true}
              onCloseClick={() => setSelected({})}
            >
              <p className='text-lg'>{selected[0]}</p>
            </InfoWindow>
          )}
          {/* {selected.location && (
          <InfoWindow
            position={selected.location}
            clickable={true}
            onCloseClick={() => setSelected({})}
          >
            <p>{selected.name}</p>
          </InfoWindow>
        )} */}

        </GoogleMap>
      </div>

    </LoadScript>
  );
}

export default MapContainer;