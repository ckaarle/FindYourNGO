import {Component, OnInit} from '@angular/core';
import {NgoDetailItem} from 'src/app/models/ngo';
import {ActivatedRoute} from '@angular/router';
import {ApiService} from '../../services/api.service';
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
  public ngoDetailItem: any | NgoDetailItem;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {
    let id = this.route.snapshot.paramMap.get('id');
    this.apiService.get('ngoDetailItem', {id: id}).subscribe(data => {
      this.ngoDetailItem = data;
    this.ngoDetailItem = Utils.mapDataToNgoDetailItem(this.ngoDetailItem);
      this.generateContentContainers();
    });
  }

  ngOnInit(): void {
  }

  containerHasValues(ngoContentContainer: NgoContentContainer): boolean {
    let hasValues = false;
    const ngoContentContainerTitles = ngoContentContainer.values;
    for (const title of Object.keys(ngoContentContainerTitles)) {
      if (hasValues) {
        break;
      } else {
        hasValues = ngoContentContainerTitles[title].values &&
            (ngoContentContainerTitles[title].values != '' || ngoContentContainerTitles[title].values.length > 0);
      }
    }
    return hasValues;
  }

  titleRowHasValues(titleRow: any): boolean {
    return titleRow && (titleRow != '' || titleRow.length > 0);
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
