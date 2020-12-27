import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {StarRatingComponent} from '../star-rating/star-rating.component';
import {NewTwComment} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'ngo-new-review',
  templateUrl: './ngo-new-review.component.html',
  styleUrls: ['./ngo-new-review.component.scss']
})
export class NgoNewReviewComponent implements OnInit, AfterViewInit {

  ngoId: number;
  reviewId: number;
  commentText = '';

  errorMessage = '';
  reviewRating = null;

  @ViewChild('starRatingComponent') starRatingComponent: StarRatingComponent;

  constructor(private ratingService: RatingService, private route: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): void {
    this.ngoId = this.route.snapshot.paramMap.get('ngoId');
    this.reviewId = this.route.snapshot.paramMap.get('reviewId');

    if (this.reviewId != null) {
      this.ratingService.getUserReview(this.reviewId).subscribe(
          (review) => {
            console.log(review)
            this.commentText = review.text;
            this.reviewId = review.id;
            this.reviewRating = review.rating;
            if (this.reviewRating != null) {
              this.starRatingComponent.setValue(this.reviewRating - 1);
            }
          }
      );
    }
  }


  save(): void {
    this.errorMessage = '';

    const userRating = Math.round(this.starRatingComponent.value) + 1;
    const newReview: NewTwComment = {
      commentId: this.reviewId,
      ngoId: this.ngoId,
      userId: 0, // TODO
      rating: userRating,
      text: this.commentText
    };

    this.ratingService.saveReview(newReview).subscribe(
        (success) => this.onSaveSuccess(newReview),
        (error) => this.onSaveError()
    );
  }

  private onSaveSuccess(newReview: NewTwComment): void {
    this.router.navigate(['/detailView', this.ngoId]);
  }

  private onSaveError(): void {
    this.errorMessage = 'Review could not be saved. Please try again later.';
  }
}

// TODO logged out redirection!
