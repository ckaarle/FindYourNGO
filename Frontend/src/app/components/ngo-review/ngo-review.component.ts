import {Component, Input, OnInit} from '@angular/core';
import {TwComment} from '../../models/ratings';

@Component({
  selector: 'ngo-review',
  templateUrl: './ngo-review.component.html',
  styleUrls: ['./ngo-review.component.scss']
})
export class NgoReviewComponent implements OnInit {

  @Input() comment: TwComment;

  constructor() {
  }

  ngOnInit(): void {
  }

}
