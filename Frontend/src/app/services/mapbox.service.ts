import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
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
    // return this.apiService.get('map/links'); TODO put back in
    return of([
      {id: 0, connected_ngo_id: 10079, reporter_id: 10065},
      {id: 0, connected_ngo_id: 10095, reporter_id: 10065},
      {id: 0, connected_ngo_id: 10203, reporter_id: 10193},
      {id: 0, connected_ngo_id: 10212, reporter_id: 10203},
      {id: 0, connected_ngo_id: 10249, reporter_id: 10079},
      {id: 0, connected_ngo_id: 10394, reporter_id: 10212},
    ]);
  }
}
