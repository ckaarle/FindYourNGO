import {Component, Input} from '@angular/core';
import { ApiService } from '../../services/api.service';
import {ActivatedRoute} from '@angular/router';
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
  $allNgos: Observable<NgoOverviewItem[]> | undefined;
  inviteeIds: number[] = [];
  inviteeNames: string[] = [];
  eventForm = new FormGroup({
    event_name: new FormControl(null),
    description: new FormControl(null),
    start_date: new FormControl(null),
    end_date: new FormControl(null),
    tags: new FormControl(null),
  });

  constructor(public apiService: ApiService, public userService: UserService, private route: ActivatedRoute) {
    // TODO: This is a hack until ngodetail item does not return undefined
    this.currentNgoId = Number(this.route.snapshot.paramMap.get('id'));
    if (this.currentNgoId !== this.userService.ngoid.value) {
      this.getEvents();
    } else {
      this.updateEvents();
    }
    this.apiService.get('idNames').subscribe((data: NgoOverviewItem[]) =>
      this.$allNgos = this.ngoControl.valueChanges.pipe(startWith(''),
        map(value => data.filter(ngo => ngo.name.toLowerCase().includes(value?.toString().toLowerCase())
          && ngo.id !== this.currentNgoId && !this.inviteeIds.some(x => x === ngo.id)))));
  }

  createEvent(): void {
    const eventVars = this.eventForm.value;
    eventVars.collaborators = this.inviteeIds;
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
    this.apiService.get(`events/invitations`).subscribe(
      (data: NgoEvent[]) => this.invitations = data);
    this.getEvents();
  }

  getEvents(): void {
    this.apiService.get(`events`, {collaborator_id: this.currentNgoId}).subscribe(
      (data: NgoEvent[]) => {
        this.currentEvents = data.filter(event => Date.parse(event.end_date.toString()) > Date.now());
        this.pastEvents = data.filter(event => Date.parse(event.end_date.toString()) < Date.now());
      });
  }

  ngoName(ngo: NgoOverviewItem): string {
    return ngo?.name;
  }

  removeInvitee(invitee: any): void {
    const index = this.inviteeNames.indexOf(invitee);
    if (index >= 0) {
      this.inviteeNames.splice(index, 1);
      this.inviteeIds.splice(index, 1);
    }
  }

  delete(id: number): void {
    this.apiService.post('events/delete/', {event_id: id}, {}).subscribe(data =>
    this.updateEvents());
  }
}
