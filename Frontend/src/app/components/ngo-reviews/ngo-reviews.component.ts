import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngo-reviews',
  templateUrl: './ngo-reviews.component.html',
  styleUrls: ['./ngo-reviews.component.scss']
})
export class NgoReviewsComponent implements OnInit {

  @Input() ngoId: number = 0;

  constructor() {
  }

  ngOnInit(): void {
  }

}
