import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {TwReview, TwReviews} from '../../models/ratings';

@Component({
  selector: 'ngo-rating',
  templateUrl: './ngo-rating.component.html',
  styleUrls: ['./ngo-rating.component.scss']
})
export class NgoRatingComponent implements OnInit {

  @Input() ngoId: number;
  @Input() ngoName: string;

  reviews: TwReviews;

  ownUserReview: TwReview;
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
