import {EventEmitter, Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {ApiService} from './api.service';
import {NgoFavourite, NgoOverviewItem} from '../models/ngo';

@Injectable({
  providedIn: 'root'
})
export class FavouriteService {

  public favouriteChanged: EventEmitter<NgoFavourite> = new EventEmitter<NgoFavourite>();

  constructor(private apiService: ApiService) {
  }

  isUserFavourite(ngoId: string | number): Observable<boolean> {
    if (this.apiService.userid.getValue() < 0) {
      return of(false);
    }
    return this.apiService.get('userFavourite', {ngoId: ngoId, userId: this.apiService.userid.getValue()});
  }

  getUserFavourites(): Observable<NgoOverviewItem[]> {
    if (this.apiService.userid.getValue() < 0) {
      return of([]);
    }
    return this.apiService.get('userFavourites', {userId: this.apiService.userid.getValue()});
  }

  setUserFavourite(favourite: boolean, ngoId: number): Observable<boolean> {
    return this.apiService.post('userFavourite', {favourite: favourite}, {ngoId: ngoId, userId: this.apiService.userid.getValue()});
  }

  emit(favourite: NgoFavourite): void {
    this.favouriteChanged.emit(favourite);
  }
}
