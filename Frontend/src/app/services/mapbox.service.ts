import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {ApiService} from './api.service';
import {NgoCluster, NgoLink} from '../models/ngo';

@Injectable({
  providedIn: 'root'
})
export class MapboxService {

  constructor(private apiService: ApiService) {
  }

  getNgoCoordinates(): Observable<any> {
    return this.apiService.get('map/plots');
  }

  getNgoLinks(ngoCluster: NgoCluster[]): Observable<NgoLink[]> {
    return this.apiService.get('map/links', ngoCluster);
  }
}
