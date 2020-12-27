import {Component, Input, OnInit} from '@angular/core';
import {TwComment} from '../../models/ratings';
import {RatingService} from '../../services/rating.service';

@Component({
  selector: 'ngo-reviews',
  templateUrl: './ngo-reviews.component.html',
  styleUrls: ['./ngo-reviews.component.scss']
})
export class NgoReviewsComponent implements OnInit {

  ownUserComment: TwComment = null;
  otherUserComments: TwComment[] = [];

  @Input() ngoId: number = 0;

  constructor(private ratingService: RatingService) {
  }

  ngOnInit(): void {
    this.ratingService.getUserReviews(this.ngoId).subscribe(data => {

      data.comments.forEach((comment) => {
        if (this.isOwnUserId(comment.userId)) {
          this.ownUserComment = comment;
        } else {
          this.otherUserComments.push(comment);
        }
      });
    });
  }

  private isOwnUserId(userId: number): boolean {
    return userId <= 0; // TODO compare to actual own user id once it exists
  }

}
