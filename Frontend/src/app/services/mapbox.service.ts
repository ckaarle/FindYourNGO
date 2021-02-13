import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {ApiService} from './api.service';

@Injectable({
  providedIn: 'root'
})
export class MapboxService {

  constructor(private apiService: ApiService) {
  }

  getNgoCoordinates(): Observable<any> {
    return this.apiService.get('map/plots');
  }

  getNgoLinks(): Observable<any> {
    return this.apiService.get('map/links');
  }
}
