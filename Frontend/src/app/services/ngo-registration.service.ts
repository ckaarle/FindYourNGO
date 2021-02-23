import {Injectable} from '@angular/core';
import {NewNgo} from '../models/ngo';
import {Observable} from 'rxjs';
import {ApiService} from './api.service';

@Injectable({
  providedIn: 'root'
})
export class NgoRegistrationService {

  constructor(private apiService: ApiService) {
  }

  registerNewNgo(newNgo: NewNgo): Observable<any> {
    return this.apiService.post('registerNgo', {ngo: newNgo}, {});
  }
}
