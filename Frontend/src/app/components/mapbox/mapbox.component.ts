import {Component, OnInit} from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';
import * as mapboxgl from 'mapbox-gl';
import * as turf from '@turf/turf';
import {NgoCoordinates} from '../../models/ngo';
import {AnySourceData} from 'mapbox-gl';

@Component({
  selector: 'app-mapbox',
  templateUrl: './mapbox.component.html',
  styleUrls: ['./mapbox.component.scss']
})
export class MapboxComponent {

  // TODO cluster instead of marker?
  // TODO only one layer for links (speedup?)

  // @ts-ignore
  map: mapboxgl.Map;
  style = 'mapbox://styles/mapbox/dark-v10';
  lat = 48.137154;
  lng = 11.576124;
  zoom = 1.0;

  color = '#fffff';

  ngos: {[id: number]: NgoCoordinates} = {};

  mapMarkers = {};
  multiLinkSource = {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [] as object[],
    }
  };

  constructor(private mapboxService: MapboxService) {
    this.color = getComputedStyle(document.body).getPropertyValue('--secondary-color');


    // @ts-ignore
    mapboxgl.accessToken = 'pk.eyJ1IjoiZmluZHlvdXJuZ28iLCJhIjoiY2tsM3l2azAzMWpqZzJ2bGI2a2JzNzl0OSJ9.hFUVv4mpv0ySKsCecmuKtQ';

    this.mapboxService.getNgoCoordinates().subscribe(data => {
      data.forEach(
          (plot: any) => {
            const name = plot.name;
            const id = plot.id;
            const longitude = plot.coordinates[1];
            const latitude = plot.coordinates[0];
            const trustworthiness = plot.trustworthiness;

            this.ngos[id] = {
              id,
              name,
              longitude,
              latitude,
              trustworthiness
            };
          });

      this.addMarker();

      this.mapboxService.getNgoLinks().subscribe(linkData => {
        linkData.forEach((link: any) => {
          if (link.connected_ngo_id > link.reporter_id) {
            const connectedNgoId = link.connected_ngo_id;
            const reporterNgoId = link.reporter_id;

            const coordinatesNgo = this.ngos[connectedNgoId];
            const coordinatesReporter = this.ngos[reporterNgoId];

            this.addLink(coordinatesNgo.longitude, coordinatesNgo.latitude, coordinatesReporter.longitude, coordinatesReporter.latitude,
                coordinatesNgo.name, coordinatesReporter.name);
          }
        });
          this.buildMap();
          this.initialiseMap();
      });
    });
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }

  addMarker(): void {
    const geoPoints = {
      type: 'FeatureCollection',
      features: []
    };

    Object.entries(this.ngos).map(ngo => ngo[1]).forEach((ngoCoordinate: NgoCoordinates) => {
        geoPoints.features.push(
            {
                type: 'Feature',
                properties: {
                    id: ngoCoordinate.id,
                    name: ngoCoordinate.name,
                    twValue: ngoCoordinate.trustworthiness
                },
                geometry: {
                    type: 'Point',
                    coordinates: [ngoCoordinate.longitude, ngoCoordinate.latitude]
                }
            }
        );
    });

    this.mapMarkers = geoPoints;
    console.log("This mapMarkers: ", this.mapMarkers);
  }

  addLink(lng1: number, lat1: number, lng2: number, lat2: number, name1: string, name2: string): void {
    const origin = turf.point([lng1, lat1]);
    const destination = turf.point([lng2, lat2]);

    const curvedLine = turf.greatCircle(origin, destination, {properties: {name: name1 + ' --- ' + name2}});

    const route = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: [origin, destination],
      }
    };
    // @ts-ignore
    route.geometry.coordinates = curvedLine.geometry.coordinates;
    this.multiLinkSource.data.features.push(route);
  }

  private initialiseMap(): void {
    this.map.on('load', () => {
      this.addMapCluster();
      this.map.addSource('multiple-link-source', this.multiLinkSource as AnySourceData);

      this.map.addLayer({
          id: 'multiple-link-source',
          source: 'multiple-link-source',
          type: 'line',
          paint: {
            'line-width': 3,
            'line-color': this.color,
          }
        });
    });
  }

  addMapCluster(): void {
    this.map.addSource('markerPointData', {
          type: 'geojson',
          data: this.mapMarkers,
          cluster: true,
          clusterMaxZoom: 14,
          clusterRadius: 50
      });

    this.map.addLayer({
        id: 'clusters',
        type: 'circle',
        source: 'markerPointData',
        filter: ['has', 'point_count'],
        paint: {
        // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
        // with three steps to implement three types of circles:
        //   * 20px circles when point count is less than 50
        //   * 30px circles when point count is between 50 and 150
        //   * 40px circles when point count is greater than or equal to 150
        'circle-color': '#ffc107',
        'circle-radius': [
            'step',
            ['get', 'point_count'],
            20, 50,
            30, 150,
            40
        ]
        }
    });

    this.map.addLayer({
        id: 'cluster-count',
        type: 'symbol',
        source: 'markerPointData',
        filter: ['has', 'point_count'],
        layout: {
          'text-field': '{point_count_abbreviated}',
          'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
          'text-size': 10
        }
    });

    this.map.addLayer({
        id: 'unclustered-point',
        type: 'circle',
        source: 'markerPointData',
        filter: ['!', ['has', 'point_count']],
        paint: {
          'circle-color': '#c62828',
            'circle-radius': 4,
            'circle-stroke-width': 1,
            'circle-stroke-color': '#fff'
        }
    });

    this.addMapClusterEvents();
  }

  addMapClusterEvents(): void {
    this.map.on('click', 'unclustered-point', (e: any) => {
      const coordinates = e.features[0].geometry.coordinates.slice();
      const name = e.features[0].properties.name;
      const twValue = e.features[0].properties.twValue;

      // Ensure that if the map is zoomed out such that
      // multiple copies of the feature are visible, the
      // popup appears over the copy being pointed to.
      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      new mapboxgl.Popup()
          .setLngLat(coordinates)
          .setHTML(
              name + '<br>TW value: ' + twValue
          )
          .addTo(this.map);
    });

    this.map.on('click', 'clusters', (e: any) => {
      const coordinates = e.features[0].geometry.coordinates.slice();

      const pointsInCluster = this.mapMarkers.features.filter((f: any) => {
        const pointPixels = this.map.project(f.geometry.coordinates);
        const pixelDistance = Math.sqrt(Math.pow(e.point.x - pointPixels.x, 2) + Math.pow(e.point.y - pointPixels.y, 2));
        return Math.abs(pixelDistance) <= 50;
      });

      let twSum = 0;

      pointsInCluster.forEach((feature: any) => twSum += feature.properties.twValue);
      const avgTw = twSum / pointsInCluster.length;

      const highestNGO = pointsInCluster.reduce((prev, current) => (prev.twValue > current.twValue) ? prev : current).properties;
      const lowestNGO = pointsInCluster.reduce((prev, current) => (prev.twValue < current.twValue) ? prev : current).properties;

      const highestTW = {name: highestNGO.name, twValue: highestNGO.twValue};
      const lowestTW = {name: lowestNGO.name, twValue: lowestNGO.twValue};

      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      new mapboxgl.Popup()
          .setLngLat(coordinates)
          .setHTML(
              `Average TW value in this cluster: ${avgTw}` +
              `<br>Highest TW value: ${highestTW.name} (${highestTW.twValue})` +
              `<br>Lowest TW value: ${lowestTW.name} (${lowestTW.twValue})`
          )
          .addTo(this.map);
    });

    this.map.on('mouseenter', 'clusters', () => {
      this.map.getCanvas().style.cursor = 'pointer';
    });

    this.map.on('mouseleave', 'clusters', () => {
      this.map.getCanvas().style.cursor = '';
    });
  }
}
