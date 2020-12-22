import {Component, Input, OnInit} from '@angular/core';
import {RatingService} from '../../services/rating.service';

@Component({
  selector: 'ngo-tw-rating',
  templateUrl: './ngo-tw-rating.component.html',
  styleUrls: ['./ngo-tw-rating.component.scss']
})
export class NgoTwRatingComponent implements OnInit {

  totalTrustworthiness: number;
  baseTrustworthiness: number;
  userTrustworthiness: number;
  totalCommentNumber: number;
  commentNumberIndexedByRating: number[] = [];

  @Input() ngoId: number = 1;

  NGO_ID = 2; // TODO remove later

  constructor(private ratingService: RatingService) {
  }

  ngOnInit(): void {
    // const twRating = this.ratingService.getTwRating(this.ngoId).subscribe(rating => { TODO put back in
    this.ratingService.getTwRating(this.NGO_ID).subscribe(rating => {
      this.totalTrustworthiness = rating.totalTrustworthiness;
      this.baseTrustworthiness = rating.baseTrustworthiness;
      this.userTrustworthiness = rating.userTrustworthiness;
      this.totalCommentNumber = rating.totalCommentNumber;

      const sortedKeys = Object.keys(rating.commentNumberByRating).sort();
      for (const key in sortedKeys) {
        this.commentNumberIndexedByRating.unshift(rating.commentNumberByRating[(+key + 1).toString()]);
      }
    });
  }

}
