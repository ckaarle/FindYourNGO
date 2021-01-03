import {Injectable} from '@angular/core';
import {ApiService} from './api.service';
import {Observable, of, throwError} from 'rxjs';
import {NewTwReview, TwReview, TwReviews, TwRating} from '../models/ratings';

@Injectable({
  providedIn: 'root'
})
export class RatingService {

  mockTwRatings: { [id: string]: TwRating } = {
    1: {
      totalTrustworthiness: 5,
      baseTrustworthiness: 5,
      userTrustworthiness: 1,
      reviewNumberByRating: {
        5: 0,
        4: 0,
        1: 0,
        2: 0,
        3: 0,
      },
      totalReviewNumber: 0,
    },
    2: {
      totalTrustworthiness: 3.8,
      baseTrustworthiness: 2.4,
      userTrustworthiness: 3.2,
      reviewNumberByRating: {
        5: 10,
        1: 3,
        4: 50,
        3: 88,
        2: 27,
      },
      totalReviewNumber: 10 + 50 + 3 + 27 + 88,
    },
    3: {
      totalTrustworthiness: 1.7,
      baseTrustworthiness: 0,
      userTrustworthiness: 3.4,
      reviewNumberByRating: {
        4: 3,
        5: 5,
        2: 5,
        1: 1,
        3: 2,
      },
      totalReviewNumber: 3 + 5 + 5 + 1 + 2,
    },
  };


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
