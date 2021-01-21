import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {EMPTY_TW_REVIEWS, TwReview, TwReviews} from '../../models/ratings';

@Component({
  selector: 'ngo-rating',
  templateUrl: './ngo-rating.component.html',
  styleUrls: ['./ngo-rating.component.scss']
})
export class NgoRatingComponent implements OnInit {

  @Input() ngoId: number = 0;
  @Input() ngoName: string = '';

  reviews: TwReviews = EMPTY_TW_REVIEWS;

  // @ts-ignore
  ownUserReview: TwReview = null;
  otherUserReviews: TwReview[] = [];

  constructor(private ratingService: RatingService) {
  }

  ngOnInit(): void {
    this.ratingService.getUserReviews(this.ngoId).subscribe(data => {

      data.reviews.forEach((review) => {
        if (this.isOwnUserId(review.userId)) {
          this.ownUserReview = review;
        } else {
          this.otherUserReviews.push(review);
        }
      });
    });
  }

  
  private isOwnUserId(userId: number): boolean {
    return userId <= 0; // TODO compare to actual own user id once it exists
  }
}
