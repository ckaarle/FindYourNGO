import {Component, Input, OnInit} from '@angular/core';
import {EMPTY_TW_REVIEW, TwReview} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';
import {Router} from '@angular/router';

@Component({
  selector: 'ngo-review',
  templateUrl: './ngo-review.component.html',
  styleUrls: ['./ngo-review.component.scss']
})
export class NgoReviewComponent implements OnInit {

  errorMessage: string | undefined = undefined;
  @Input() review: TwReview = EMPTY_TW_REVIEW;
  @Input() ngoName: string = '';
  @Input() editable: boolean = false;

  constructor(private ratingService: RatingService, private router: Router) {
  }

  ngOnInit(): void {
  }

  delete(): void {
    if (!this.editable) {
      return;
    }
    this.errorMessage = undefined;
    console.log(this.review);
    this.ratingService.deleteReview(this.review.id).subscribe(
        (success) => this.showDeleteSuccess(),
        (error) => this.showDeleteError(),
    );
  }

  private showDeleteSuccess(): void {
    // I am not sure why manually reloading is necessary
    this.router.navigate(['/detailView', this.review.ngoId]).then(() => window.location.reload());
  }

  private showDeleteError(): void {
    this.errorMessage = 'Review could not be deleted. Please try again later.';
  }

  edit(): void {
    if (!this.editable) {
      return;
    }
    this.router.navigate(['/newReview', this.review.ngoId, {reviewId: this.review.id, ngoName: this.ngoName}]);
  }

}
