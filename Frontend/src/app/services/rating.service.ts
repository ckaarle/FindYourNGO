import {Injectable} from '@angular/core';
import {ApiService} from './api.service';
import {Observable, of, throwError} from 'rxjs';
import {NewTwReview, TwReview, TwReviews, TwRating} from '../models/ratings';

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  mockComments: TwReviews[] = [
    {
      reviews: [
        {
          id: 0,
          userId: 10,
          userName: 'reaaaaaally long user name',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 2,
          created: new Date(2020, 12, 20),
          last_edited: new Date(2020, 12, 22),
          rating: 2,
          text: 'This is a user comment. It really is not very short. Indeed, it is quite long. So we will see how it will be displayed. Maybe it will look weird, maybe it will look good. Hard to tell.'
        },
        {
          id: 1,
          userId: 11,
          userName: 'User3',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 1,
          created: new Date(2020, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 1,
          text: ''
        },
        {
          id: 2,
          userId: 12,
          userName: 'User4',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 2,
          created: new Date(2019, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 5,
          text: 'Mäh.'
        },
        { // own comment
          id: 3,
          userId: -1,
          userName: 'Me',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 2,
          created: new Date(2020, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 3,
          text: 'This is my user comment. It is quite short :)'
        },
      ],
      reviewNumber: 3
    },
    {
      reviews: [
        {
          id: 4,
          userId: 10,
          userName: 'User2',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 1,
          created: new Date(2020, 12, 20),
          last_edited: new Date(2020, 12, 22),
          rating: 2,
          text: 'This is a user comment. It really is not very short. Indeed, it is quite long. So we will see how it will be displayed. Maybe it will look weird, maybe it will look good. Hard to tell.'
        },
        {
          id: 5,
          userId: -1,
          userName: 'Me',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 2,
          created: new Date(2020, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 3,
          text: 'This is my user comment. It is quite short :)'
        },
        {
          id: 6,
          userId: 11,
          userName: 'User3',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 3,
          created: new Date(2020, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 1,
          text: 'This is also a short comment.'
        }
      ],
      reviewNumber: 3
    },
    {
      reviews: [
        {
          id: 7,
          userId: -1,
          userName: 'Me',
          // userProfile: null,
          ngoId: 21348,
          reviewsByUser: 2,
          created: new Date(2020, 12, 22),
          last_edited: new Date(2020, 12, 22),
          rating: 3,
          text: 'This is my user comment. It is quite short :)'
        }
      ],
      reviewNumber: 1
    },
    {
      reviews: [],
      reviewNumber: 0
    }
  ];

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
}
