const urlFastAPI = "http://127.0.0.1:8000/api";


//   FUNCIONES DE CREACION DE ENTIDADES EN EL MAPA
// Función para validar que el input solo contenga números
function validarNumeros(input) {
  input.value = input.value.replace(/\D/g, '');
}

// Función para obtener el color según la temperatura
function getColorForTemperature(temp) {
  if (temp <= 0) {
    return Cesium.Color.BLUE.withAlpha(0.3);
  } else if (temp <= 15) {
    return Cesium.Color.CYAN.withAlpha(0.3);
  } else if (temp <= 18) {
    return Cesium.Color.GREEN.withAlpha(0.3);
  } else if (temp <= 19) {
    return Cesium.Color.YELLOW.withAlpha(0.3);
  } else {
    return Cesium.Color.RED.withAlpha(0.3);
  }
}

// Funciones para crear entidades en el visor de Cesium
// Estas funciones crean diferentes tipos de entidades (puntos, polígonos, líneas, etc.)
// Cada función toma los datos de la entidad y los añade al visor.

function crearPunto(datosPunto,altura=0) {
    const coordenadas = datosPunto.geometry.coordinates;
    const [lon, lat] = coordenadas;
    console.log('Coordenadas:', coordenadas);
    console.log('Lat:', lat, 'Lon:', lon);

    createPropertiesPanel(datosPunto.properties);

    viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(lon, lat, 0), // Altura 0 para el terreno
      name: datosPunto.properties.direccion || 'Sin dirección',
      description: createPropertiesPanel(datosPunto.properties),
      point:{
        pixelSize: 7,
        color: Cesium.Color.RED.withAlpha(0.8),
        outlineColor: Cesium.Color.BLACK,
        outlineWidth: 1,
        heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND, // Úsalo si el punto está en terreno
        disableDepthTestDistance: Number.POSITIVE_INFINITY // Siempre visible encima del terreno
      }
    });
    
    if (datosPunto.properties.temperatura)
    {
      viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat),
        ellipsoid: {
          radii: new Cesium.Cartesian3(500.0, 500.0, 500),
          material: getColorForTemperature(datosPunto.properties.temperatura),
          heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND  ,
          disableDepthTestDistance: Number.POSITIVE_INFINITY
        }        
      });
    }
  }


  function crearPoligono(datosPoligono,altura=0) {
    const coordenadas = datosPoligono.geometry.coordinates[0]; // Asumiendo que es un polígono simple
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;

      return Cesium.Cartesian3.fromDegrees(lon, lat); // Multiplicamos por 1000 para convertir a metros
    });


    viewer.entities.add({
      description: createPropertiesPanel(datosPoligono.properties),
      polygon: {
        hierarchy: new Cesium.PolygonHierarchy(posiciones),
        material: Cesium.Color.BLUE.withAlpha(0.5),
        outline: true,
        outlineColor: Cesium.Color.BLACK,
      }
    });
  }

  function crearPoligonoCatastro(datosPoligono,altura=0) {
    const coordenadas = datosPoligono.geometry.coordinates[0]; // Asumiendo que es un polígono simple
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;

      return Cesium.Cartesian3.fromDegrees(lon, lat); // Multiplicamos por 1000 para convertir a metros
    });

    viewer.entities.add({
      description: createPropertiesPanel(datosPoligono.properties),
      polygon: {
        hierarchy: new Cesium.PolygonHierarchy(posiciones),
        material: Cesium.Color.RED.withAlpha(0.5),
        outline: true,
        outlineColor: Cesium.Color.BLACK,
        clampToGround: true, // Para que el polígono se ajuste al terreno
        heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND, // Úsalo si el polígono está en terreno
        disableDepthTestDistance: Number.POSITIVE_INFINITY,
        height: altura, // Altura del polígono
        extrudedHeight: 3, // Altura del polígono extruido
        // height: altura, // Altura del polígono
        // clampToGround: false // Para que el polígono se ajuste al terreno
      }
    });
  }

  function crearLinea(datosLinea,altura=0) {
    const coordenadas = datosLinea.geometry.coordinates;
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;
      return Cesium.Cartesian3.fromDegrees(lon, lat, 0);
    });

    viewer.entities.add({
      description: createPropertiesPanel(datosLinea.properties),
      polyline: {
        positions: posiciones,
        material: Cesium.Color.BLUE,
        width: 5
      }
    });
  }


  function crearMultipoligono(datosMultipoligono,altura=0) {
    
   const coordenadas = datosMultipoligono.geometry.coordinates[0][0]; // Asumiendo que es un polígono simple
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;
      return Cesium.Cartesian3.fromDegrees(lon, lat);
    });

    viewer.entities.add({
      // position : Cesium.Cartesian3.fromDegrees(datosMultipoligono.geometry.coordinates[0][0],0),
      description: createPropertiesPanel(datosMultipoligono.properties),
      polygon: {
        hierarchy: posiciones,
        material: Cesium.Color.BLUE.withAlpha(0.5),
        // outline: true,
        // outlineColor: Cesium.Color.BLACK
      }
    });
  }

  function crearMultilinea(datosMultilinea,altura=0) {
    const coordenadas = datosMultilinea.geometry.coordinates[0]; // Asumiendo que es un polígono simple
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;
      return Cesium.Cartesian3.fromDegrees(lon, lat);
    });

    viewer.entities.add({ 
      description: createPropertiesPanel(datosMultilinea.properties),
      corridor: {
        positions: posiciones,
        width: 10.0,
        material: Cesium.Color.BLUE.withAlpha(0.5),
        clampToGround: true
      }
    });
  }


  function crearLineString(datosLineString,altura=0) {
    const coordenadas = datosLineString.geometry.coordinates; 
    const posiciones = coordenadas.map(coord => {
      const [lon, lat] = coord;
      return Cesium.Cartesian3.fromDegrees(lon, lat, 0);
    });

    viewer.entities.add({
      description: createPropertiesPanel(datosLineString.properties), 
      polyline: {
        positions: posiciones,
        material: Cesium.Color.RED.withAlpha(0.5),
        width: 5,
        clampToGround: true // Para que la línea se ajuste al terreno
      },
      label: {
        text: datosLineString.properties.DIRECCION || 'Sin dirección',
        font: '18pt sans-serif',
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        outlineWidth: 2,
        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
        pixelOffset: new Cesium.Cartesian2(0, -12),
        heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND, // Úsalo si el punto está en terreno
        disableDepthTestDistance: Number.POSITIVE_INFINITY // Siempre visible encima del terreno
      }
    });
  }


  async function insertCathedralBuilding() {
    Cesium.Ion.defaultAccessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3YWQ3ZWY4ZS03NzBjLTRjNzktYTYyNy0zMTRkYmE1NmE1NDciLCJpZCI6MjgwODk3LCJpYXQiOjE3NDEwNzIzMzl9.rpQ6pVt0APCbZ_zhTJkhquCVXwmMo3unuk4ZafCea-k";
    try {
      const tileset = await Cesium.Cesium3DTileset.fromIonAssetId(3459233);
      viewer.scene.primitives.add(tileset);
      await viewer.zoomTo(tileset);

      // Apply the default style if it exists
      const extras = tileset.asset.extras;
      if (
        Cesium.defined(extras) &&
        Cesium.defined(extras.ion) &&
        Cesium.defined(extras.ion.defaultStyle)
      ) {
        tileset.style = new Cesium.Cesium3DTileStyle(extras.ion.defaultStyle);
      }
    } catch (error) {
      console.log(error);
    }
  }

  // Función para cargar un tileset de Google Photorealistic 3D Tiles
  async function mostrar3DTilesGoogle(){
     try {
      window.googleTileset = await Cesium.createGooglePhotorealistic3DTileset({
        // Only the Google Geocoder can be used with Google Photorealistic 3D Tiles.  Set the `geocode` property of the viewer constructor options to IonGeocodeProviderType.GOOGLE.
        onlyUsingWithGoogleGeocoder: true,
      });
      viewer.scene.primitives.add(googleTileset);
    } catch (error) {
      console.log(`Error loading Photorealistic 3D Tiles tileset.
      ${error}`);
    }
  }



  // FUNCION PARA CARGAR UN GEOJSON EN EL VISOR
  // console.log(Cesium.VERSION);
  function cargarGeoJSON(ruta,IsCatastro=false) {

    mostrarSpinner();

    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(-1.6456,42.8125, 7000),
    });
      
    var dataSource;
    fetch(ruta,{
        method: 'GET', // o 'POST', 'PUT', etc.
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + window.token
        }
      })
      .then(response => response.json())
      .then(data => {
        dataSource= data;
        let entidades=null;
        
        if (!Array.isArray(dataSource)){
           entidades = dataSource.features;  
        }
        else {
            entidades = dataSource[0].features;
        }

        if (!entidades ) {
          console.warn("No se encontraron entidades en el GeoJSON."); 
          return;
        }
        
          
        for (let i = 0; i < entidades.length; i++) {
          
          let altura = entidades[i].properties.altura;

          switch (entidades[i].geometry.type) {
            case 'Point':
              console.log('Es un punto');
              crearPunto(entidades[i],IsCatastro ? altura : 0);
              break;
            case 'Polygon':
              console.log('Es un polígono');
              if (!IsCatastro) 
                crearPoligono(entidades[i],IsCatastro ? altura : 0);
              else
                crearPoligonoCatastro(entidades[i],IsCatastro ? altura : 0);

              break;
            case 'LineString':
              console.log('Es una línea');
              crearLineString(entidades[i],IsCatastro ? altura : 0);
              break;
            case 'MultiPolygon':
              console.log('Es un multipolígono');
              crearMultipoligono(entidades[i],IsCatastro ? altura : 0);
              break;
            case 'MultiLineString':
              console.log('Es una multilínea');
              crearMultilinea(entidades[i],IsCatastro ? altura : 0);
              break;
            default:
              console.log('Tipo de geometría no soportado');
          }
        }

        // puntoPamplona()
        console.log('finalizado');
        ocultarSpinner();
        return dataSource[0].features[0].properties.feature
      })
      .catch(error => {
        ocultarSpinner();
        console.error("Error al leer el GeoJSON:", error);
      }
        
    );
  }//FIN cargarGeoJSON 
  
  // Función para limpiar entidades del visor
  function limpiarEntidades() {
    // Limpiar todas las entidades del visor
    viewer.entities.removeAll();
  }

  // Función para limpiar primitivas del visor
  function limpiarPrimitivas() {
    // Limpiar todas las entidades del visor
    viewer.scene.primitives.removeAll();
  }

  // Función para volar a un punto específico: Pamplona
  function puntoPamplona() {
    viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(-1.6756,42.7415, 7000),
        orientation: {
            heading: Cesium.Math.toRadians(10.0),  
            pitch: Cesium.Math.toRadians(-40.0),
            roll: 0.0
        }
      });
  }

  // Funciones para volar a una ubicación específica
  function volarA(lon,lat,alt=7000) {
    viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(lon,lat, alt),
      });
  }
  
  // Función para mover la cámara a una ubicación específica
  function cameraIrA(lon,lat,alt=7000) {
    viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(lon,lat, alt),
      });
  }

  function cargarRutaVehicle() {
    // Cargar CZML
    viewer.dataSources.add(Cesium.CzmlDataSource.load('datos/Vehicle.czml'));
    viewer.scene.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(-116.52, 35.02, 95000),
      orientation: {
        heading: 6,
      },
    });
    volarA(-116.52, 35.02,8000)
  }

  // FUNCION PARA ABRIR O CERRAR UN SUBÁRBOL EN EL MENÚ LATERAL
  function toggleSubtree(element) {
    const subtree = element.nextElementSibling;
    subtree.classList.toggle("active");
  }

  // Función para alternar entre vista 2D y 3D
  // window.is3D = true; // Variable para controlar la vista actual
  // function toggleView() {
    
  //   if (window.is3D) {
  //     document.getElementById("map").style.display =  "none" ;
  //     document.getElementById("cesiumContainer").style.display = "block";
  //     window.is3D = !window.is3D;
  //   }
  //   else
  //   {
  //     document.getElementById("map").style.display = "block" ;
  //     document.getElementById("cesiumContainer").style.display = "none";
  //     window.is3D = !window.is3D;
  //   }
  // }

  // Función para obtener el estado de la base de datos
  function dbStatus(){
    fetch(urlBase +':8000/')
    .then(response => response.json())
    .then(data => console.log("Status de BD:" + data.json()))
    .catch(error => console.error('Error:', error));
  }


  async function getLayersNames() {
    mostrarSpinner();
    const selectCapas = document.getElementById('capasGeopamplona');
    const urlcapas = urlFastAPI + "/tablesgeopamplona";
    
    fetch(urlcapas, {
        method: 'GET', // o 'POST', 'PUT', etc.
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + window.token
        }
    })
        .then(response => response.json())
        .then(data => {
            data.forEach(dato => {
              const option = document.createElement('li');
              option.id = dato;
              option.value = dato;
              option.textContent = dato;

              // Crear el checkbox
              const checkbox = document.createElement('input');
              checkbox.type = 'checkbox';
              checkbox.checked = true; // Inicialmente visible
              checkbox.id = 'layer_'+dato;
              // capa='layer_'+dato;

              // Agregar el checkbox y el label al <li>
              option.appendChild(checkbox);

              option.addEventListener('click', function() {
                limpiarEntidades();
                const urlGeoJson = urlFastAPI + "/getgeojson/" + dato;
                cargarGeoJSON(urlGeoJson);
              });
              selectCapas.appendChild(option);
            });
            ocultarSpinner();
          }
    )
    .catch(error =>{
      ocultarSpinner();
      console.error("Error al leer el GeoJSON:", error);
    } );
  }


  // Carga mapa base de OpenStreetMap 
  function cagarBaseLayers(){
    //borrado de capas base
    // viewer.imageryLayers.removeAll(); 
    // Añadir OpenStreetMap como capa base
    let noche = Cesium.ImageryLayer.fromProviderAsync(Cesium.IonImageryProvider.fromAssetId(3812));
    baseLayer.push(noche);

    const osm = new Cesium.OpenStreetMapImageryProvider({
        url : 'https://tile.openstreetmap.org/'
    })
    baseLayer.push(osm); // Añade la capa OSM a la lista de capas base


    //hace la capa visible
    // viewer.imageryLayers.addImageryProvider(osm); // Añade la capa OSM

  };


  function createPropertiesPanel(properties) {
    
    let descrip = `<table class="tablePorperties">`;
    for (const [key, value] of Object.entries(properties)) {
      if (key === 'enlace'|| key === 'url' || key === 'link' || key === 'source') {
        // Si el valor es un enlace, lo formateamos como un enlace HTML
        descrip = descrip + `<tr class="trproper">
                                <td>Enlace</td>
                                <td class="tdproper">
                                  <a href="${value}" target="_blank">Ir a Catastro</a>
                                </td>
                              </tr>`;
      }
      else{
        descrip = descrip + `<tr class="trproper">
                                <td class="tdproper">${key}</td>
                                <td class="tdproper"> ${value}</td>
                             </tr>`;
      }
      
    }
    descrip = descrip + '</table>';
    return descrip;
  }

  function positionCamera() {
    const position = viewer.camera.positionCartographic;
    const lon = Cesium.Math.toDegrees(position.longitude);
    const lat = Cesium.Math.toDegrees(position.latitude);
    const alt = position.height;

    console.log(`Posición de la cámara:
      Longitud: ${lon},
      Latitud: ${lat},
      Altitud: ${alt}`);
  }


  // Función para obtener datos del catastro
  function getCatastro(idMunicipio=201,idPoligono=1,idParcela=36) {
    idMunicipio = document.getElementById('idMunicipio').value==="" ? 201 : document.getElementById('idMunicipio').value;
    idPoligono = document.getElementById('idPoligono').value==="" ? 1 : document.getElementById('idPoligono').value;
    idParcela = document.getElementById('idParcela').value==="" ? 36 : document.getElementById('idParcela').value;
    const urlCatastro = urlFastAPI +"/getcatastrolayers/"+idMunicipio+"/"+idPoligono+"/"+idParcela;
    cargarGeoJSON(urlCatastro,true);
  }

  function getCatastroBuscador(idMunicipio,idPoligono,idParcela) {
    const urlCatastro = urlFastAPI +"/getcatastrolayers/"+idMunicipio+"/"+idPoligono+"/"+idParcela;
    cargarGeoJSON(urlCatastro,true);
  }


  function mostrarSpinner() {
    console.log("Mostrando spinner");
    document.getElementById("spinnerOverlay").style.display = "flex";
  }

  function ocultarSpinner() {
    console.log("Ocultando spinner");
    document.getElementById("spinnerOverlay").style.display = "none";
  }
 


  function buscarDireccion() {
    mostrarSpinner();
    let direccionABuscar = document.getElementById('buscadorDirecciones').value.trim();
    if (direccionABuscar === '') {
      alert('Por favor, introduce una dirección.');
      return;
    }

    const urlBuscarDireccion = urlFastAPI + "/buscadorDireccion/" + direccionABuscar;
    fetch(urlBuscarDireccion,{
        method: 'GET', // o 'POST', 'PUT', etc.
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + window.token
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log('Datos de la dirección:', data);

        const resultados = document.getElementById('resultadosBusqueda');
        resultados.innerHTML = ''; // Limpiar resultados anteriores
        if (data.length === 0) {
          resultados.innerHTML = '<li>No se encontraron resultados.</li>';
          return;
        }

        data.map(datos => {
        //  console.log('Datos de la dirección:', datos);
          const li = document.createElement('li');
          li.textContent = datos[0] + ' - (' + datos[1] + ' - ' + datos[2] + ' - ' + datos[3]+ ')';
          li.addEventListener('click', function() {
            getCatastroBuscador(datos[1], datos[2], datos[3]);
          });
          resultados.appendChild(li);
        });

        ocultarSpinner();
      })
      .catch(error => {
        ocultarSpinner();
        console.error('Error al buscar la dirección:', error);
        alert('Error al buscar la dirección. Calle incorrecta o no encontrada.');
      });
  }


  const stripeMaterial = new Cesium.StripeMaterialProperty({
    evenColor: Cesium.Color.WHITE.withAlpha(0.5),
    oddColor: Cesium.Color.BLUE.withAlpha(0.5),
    repeat: 1.0,
  });

  function getTemperatureData() {
    
    arrayTemp=[[-1.643995,42.818313],[-1.985146,43.314755 ],[-2.672234,42.848863]];

    arrayTemp.forEach(coordenada => {
      const lat = coordenada[1];
      const lon = coordenada[0];
      const urlTemp = "https://api.openweathermap.org/data/2.5/weather?lat="+ lat +"&lon="+ lon + "&appid=e467793f3c797662f7eeee239b4a3871&&units=metric";
      fetch(urlTemp)
      .then(response => response.json())
      .then(data => {
        console.log('Datos de temperatura:', data);
        
        const temperaturasUL = document.getElementById('temperaturas');
        const li = document.createElement('li');
        li.textContent = `Temperatura en ${lat}, ${lon}: ${data.main.temp} °C`;
        temperaturasUL.appendChild(li);

        const temperatura = data.main.temp;
        crearPuntoTiempoReal(coordenada,temperatura);
      })
      .catch(error => console.error('Error al obtener los datos de temperatura:', error));
    });
    
  }


  function crearPuntoTiempoReal(datosPunto,temperatura) {
    const coordenadas = datosPunto;
    const [lon, lat] = coordenadas;
    console.log('Coordenadas:', coordenadas);
    console.log('Lat:', lat, 'Lon:', lon);

    viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(lon, lat), // Altura 0 para el terreno
      name: 'Punto de temperatura',
      // description: createPropertiesPanel(datosPunto.properties),
      point:{
        pixelSize: 8,
        color: Cesium.Color.RED.withAlpha(0.8),
        outlineColor: Cesium.Color.BLACK,
        outlineWidth: 1,
        heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND, // Úsalo si el punto está en terreno
        disableDepthTestDistance: Number.POSITIVE_INFINITY // Siempre visible encima del terreno
      },
      ellipsoid: {
        radii: new Cesium.Cartesian3(20000.0, 20000.0, 800),
        material: getColorForTemperature(temperatura),
        heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND  ,
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      }        
    });
    
    volarA(lon, lat, 10000); // Volar a la ubicación del punto

  }
  

  // positionCamera();
   


  //DETECCION DE POLIGONO CON EL MOUSE
