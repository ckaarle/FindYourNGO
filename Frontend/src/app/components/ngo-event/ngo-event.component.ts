import {Component, Input, ChangeDetectorRef} from '@angular/core';
import { ApiService } from '../../services/api.service';
import {ActivatedRoute, UrlSerializer} from '@angular/router';
import {NgoOverviewItem} from '../../models/ngo';
import {map, startWith} from 'rxjs/operators';
import {FormControl, FormGroup} from '@angular/forms';
import {Observable} from 'rxjs';
import {UserService} from '../../services/user.service';

export interface NgoEvent {
  id: number;
  name: string;
  start_date: Date;
  end_date: Date;
  organizer: number;
  description: string;
  tags: string;
}

@Component({
  selector: 'app-ngo-event',
  templateUrl: './ngo-event.component.html',
  styleUrls: ['./ngo-event.component.scss']
})
export class NgoEventComponent {
  @Input() currentNgoId = -1;

  currentEvents: NgoEvent[] = [];
  pastEvents: NgoEvent[] = [];
  invitations: NgoEvent[] = [];
  ngoControl = new FormControl();
  $allNgos: Observable<NgoOverviewItem[]>;
  inviteeIds: number[] = [];
  inviteeNames: string[] = [];
  eventForm = new FormGroup({
    event_name: new FormControl(null),
    description: new FormControl(null),
    start_date: new FormControl(null),
    end_date: new FormControl(null),
    tags: new FormControl(null),
  });

  constructor(public apiService: ApiService, public userService: UserService, private route: ActivatedRoute, private changeDetector: ChangeDetectorRef) {
    this.currentNgoId = Number(this.route.snapshot.paramMap.get('id'));  // TODO: This is a hack until ngodetail item does not return undefined
    this.updateEvents();
    this.apiService.get('idNames').subscribe((data: NgoOverviewItem[]) =>
      this.$allNgos = this.ngoControl.valueChanges.pipe(startWith(''),
          map(value => data.filter(ngo => ngo.name.toLowerCase().includes(value.toLowerCase()) && ngo.id !== this.currentNgoId))));
  }

  createEvent(): void {
    const eventVars = this.eventForm.value;
    eventVars.collaborators = this.inviteeIds;
    console.log(eventVars);
    this.apiService.post('events/create/', eventVars).subscribe(
        data => this.updateEvents());
    this.eventForm.reset();
    this.ngoControl.reset();
    this.inviteeIds = [];
    this.inviteeNames = [];
  }

  inviteToEvent(): void {
    this.apiService.post('events/invite/', {}, {}).subscribe(
        data => this.updateEvents());
  }

  addNgoToEvent(): void {
    const id = this.ngoControl.value.id;
    if (!this.inviteeIds.includes(id)) {
      this.inviteeIds.push(this.ngoControl.value.id);
      this.inviteeNames = [...this.inviteeNames, this.ngoControl.value.name];  // use spread operator, so angular sees changes
    }
    this.ngoControl.reset();
  }

  acceptEvent(id: number): void {
    this.apiService.post('events/accept/', {}, {event_id: id}).subscribe(
        data => this.updateEvents());
  }

  rejectEvent(id: number): void {
    this.apiService.post('events/reject/', {}, {event_id: id}).subscribe(
        data => this.updateEvents());
  }

  updateEvents(): void {
    this.apiService.get(`events`, {collaborator_id: this.currentNgoId}).subscribe(
      (data: NgoEvent[]) => {
        this.currentEvents = data.filter(event => Date.parse(event.end_date.toString()) > Date.now());
        this.pastEvents = data.filter(event => Date.parse(event.end_date.toString()) < Date.now());
      });
    this.apiService.get(`events/invitations`).subscribe(
      (data: NgoEvent[]) => this.invitations = data);
  }

  ngoName(ngo: NgoOverviewItem): string {
    return ngo?.name;
  }
}
