import {EventEmitter, Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {ApiService} from './api.service';
import {NgoEvent, NgoFavourite, NgoOverviewItem} from '../models/ngo';
import {UserService} from './user.service';

@Injectable({
  providedIn: 'root'
})
export class FavouriteService {

  public favouriteChanged: EventEmitter<NgoFavourite> = new EventEmitter<NgoFavourite>();

  constructor(private apiService: ApiService, private userService: UserService) {
  }

  isUserFavourite(ngoId: string | number): Observable<boolean> {
    if (this.userService.userid.getValue() < 0) {
      return of(false);
    }
    return this.apiService.get('userFavourite', {ngoId: ngoId, userId: this.userService.userid.getValue()});
  }

  getUserFavourites(): Observable<NgoOverviewItem[]> {
    if (this.userService.userid.getValue() < 0) {
      return of([]);
    }
    return this.apiService.get('userFavourites', {userId: this.userService.userid.getValue()});
  }

  setUserFavourite(favourite: boolean, ngoId: number): Observable<boolean> {
    return this.apiService.post('userFavourite', {favourite: favourite}, {ngoId: ngoId, userId: this.userService.userid.getValue()});
  }

  getUserFavouriteEvents(): Observable<NgoEvent[]> {
    return this.apiService.get('userFavouriteEvents', {userId: this.userService.userid.getValue()});
  }

  emit(favourite: NgoFavourite): void {
    this.favouriteChanged.emit(favourite);
  }
}
