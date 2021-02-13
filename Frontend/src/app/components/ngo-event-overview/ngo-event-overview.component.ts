import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import {NgoEvent} from '../../models/ngo';

@Component({
  selector: 'app-ngo-event-overview',
  templateUrl: './ngo-event-overview.component.html',
  styleUrls: ['./ngo-event-overview.component.scss']
})
export class NgoEventOverviewComponent {

  event: NgoEvent = {} as NgoEvent;

  constructor(@Inject(MAT_DIALOG_DATA) public data: { event: NgoEvent }) {
    this.event = data.event;
  }

}
