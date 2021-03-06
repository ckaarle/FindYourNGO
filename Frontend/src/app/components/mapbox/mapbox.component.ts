// @ts-nocheck
import {Component} from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';
import * as mapboxgl from 'mapbox-gl';
import * as turf from '@turf/turf';
import {NgoCluster, NgoCoordinates, NgoLink} from '../../models/ngo';
import {AnySourceData} from 'mapbox-gl';

@Component({
  selector: 'app-mapbox',
  templateUrl: './mapbox.component.html',
  styleUrls: ['./mapbox.component.scss']
})

export class MapboxComponent {
  map: mapboxgl.Map;

  style = 'mapbox://styles/mapbox/dark-v10';
  lat = 48.137154;
  lng = 11.576124;
  zoom = 2.0;

  ngos: {[id: number]: NgoCoordinates} = {};

  mapMarkers = {};
  multiLinkSource = {};

  constructor(private mapboxService: MapboxService) {
    this.multiLinkSource = { type: 'FeatureCollection', features: []};
    this.mapMarkers = { type: 'FeatureCollection', features: []};

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
      this.buildMap();
      this.initialiseMap();
    });
  }

  generateCoordinateRanges(): void {
    this.multiLinkSource.features = [];
    this.map.getSource('multiple-link-source').setData(this.multiLinkSource);
    const ngoCluster: NgoCluster[] = [];
    let cluster: any[] = this.map.querySourceFeatures('markerPointData', {sourceLayer: 'clusters'});
    cluster = cluster.filter((c, index, self) => c.id && self.findIndex(item => item.id === c.id) === index);
    cluster.forEach((c: any) => {
        const pixelCoords = this.map.project(c.geometry.coordinates);
        const minPoint = this.map.unproject({x: pixelCoords.x - 50, y: pixelCoords.y - 50});
        const maxPoint = this.map.unproject({x: pixelCoords.x + 50, y: pixelCoords.y + 50});

        ngoCluster.push({
            id: c.id,
            lat_min: maxPoint.lat, // latitude uses reversed values
            lat_max: minPoint.lat,
            lng_min: minPoint.lng,
            lng_max: maxPoint.lng
        });
    });

    let singleMarkers = this.map.querySourceFeatures('markerPointData', {sourceLayer: 'unclustered-point'});
    singleMarkers = singleMarkers.filter((m, index, self) => !m.id && self.findIndex(item => item.properties.id === m.properties.id) === index);
    singleMarkers.forEach((m: any) => {

        ngoCluster.push({
            id: m.properties.id,
            lat_min: m.geometry.coordinates[0],
            lat_max: m.geometry.coordinates[0],
            lng_min: m.geometry.coordinates[1],
            lng_max: m.geometry.coordinates[1]
        });
    });

    this.mapboxService.getNgoLinks(ngoCluster).subscribe((linkData: NgoLink[]) => {
        linkData.forEach((link: NgoLink) => {
          this.addLink(link, cluster);
        });
        this.map.getSource('multiple-link-source').setData(this.multiLinkSource);
    });
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }

  addMarker(): void {
    const geoPoints: any[] = [];
    Object.entries(this.ngos).map(ngo => ngo[1]).forEach((ngoCoordinate: NgoCoordinates) => {
        geoPoints.push(
            {
                type: 'Feature',
                properties: {
                    id: -ngoCoordinate.id,
                    ngo_id: ngoCoordinate.id,
                    name: ngoCoordinate.name,
                    twValue: +ngoCoordinate.trustworthiness.toFixed(2)
                },
                geometry: {
                    type: 'Point',
                    coordinates: [ngoCoordinate.longitude, ngoCoordinate.latitude]
                }
            }
        );
    });
    this.mapMarkers.features = geoPoints;
  }

  addLink(link: NgoLink, cluster: any[]): void {
    const clusterOrigin = cluster.filter(c => c.id === link.id1)[0];
    const clusterDestination = cluster.filter(c => c.id === link.id2)[0];

    if (clusterOrigin && clusterDestination) {
        const origin = turf.point(clusterOrigin.geometry.coordinates);
        const destination = turf.point(clusterDestination.geometry.coordinates);

        const curvedLine = turf.greatCircle(origin, destination);

        const route = {
            type: 'Feature',
            properties: {linkCount: link.link_count},
            geometry: {
                type: 'LineString',
                coordinates: curvedLine.geometry.coordinates
            }
        };
        this.multiLinkSource.features.push(route);
    }
  }

  private initialiseMap(): void {
    this.map.on('load', () => {
      this.addLinkLayer();
      this.addMapCluster();
    });
  }

  addLinkLayer(): void {
      this.map.addSource('multiple-link-source', {
          type: 'geojson',
          data: this.multiLinkSource,
      });

      this.map.addLayer({
        id: 'multiple-link-layer',
        source: 'multiple-link-source',
        type: 'line',
        paint: {
            'line-width': 1,
            'line-color': '#c62828',
        }
      });

      this.map.once('idle', async (e) => { // when all features (suche as clusters) have loaded
          this.generateCoordinateRanges();
      });

      this.addLinkLayerEvents();
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
        'circle-color': '#ffc107',
        'circle-radius': [
            'step',
            ['get', 'point_count'],
            20, 50, // when point count is less than 50
            30, 150, // when point count is between 50 and 150
            40 // when point count is greater than or equal to 150
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
    this.registerPointClick();
    this.registerClusterClick();
    this.registerHovering('clusters');
    this.registerZooming();
  }

  addLinkLayerEvents(): void {
      this.registerHovering('multiple-link-layer');
  }

  registerPointClick(): void {
    this.map.on('click', 'unclustered-point', (e: any) => {
      const coordinates = e.features[0].geometry.coordinates.slice();
      const name = e.features[0].properties.name;
      const twValue = e.features[0].properties.twValue;

      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      new mapboxgl.Popup()
          .setLngLat(coordinates)
          .setHTML(
              name + '<br>TW score: ' + twValue
          )
          .addTo(this.map);
    });
  }

  registerClusterClick(): void {
    this.map.on('click', 'clusters', (e: any) => {
      const coordinates = e.features[0].geometry.coordinates.slice();

      const pointsInCluster = this.mapMarkers.features.filter((f: any) => {
          if (f.geometry.coordinates[0] !== '""' || f.geometry.coordinates[1] !== '""') {
              const pointPixels = this.map.project(f.geometry.coordinates);
              const pixelDistance = Math.sqrt(Math.pow(e.point.x - pointPixels.x, 2) + Math.pow(e.point.y - pointPixels.y, 2));
              return Math.abs(pixelDistance) <= 50;
          }
      });

      let twSum = 0;

      pointsInCluster.forEach((feature: any) => twSum += feature.properties.twValue);
      const avgTw = +(twSum / pointsInCluster.length).toFixed(2);

      const highestNGO = pointsInCluster.reduce((prev, current) => (prev.twValue > current.twValue) ? current : prev).properties;
      const lowestNGO = pointsInCluster.reduce((prev, current) => (prev.twValue > current.twValue) ? prev : current).properties;

      const highestTW = {name: highestNGO.name, twValue: +highestNGO.twValue.toFixed(2)};
      const lowestTW = {name: lowestNGO.name, twValue: +lowestNGO.twValue.toFixed(2)};

      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      const twScoreDescription = highestTW.twValue !== lowestTW.twValue ?
              `<br>Highest TW score: ${highestTW.name} (${highestTW.twValue})` +
              `<br>Lowest TW score: ${lowestTW.name} (${lowestTW.twValue})` : '';

      new mapboxgl.Popup()
          .setLngLat(coordinates)
          .setHTML(
              `Average TW score in this cluster: ${avgTw}` + `${twScoreDescription}`
          )
          .addTo(this.map);
    });
  }

  registerHovering(layerId: string): void {
    let tooltip: any;
    this.map.on('mouseenter', layerId, e => {
      this.map.getCanvas().style.cursor = 'pointer';
      tooltip = layerId === 'multiple-link-layer' ? this.registerLineHover(e) : undefined;
    });

    this.map.on('mouseleave', layerId, () => {
      this.map.getCanvas().style.cursor = '';
      tooltip ? tooltip.remove() : undefined;
    });
  }

  registerZooming(): void {
    this.map.on('moveend', 'clusters', () => {
      this.generateCoordinateRanges();
    });
  }

  registerLineHover(feature): any {
      const linkCount = feature.features[0].properties.linkCount;

      return new mapboxgl.Popup()
          .setLngLat(feature.lngLat)
          .setHTML(
               `Link count: ${linkCount}` +
              `<br>`
          )
          .addTo(this.map);
  }
}
