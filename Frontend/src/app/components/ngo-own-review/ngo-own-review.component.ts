import {Component, Input, OnInit} from '@angular/core';
import {TwComment} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';
import {Router} from '@angular/router';

@Component({
  selector: 'ngo-own-review',
  templateUrl: './ngo-own-review.component.html',
  styleUrls: ['./ngo-own-review.component.scss']
})
export class NgoOwnReviewComponent implements OnInit {

  errorMessage: string | undefined = undefined;
  @Input() comment: TwComment;

  constructor(private ratingService: RatingService, private router: Router) {
  }

  ngOnInit(): void {
  }

  delete(): void {
    this.errorMessage = undefined;
    this.ratingService.deleteReview(this.comment.id).subscribe(
        (success) => this.showDeleteSuccess(),
        (error) => this.showDeleteError(),
    );
  }

  private showDeleteSuccess(): void {
    // I am not sure why manually reloading is necessary
    this.router.navigate(['/detailView', this.comment.ngoId]).then(() => window.location.reload());
  }

  private showDeleteError(): void {
    this.errorMessage = 'Review could not be deleted. Please try again later.';
  }

  edit(): void {
    this.router.navigate(['/newReview', this.comment.ngoId, {reviewId: this.comment.id}]);
  }

}
