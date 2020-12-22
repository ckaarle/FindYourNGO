import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'ngo-rating',
  templateUrl: './ngo-rating.component.html',
  styleUrls: ['./ngo-rating.component.scss']
})
export class NgoRatingComponent implements OnInit {

  @Input() ngoId: number = 0;

  constructor() { }

  ngOnInit(): void {
  }

}
