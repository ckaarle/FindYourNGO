import {Injectable} from '@angular/core';
import {ApiService} from './api.service';
import {Observable, of} from 'rxjs';
import {TwRating} from '../models/ratings';

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  mockData: { [id: string]: TwRating } = {
    1: {
      totalTrustworthiness: 5,
      baseTrustworthiness: 5,
      userTrustworthiness: 1,
      commentNumberByRating: {
        5: 0,
        4: 0,
        1: 0,
        2: 0,
        3: 0,
      },
      totalCommentNumber: 0,
    },
    2: {
      totalTrustworthiness: 3.8,
      baseTrustworthiness: 2.4,
      userTrustworthiness: 3.2,
      commentNumberByRating: {
        5: 10,
        1: 3,
        4: 50,
        3: 88,
        2: 27,
      },
      totalCommentNumber: 10 + 50 + 3 + 27 + 88,
    },
    3: {
      totalTrustworthiness: 1.7,
      baseTrustworthiness: 0,
      userTrustworthiness: 3.4,
      commentNumberByRating: {
        4: 3,
        5: 5,
        2: 5,
        1: 1,
        3: 2,
      },
      totalCommentNumber: 3 + 5 + 5 + 1 + 2,
    },
  };

  constructor(private apiService: ApiService) {
  }

  getTwRating(ngoId: number): Observable<TwRating> {
    return of(this.mockData[ngoId.toString()] as TwRating); // TODO delegate to ApiService
  }
}
