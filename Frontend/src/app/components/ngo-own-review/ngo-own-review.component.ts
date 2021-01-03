import {Component, Input, OnInit} from '@angular/core';
import {TwReview} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';
import {Router} from '@angular/router';

@Component({
  selector: 'ngo-own-review',
  templateUrl: './ngo-own-review.component.html',
  styleUrls: ['./ngo-own-review.component.scss']
})
export class NgoOwnReviewComponent implements OnInit {

  errorMessage: string | undefined = undefined;
  @Input() review: TwReview;
  @Input() ngoName: string;

  constructor(private ratingService: RatingService, private router: Router) {
  }

  ngOnInit(): void {
  }

  delete(): void {
    this.errorMessage = undefined;
    console.log(this.review)
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
    this.router.navigate(['/newReview', this.review.ngoId, {reviewId: this.review.id, ngoName: this.ngoName}]);
  }

}
