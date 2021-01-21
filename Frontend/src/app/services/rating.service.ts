import {Injectable} from '@angular/core';
import {ApiService} from './api.service';
import {Observable} from 'rxjs';
import {NewTwReview, TwRating, TwReview, TwReviews} from '../models/ratings';

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  constructor(private apiService: ApiService) {
  }

  getTwRating(ngoId: number): Observable<TwRating> {
    return this.apiService.get('twRating', {id: ngoId});
  }

  getUserReviews(ngoId: number): Observable<TwReviews> {
    return this.apiService.get('userReviewsForNgo', {id: ngoId});
  }

  saveReview(newReview: NewTwReview): Observable<any> {
    return this.apiService.put('review', newReview);
  }

  deleteReview(id: number): Observable<any> {
    return this.apiService.delete('review', {id: id});
  }

  getUserReview(reviewId: number): Observable<TwReview> {
    return this.apiService.get('review', {id: reviewId});
  }

  getUserHasWrittenReviewForNgo(ngoId: number, userId: string): Observable<boolean> {
    return this.apiService.get('userReviewPresent', {ngoId: ngoId, userId: userId});
  }
}
