import {Component, OnInit, ViewChild} from '@angular/core';
import {StarRatingComponent} from '../star-rating/star-rating.component';
import {NewTwReview} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'ngo-new-review',
  templateUrl: './ngo-new-review.component.html',
  styleUrls: ['./ngo-new-review.component.scss']
})
export class NgoNewReviewComponent implements OnInit {

  ngoId: number = 0;
  reviewId: number = 0;
  ngoName = '';
  reviewText = '';

  errorMessage = '';
  reviewRating = 0;

  // @ts-ignore
  @ViewChild('starRatingComponent') starRatingComponent: StarRatingComponent;

  constructor(private ratingService: RatingService, private route: ActivatedRoute, private router: Router, private apiService: ApiService) {
  }

  ngOnInit(): void {
    // @ts-ignore
    this.ngoId = this.route.snapshot.paramMap.get('ngoId');
    // @ts-ignore
    this.reviewId = this.route.snapshot.paramMap.get('reviewId');
    // @ts-ignore
    this.ngoName = this.route.snapshot.paramMap.get('ngoName');


    if (this.reviewId != null) {
      this.ratingService.getUserReview(this.reviewId).subscribe(
          (review) => {
            console.log(review);
            this.reviewText = review.text;
            this.reviewId = review.id;
            this.reviewRating = review.rating;
            if (this.reviewRating != null) {
              // @ts-ignore
              this.starRatingComponent.setValue(this.reviewRating - 1);
            }
          }
      );
    }
  }


  save(): void {
    this.errorMessage = '';

    const userRating = Math.round(this.starRatingComponent.value) + 1;
    const newReview: NewTwReview = {
      reviewId: this.reviewId,
      ngoId: this.ngoId,
      userId: this.apiService.userid.getValue(),
      rating: userRating,
      text: this.reviewText
    };

    this.ratingService.saveReview(newReview).subscribe(
        (success) => this.onSaveSuccess(),
        (error) => this.onSaveError()
    );
  }

  private onSaveSuccess(): void {
    this.router.navigate(['/detailView', this.ngoId]);
  }

  private onSaveError(): void {
    this.errorMessage = 'Review could not be saved. Please try again later.';
  }

  cancel(): void {
    this.onSaveSuccess();
  }
}
