import {Component, ViewChild} from '@angular/core';
import {CalendarOptions, EventClickArg, EventInput, FullCalendarComponent} from '@fullcalendar/angular';
import {FavouriteService} from '../../services/favourite.service';
import {NgoEvent} from '../../models/ngo';
import {MatDialog} from '@angular/material/dialog';
import {NgoEventOverviewComponent} from '../ngo-event-overview/ngo-event-overview.component';


@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss']
})
export class CalendarComponent {

  // @ts-ignore
  @ViewChild('calendar') calendarComponent: FullCalendarComponent;

  events: NgoEvent[] = [];

  calendarOptions: CalendarOptions = {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    initialView: 'dayGridMonth',
    initialEvents: [],
    weekends: true,
    editable: false,
    selectable: false,
    selectMirror: true,
    dayMaxEvents: true,
    eventClick: this.handleEventClick.bind(this),
    eventColor: getComputedStyle(document.body).getPropertyValue('--secondary-color'),
  };

  constructor(private favouriteService: FavouriteService, private dialog: MatDialog) {
    this.favouriteService.getUserFavouriteEvents().subscribe(events => {
      this.events = events;
      this.calendarOptions.events = this.convertToCalendarEvents(events);

      // TODO hack: this timeout is noticeable, but without it, the initial view of the calendar will have a weird size (size will update
      //  after clicking anywhere on the calendar)
      setTimeout(() => {
        this.calendarComponent.getApi().updateSize();
      }, 200);
    });
  }

  handleEventClick(clickInfo: EventClickArg): void {
    const event = this.events.filter(e => e.id === +(clickInfo.event.id))[0];
    // @ts-ignore
    this.dialog.open(NgoEventOverviewComponent, {
      data: {event: event}
    });
  }

  private convertToCalendarEvents(events: NgoEvent[]): EventInput[] {
    const eventInputs: EventInput[] = [];

    events.forEach(event => {
      eventInputs.push({
        id: event.id.toString(),
        title: event.name,
        start: event.start_date,
        end: event.end_date,
        allDay: true, // so far, we have no exact times for events
      });
    });

    return eventInputs;
  }
}
