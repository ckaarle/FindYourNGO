import { Component, Inject, OnInit } from '@angular/core';
import { NgoDetailItem } from 'src/app/models/ngo';
import { CustomOverlayRef, NGO_DETAIL_ITEM_DIALOG_DATA } from 'src/app/services/overlay.service';

export interface NgoContentContainer {
  icon: string,
  values: any
}

@Component({
  selector: 'ngo-detail-item',
  templateUrl: './ngo-detail-item.component.html',
  styleUrls: ['./ngo-detail-item.component.scss']
})
export class NgoDetailItemComponent implements OnInit {
  ngoContentContainers: NgoContentContainer[]= [];

  constructor(
    public dialogRef: CustomOverlayRef,
    @Inject(NGO_DETAIL_ITEM_DIALOG_DATA) public ngoDetailItem: any|NgoDetailItem
    ) { }

  ngOnInit(): void {
    this.mapDataToObject();
    this.generateContentContainers();
  }

  containerHasValues(ngoContentContainer: NgoContentContainer): boolean {
    let hasValues = false;
    Object.entries(ngoContentContainer.values).forEach(titleRow => {
      if (hasValues) { 
        return;
      } else {
        hasValues = titleRow[1].values != undefined && (typeof titleRow[1].values == "string" && /\S/.test(titleRow[1].values) || titleRow[1].values.length);
      }
    });
    return hasValues;
  }

  generateContentContainers() {
    this.ngoContentContainers = [
      {icon: 'info', values: this.ngoDetailItem.description},
      {icon: 'group_work', values: this.ngoDetailItem.fieldOfActivity},
      {icon: 'query_stats', values: this.ngoDetailItem.stats},
      {icon: 'location_on', values: this.ngoDetailItem.location},
      {icon: 'person', values: this.ngoDetailItem.contact}
    ]
  }

  mapDataToObject() { //TODO: edit serializer to reduce work here
    this.ngoDetailItem = {
      id: this.ngoDetailItem.id,
      name: this.ngoDetailItem.name,
      acronym: this.ngoDetailItem.acronym,
      description: {
        aim: {displayName: 'Description', values: this.ngoDetailItem.aim},
        typeOfOrganization: {displayName: 'Organization type', values: this.ngoDetailItem.stats.typeOfOrganization},
        website: {displayName: 'Website', values: this.ngoDetailItem.contact.website}
      },
      fieldOfActivity: {
        topics: {displayName: 'Topics', values: this.ngoDetailItem.topics},
        activities: {displayName: 'Activities', values: this.ngoDetailItem.activities},
        branches: {displayName: 'Branches', values: this.ngoDetailItem.branches},
        workingLanguages: {displayName: 'Working languages', values: this.ngoDetailItem.stats.workingLanguages}
      },
      stats: {
        president: {displayName: 'President', values: this.ngoDetailItem.stats.presidentFirstName + ' ' + this.ngoDetailItem.stats.presidentLastName},
        foundingYear: {displayName: 'Founding year', values: this.ngoDetailItem.stats.foundingYear},
        staffNumber: {displayName: 'Staff number', values: this.ngoDetailItem.stats.staffNumber},
        memberNumber: {displayName: 'Member number', values: this.ngoDetailItem.stats.memberNumber},
        yearlyIncome: {displayName: 'Yearly income', values: this.ngoDetailItem.stats.yearlyIncome},
        funding: {displayName: 'Funding', values: this.ngoDetailItem.stats.funding},
        accreditations: {displayName: 'Accreditations', values: this.ngoDetailItem.accreditations}
      },
      location: {
        address: {displayName: 'Address', values: this.ngoDetailItem.contact.address.street + ', ' + this.ngoDetailItem.contact.address.postcode + ' ' + this.ngoDetailItem.contact.address.city + ', ' + this.ngoDetailItem.contact.address.country}
      },
      contact: {
        ngoPhoneNumber: {displayName: 'Phone number', values: this.ngoDetailItem.contact.ngoPhoneNumber},
        ngoEmail: {displayName: 'Email', values: this.ngoDetailItem.contact.ngoEmail},
        representative: {displayName: 'Representative', values: this.ngoDetailItem.contact.representative? this.ngoDetailItem.contact.representative?.representativeFirstName + ' ' + this.ngoDetailItem.contact.representative?.representativeLastName + '\n' + this.ngoDetailItem.contact.representative?.representativeEmail: undefined}
      },
      rating: {
        trustworthiness: {displayName: 'Trustworthiness', values: this.ngoDetailItem.trustworthiness},
        amount: {displayName: 'Amount', values: 10} //TODO
      }
    }

  }

}
