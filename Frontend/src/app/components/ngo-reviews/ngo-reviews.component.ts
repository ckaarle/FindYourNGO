import {Component, Input, OnInit} from '@angular/core';
import {TwReview} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';

@Component({
  selector: 'ngo-reviews',
  templateUrl: './ngo-reviews.component.html',
  styleUrls: ['./ngo-reviews.component.scss']
})
export class NgoReviewsComponent implements OnInit {

  ownUserReview: TwReview = null;
  otherUserReviews: TwReview[] = [];

  @Input() ngoId: number = 0;
  @Input() ngoName: string;

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
