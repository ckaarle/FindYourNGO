import { Component, Inject, OnInit } from '@angular/core';
import { NgoDetailItem } from 'src/app/models/ngo';
import { CustomOverlayRef, NGO_DETAIL_ITEM_DIALOG_DATA } from 'src/app/services/overlay.service';
import {Utils} from '../../services/utils';

export interface NgoContentContainer {
  icon: string;
  values: any;
}

@Component({
  selector: 'ngo-detail-item',
  templateUrl: './ngo-detail-item.component.html',
  styleUrls: ['./ngo-detail-item.component.scss']
})
export class NgoDetailItemComponent implements OnInit {
  ngoContentContainers: NgoContentContainer[] = [];

  constructor(
    public dialogRef: CustomOverlayRef,
    @Inject(NGO_DETAIL_ITEM_DIALOG_DATA) public ngoDetailItem: NgoDetailItem
    ) { }

  ngOnInit(): void {
    this.ngoDetailItem = Utils.mapDataToNgoDetailItem(this.ngoDetailItem);
    this.generateContentContainers();
  }

  containerHasValues(ngoContentContainer: NgoContentContainer): boolean {
    let hasValues = false;
    const ngoContentContainerTitles = ngoContentContainer.values;
    for (const title of Object.keys(ngoContentContainerTitles)) {
      if (hasValues) {
        break;
      } else {
        hasValues = ngoContentContainerTitles[title].values &&
            (ngoContentContainerTitles[title].values !== '' || ngoContentContainerTitles[title].values.length > 0);
      }
    }
    return hasValues;
  }

  titleRowHasValues(titleRow: any): boolean {
    return titleRow && (titleRow !== '' || titleRow.length > 0);
  }

  generateContentContainers(): void {
    this.ngoContentContainers = [
      {icon: 'info', values: this.ngoDetailItem.description},
      {icon: 'group_work', values: this.ngoDetailItem.fieldOfActivity},
      {icon: 'query_stats', values: this.ngoDetailItem.stats},
      {icon: 'person', values: this.ngoDetailItem.contact}
    ];
  }

}
