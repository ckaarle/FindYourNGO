import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';
import {EMPTY_TW_REVIEW, EMPTY_TW_REVIEWS, TwReview, TwReviews} from '../../models/ratings';
import {ApiService} from '../../services/api.service';
import {Router} from '@angular/router';
import {LoginDialogComponent} from '../../screens/login-dialog/login-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {UserService} from "../../services/user.service";

@Component({
  selector: 'ngo-rating',
  templateUrl: './ngo-rating.component.html',
  styleUrls: ['./ngo-rating.component.scss']
})
export class NgoRatingComponent implements OnInit {

  @Input() ngoId: number = 0;
  @Input() ngoName: string = '';
  @Input() amount: number = 0;

  reviews: TwReviews = EMPTY_TW_REVIEWS;

  // @ts-ignore
  ownUserReview: TwReview = null;
  otherUserReviews: TwReview[] = [];

  constructor(private ratingService: RatingService, private userService: UserService, private apiService: ApiService, private router: Router, public dialog: MatDialog) {
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
    return userId !== -1 && userId === this.userService.userid.getValue();
  }

  writeNewReview(): void {
    const dialogRef = this.dialog.open(LoginDialogComponent);
    dialogRef.afterClosed().subscribe(result => {

      if (this.userService.userid.getValue() === -1) {
        console.log('User Login Dialog was exited. Aborting.');
        return;
      }

      this.ratingService.getUserHasWrittenReviewForNgo(this.ngoId, this.userService.userid.getValue()).subscribe(data => {
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
