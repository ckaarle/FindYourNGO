import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {EMPTY_TW_REVIEW, EMPTY_TW_REVIEWS, TwReview, TwReviews} from '../../models/ratings';
import {ApiService} from '../../services/api.service';
import {Router} from '@angular/router';
import {LoginDialogComponent} from '../../screens/login-dialog/login-dialog.component';
import {MatDialog} from '@angular/material/dialog';

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

  constructor(private ratingService: RatingService, private apiService: ApiService, private router: Router, public dialog: MatDialog) {
  }

  ngOnInit(): void {
    console.log('NGO ON INIT WAS CALLED');
    this.ratingService.getUserReviews(this.ngoId).subscribe(data => {

      data.reviews.forEach((review) => {
        console.log(review);
        if (this.isOwnUserId(review.userId)) {
          console.log('OWN USER REVIEW');
          this.ownUserReview = review;
        } else {
          console.log('OTHER USER REVIEW');
          this.otherUserReviews.push(review);
        }
      });
    });
  }

  private isOwnUserId(userId: string): boolean {
    console.log(userId);
    console.log(this.apiService.userid.getValue());
    return userId !== '' && userId === this.apiService.userid.getValue();
  }

  writeNewReview(): void {
    const dialogRef = this.dialog.open(LoginDialogComponent);
    dialogRef.afterClosed().subscribe(result => {

      if (this.apiService.userid.getValue() === '') {
        console.log('User Login Dialog was exited. Aborting.');
        return;
      }

      this.ratingService.getUserHasWrittenReviewForNgo(this.ngoId, this.apiService.userid.getValue()).subscribe(data => {
        if (data) {
          // simply reload
          this.router.navigate(['/detailView', this.ngoId]).then(() => window.location.reload());
        } else {
          this.router.navigate(['/newReview', this.ngoId, {ngoName: this.ngoName}]);
        }
      });
    });
  }
}
