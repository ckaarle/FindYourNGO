import { Component, Inject, OnInit } from '@angular/core';
import { NgoDetailItem } from 'src/app/models/ngo';
import { CustomOverlayRef, NGO_DETAIL_ITEM_DIALOG_DATA } from 'src/app/services/overlay.service';

@Component({
  selector: 'ngo-detail-item',
  templateUrl: './ngo-detail-item.component.html',
  styleUrls: ['./ngo-detail-item.component.scss']
})
export class NgoDetailItemComponent implements OnInit {

  constructor(
    public dialogRef: CustomOverlayRef,
    @Inject(NGO_DETAIL_ITEM_DIALOG_DATA) public ngoDetailItem: NgoDetailItem
    ) { }

  ngOnInit(): void {
    this.ngoDetailItem.amount = 10; //TODO
    
  }

}
