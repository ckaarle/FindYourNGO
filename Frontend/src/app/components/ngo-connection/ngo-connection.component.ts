import {Component, OnDestroy, OnInit, Inject, Input} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {Names, NgoConnection, NgoOverviewItem} from '../../models/ngo';
import {Observable, from} from 'rxjs';
import {map, startWith} from 'rxjs/operators';
import {FormControl} from '@angular/forms';
import {ActivatedRoute} from '@angular/router';
import {UserService} from '../../services/user.service';
import {FilterService} from '../../services/filter.service';

@Component({
  selector: 'app-ngo-connection',
  templateUrl: './ngo-connection.component.html',
  styleUrls: ['./ngo-connection.component.scss']
})
export class NgoConnectionComponent {
  @Input() currentNgoId = -1;

  connections: NgoOverviewItem[] = [];
  incomingRequests: NgoOverviewItem[] = [];
  outgoingRequests: NgoOverviewItem[] = [];
  ngoControl = new FormControl();
  $allNgos: Observable<NgoOverviewItem[]> | undefined;

  constructor(public apiService: ApiService, public userService: UserService, private route: ActivatedRoute, public filter: FilterService) {
    // TODO: This is a hack until ngodetail item does not return undefined
    this.currentNgoId = Number(this.route.snapshot.paramMap.get('id'));
    if (this.currentNgoId !== this.userService.ngoid.value) {
      this.apiService.get(`connections`, {requested_ngo: this.currentNgoId}).subscribe(
      (data: NgoOverviewItem[]) => this.connections = data);
    } else {
      this.updateConnections();
    }
    this.apiService.get('idNames').subscribe((data: NgoOverviewItem[]) =>
      this.$allNgos = this.ngoControl.valueChanges.pipe(startWith(''),
        map(value => data.filter(ngo => ngo.name.toLowerCase().includes(value?.toString().toLowerCase())
          && ngo.id !== this.currentNgoId && !this.connections.some(x => x.id === ngo.id)
          && !this.outgoingRequests.some(x => x.id === ngo.id)))));
  }

  addNgo(): void {
    this.addConnection(this.ngoControl.value.id);
    this.ngoControl.reset();
  }

  addConnection(id: number): void {
    this.apiService.post('connections/add/', {}, {ngo_id: id}).subscribe(
        x => this.updateConnections());
  }

  removeConnection(id: number): void {
    this.apiService.post('connections/remove/', {}, {ngo_id: id}).subscribe(
        x => this.updateConnections());
  }

  updateConnections(): void {
    this.apiService.get(`connections`, {requested_ngo: this.currentNgoId}).subscribe(
      (data: NgoOverviewItem[]) => this.connections = data);
    this.apiService.get(`requests/incoming`).subscribe(
      (data: NgoOverviewItem[]) => this.incomingRequests = data);
    this.apiService.get(`requests/outgoing`).subscribe(
      (data: NgoOverviewItem[]) => this.outgoingRequests = data);
  }

  ngoName(ngo: NgoOverviewItem): string {
    return ngo?.name;
  }
}
