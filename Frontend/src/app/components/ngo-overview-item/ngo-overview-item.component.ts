import { Component, Input, OnInit } from '@angular/core';
import { NgoOverviewItem } from '../../models/ngo';

@Component({
  selector: 'ngo-overview-item',
  templateUrl: './ngo-overview-item.component.html',
  styleUrls: ['./ngo-overview-item.component.scss']
})
export class NgoOverviewItemComponent implements OnInit {
  @Input() ngoOverviewItem: NgoOverviewItem = {} as NgoOverviewItem;
  @Input() editableRating: boolean = false;
  
  constructor() { }

  ngOnInit(): void {
  }

}
